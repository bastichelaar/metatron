# -*- coding: utf-8 -*-

import os
import sys
import signal
import json
from threading import Thread
from subprocess import Popen, PIPE

from . import get_logger
from .decorators import deprecated
from ..exceptions import BlazeException, BlazeMetadataNotFound, BlazeImageNotFound


@deprecated
def check_output(cmd, cwd=None, stdin=None, stderr=None, shell=False, both=False):
    """
    Runs a command and returns its output to stdout

    :param cmd: List containing the command and arguments as strings
    :return:    Output returned by the command
    """
    p = Popen(cmd, cwd=cwd, stdin=stdin, stderr=stderr, shell=shell,
              stdout=PIPE)
    out, err = p.communicate()
    if both:
        return out, err
    return out


class CommandOutput(object):
    def __init__(self, out, err, status):
        self.out = out
        self.err = err
        self.status = status

    @property
    def success(self):
        return self.status == 0

    @property
    def failure(self):
        return not self.success

    def __iter__(self):
        return iter([self.out, self.err, self.status])


def run_command(cmd, cwd=None, verbose=False):
    """
    Runs a command and returns its stdout and sterr output as well as the exit status code.

    :param cmd:     List containing the command and arguments as strings
    :param cwd:     Working directory from where the command is run
    :param verbose: Enable live output of both stdout and stderr
    :return:        Output returned by the command
    """
    child = Popen(cmd, cwd=cwd, stderr=PIPE, stdout=PIPE)

    results = ["", ""]

    def live_output(input_stream, output_stream, results, index):
        while child.poll() is None:
            line = input_stream.readline()
            if verbose:
                output_stream.write(line)
                output_stream.flush()
            results[index] += line
        rest = input_stream.read()
        if rest:
            results[index] += rest
            if verbose:
                output_stream.write(rest)
                output_stream.flush()

    thread_out = Thread(target=live_output, args=(child.stdout, sys.stdout, results, 0))
    thread_err = Thread(target=live_output, args=(child.stderr, sys.stderr, results, 1))
    thread_out.start()
    thread_err.start()
    thread_out.join()
    thread_err.join()

    out, err = results
    status = child.returncode

    return CommandOutput(out, err, status)


def generate_tag():
    """
    Generates a tag name following the Blaze specifications: "number of commits"-"revision hash"

    For example, 42-bad1337

    :return: Generated tag
    """
    if not os.path.isdir(os.path.join(os.getcwd(), ".git")):
        raise BlazeException("Could not generate tag: current directory is not the root of a Git repository")

    git_version  = run_command(["git", "rev-list",  "--count", "HEAD"]).out.strip()
    git_revision = run_command(["git", "rev-parse", "--short", "HEAD"]).out.strip()

    return "%s-%s" % (git_version, git_revision)


def handle_sigint():
    """
    Makes the current program exit with an exit code of 1 upon receiving a SIGINT
    """
    signal.signal(signal.SIGINT, lambda signum, frame: sys.exit(1))


def get_metadata(image, tag, pull=True):
    """
    Pulls an image, converts and returns its metadata as a dictionary

    TODO: In the future, find a solution for remote inspection without pull,
    or implement a metadata service that contains recent images.

    :param image: name of the docker image
    :param tag:   desired tag of the image
    :param pull:  if set, the image will be pulled first (only for debugging and testing)
    :returns:     metadata dictionary tree
    """
    log = get_logger()
    full_name = "%s:%s" % (image, tag)

    if pull:
        log.info("Pulling image %s from docker hub" % full_name)
        out, err, _ = run_command(["docker", "pull", full_name])
        if "not found" in err:
            raise BlazeImageNotFound("Image %s not found on docker hub" % full_name)

    log.info("Inspecting local image %s" % full_name)
    inspection_raw, err, _ = run_command(["docker", "inspect", full_name])
    if "No such image" in err:
        raise BlazeImageNotFound("Image %s not found locally" % full_name)

    if pull:  # pragma: no cover
        log.info("Removing local image %s" % full_name)
        run_command(["docker", "rmi", full_name])

    inspection_json = json.loads(inspection_raw)

    config = inspection_json[0]["Config"]
    labels = dict(filter(lambda e: e[0].startswith("blaze.service"), config["Labels"].iteritems()))
    env = config["Env"]

    if len(labels) == 0:
        raise BlazeMetadataNotFound("Image %s doesn't contain new-style metadata" % full_name)

    result = {}

    for list_entry in filter(lambda e: e.endswith(".list"), labels):
        elems_keys = filter(lambda e: e.startswith(list_entry + "."), labels)
        elems_keys = sorted(elems_keys)
        elems = [labels[key] for key in elems_keys]
        labels[list_entry[:-5]] = elems
        del labels[list_entry]
        for key in elems_keys:
            del labels[key]

    def add_to_tree(key, value, tree):
        last = tree
        for part in key[:-1]:
            if part not in last:
                last[part] = {}
            last = last[part]
        last[key[-1]] = value

    new = {key[14:]: value for key, value in labels.iteritems()}
    for key, value in new.iteritems():
        key = key.split(".")
        if not(isinstance(value, list)):
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    pass
            if value == "true": value = True
            if value == "false": value = False
        add_to_tree(key, value, result)

    result["environment"] = {key: value for key, value in map(lambda entry: entry.split("=", 1), env)}

    return result


#!/usr/bin/env python3
"""
Dirwatcher - A long-running program
"""

__author__ = "Reginald Jefferson, TDD, BabyNames"

import sys
import argparse
import logging
import signal
import time
import os

logger = logging.getLogger(__file__)
files_logged = []
magic_text = {}
stay_running = True


def search_for_magic(filename, start_line, magic_string):
    # Your code here
    return


def watch_directory(path, magic_string, extension, interval):
    # Your code here
    return


def create_parser():
    # needs....
    """An argument that controls the polling interval
    (instead of hard-coding it)"""
    """An argument that specifics the "magic text" to search for"""
    """An argument that filters what kind of file extension
    to search within (i.e., .txt, .log)"""
    """An argument to specify the
    directory to watch (this directory may not yet exist!)"""

    parser = argparse.ArgumentParser(
        description='Checking for magic string and logging instances'
    )
    parser.add_argument(
        'i', 'int', help='controls the polling interval')
    parser.add_argument(
        'm', 'mag', help='specifies the magic text to search for')
    parser.add_argument(
        'f', 'fil', help='filters what kind of file extension to search')
    parser.add_argument(
        'w', 'watch', help='specify the directory to watch')

    return parser


def signal_handler(sig_num, frame):
    """This is a handler for SIGTERM and SIGINT.
    Other signals can be mapped here as well (SIGHUP?)
    Basically, it just sets a global flag, and main()
    will exit its loop if the signal is trapped.
    :param sig_num: The integer signal number
    that was trapped from the OS.:param frame: Not used :return None"""

    # setting up signals, program runs indefinitely unless loop is exited
    global stay_running
    sigs = dict((k, v) for v, k in reversed(sorted(signal.__dict__.items()))
                if v.startswith('SIG') and not v.startswith('SIG_'))
    logger.warning('Received OS Signal: {}'.format(sigs[sig_num]))
    stay_running = False


def main(args):
    # calling parser
    parser = create_parser()
    args = parser.parse_args()

    return


if __name__ == '__main__':
    main(sys.argv[1:])

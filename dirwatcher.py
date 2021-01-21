#!/usr/bin/env python3
"""
Dirwatcher - A long-running program
"""

__author__ = "Reginald Jefferson, TDD, BabyNames"

import sys
import argparse


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
    # Your code here
    return


def main(args):
    # Your code here
    return


if __name__ == '__main__':
    main(sys.argv[1:])

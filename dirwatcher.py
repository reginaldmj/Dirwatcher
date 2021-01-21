#!/usr/bin/env python3
"""
Dirwatcher - A long-running program
"""

__author__ = "Reginald Jefferson"

import sys


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
    return


def signal_handler(sig_num, frame):
    # Your code here
    return


def main(args):
    # Your code here
    return


if __name__ == '__main__':
    main(sys.argv[1:])

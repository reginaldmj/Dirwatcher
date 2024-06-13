#!/usr/bin/env python3
"""
Dirwatcher - A long-running program
Monitors a folder from the command line for any files with an extension.
Checks if a specific 'Magic String' is found and which line.
"""

__author__ = """Reginald Jefferson
                Standup & demos with Dan"""

import sys
import logging
import signal
import time
import os
import argparse
import errno


logger = logging.getLogger(__name__)

exit_flag = False
files = {}


def search_for_magic(filename, start_line, magic_string):
    """Looks for a magic string and its line provided in command."""
    # logger.info(f"Looking for '{magic_string}' in {filename}.")
    line_num = -1
    with open(filename) as f:
        for line_num, line in enumerate(f):
            if line_num >= start_line:
                if magic_string in line:
                    logger.info(
                        f"Found {magic_string} on line {line_num + 1} "
                        f"in file {filename}")
    return line_num + 1


def file_added(file_list, extension):
    """Checks if a file is added in directory"""
    global files
    for f in file_list:
        if f.endswith(extension) and f not in files:
            files[f] = 0
            logger.info(f"{f} added to directory.")
    return file_list


def file_deleted(file_list):
    """Checks if file deleted in directory."""
    global files
    for f in list(files):
        if f not in file_list:
            logger.info(f"{f} deleted from directory")
            del files[f]
    return file_list


def watch_directory(path, magic_string, extension, interval):
    """Watches a selected directory for any added/deleted files"""
    file_list = os.listdir(path)
    file_added(file_list, extension)
    file_deleted(file_list)
    for f in files:
        path = os.path.join(path, f)
        files[f] = search_for_magic(path, files[f], magic_string)


def create_parser():
    """An argument parser object"""
    parser = argparse.ArgumentParser(
        description="Watch a directory for files with a magic string."
    )
    parser.add_argument('-e', '--extension', type=str, default='.txt',
                        help='The watched file extension.')
    parser.add_argument('-i', '--interval', type=float, default=1.0,
                        help='The number of seconds between the interval.')
    parser.add_argument('directory', help='The watched directory.')
    parser.add_argument('magic_string', help='The watched magic string.')
    return parser


def signal_handler(sig_num, frame):
    """
    This is a handler for SIGTERM and SIGINT.
    Other signals can be mapped here as well (SIGHUP?)
    Basically, it just sets a global flag,
    and main() will exit its loop if the signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """
    # log the associated signal name
    logger.warning('Received ' + signal.Signals(sig_num).name)
    global exit_flag
    exit_flag = True


def main(args):
    """Main function"""
    parser = create_parser()
    parsed_args = parser.parse_args(args)

    polling_interval = parsed_args.interval

    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d %(name)-12s '
               '%(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d &%H:%M:%S'
    )
    logger.setLevel(logging.DEBUG)

    # Start Logging
    start_time = time.time()
    logger.info(
        "\n"
        "-------------------------------------------------------------------\n"
        f"      Running: {__file__}\n"
        f"      PID: {os.getpid()}\n"
        f"      Started at {start_time}\n"
        "-------------------------------------------------------------------\n"
    )

    # Hook into these two signals from the OS
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends
    # either of these to my process.

    while not exit_flag:
        try:
            watch_directory(
                parsed_args.directory,
                parsed_args.magic_string,
                parsed_args.extension,
                parsed_args.interval)
        except OSError as e:
            if e.errno == errno.ENOENT:
                logger.error(
                    f"The directory {parsed_args.directory} cannot be found.")
                time.sleep(1)
        except Exception as e:
            # This is an UNHANDLED exception
            # Log an ERROR level message here
            logger.error(f"Unhandled exception: {e}")

        # put a sleep inside my while loop so I don't peg the cpu usage at 100%
        time.sleep(polling_interval)
    # final exit point happens here
    # Log a message that we are shutting down
    uptime = time.time() - start_time
    logger.info(
        "\n"
        "-------------------------------------------------------------------\n"
        f"       Stopped: {__file__}\n"
        f"       Uptime: {uptime:.2F}\n"
        "-------------------------------------------------------------------\n"
    )
    logging.shutdown()
    # Include the overall uptime since program start


if __name__ == '__main__':
    main(sys.argv[1:])
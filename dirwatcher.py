#!/usr/bin/env python3
"""
Dirwatcher - A long-running program
Given a directory, file extension, and a string of text to search for,
this program will continually monitor the directory for files with the
given extension, and log every line of those files that contain the
specified "magic text". Files added to, or removed from the given directory
will be logged accordingly.
"""

__author__ = "Reginald Jefferson"

import sys
import os
import signal
import argparse
import logging
import time
import re
import textwrap

# creates flag to allow for program termination
exit_flag = False

# creates and formats logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s %(name)s\t%(levelname)s\n[%(threadName)s  ] %(message)s"
)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# creates dict of files: line_count watched in memory
watched_files = {}


def detect_added_files(files):
    """
    Searches for new files with the given extension in the target directory.
    Syncs them to memory to maintain an updated reference to all known files.
    """
    global watched_files
    for f in files:
        if f not in watched_files or watched_files[f] == -1:
            logger.info(f"Adding {f} to watchlist")
            watched_files[f] = 0


def detect_removed_files(files):
    """
    Compares files referenced in local memory with those currently in the
    target directory, to determine if any previously known files have been
    removed from the directory.
    """
    global watched_files
    for f in watched_files:
        if f not in files and watched_files[f] != -1:
            logger.info(f"Removing {f} from watchlist")
            watched_files[f] = -1


def search_for_magic(file, lines, start_line, magic_string):
    """
    Scans new lines in target files for the existence of "magic text".
    """
    for i, line in enumerate(lines[start_line:]):
        if re.search(magic_string, line):
            # adds 1 to output line number to account for 0 based indexing
            logger.info(f"{magic_string} found on line {start_line + i + 1} of {file}")


def watch_directory(path, magic_string, extension):
    """
    Controller function.
    Scans files in target directory, calls functions to monitor new and removed
    files, calls function to look for "magic text" if target files have been
    updated. Updates local memory's reference to last known line where
    "magic text" can be found in each file.
    Logs warning if target directory does not exist.
    """
    global watched_files

    if os.path.exists(path):
        current_files = [f for f in os.listdir(path) if f.endswith(extension)]
        detect_added_files(current_files)
        detect_removed_files(current_files)
        for file in current_files:
            with open(os.path.join(path, file)) as f:
                lines = f.readlines()
                f.close()
            number_of_lines = len(lines)
            # checks to see if files have been added to
            if watched_files[file] < number_of_lines:
                search_for_magic(file, lines, watched_files[file], magic_string)
                watched_files[file] = number_of_lines
    else:
        logger.warning(f"directory {path} does not exist")
    return


def validate_ext(parser, ext):
    """
    Guards against impossible file extensions
    """
    if not re.match(r"^\.[\w|\d]+$\S*", ext):
        parser.error("extension format is invalid")


def create_parser(args):
    """
    Creates parser to handle command line arguments.
    Provides help text to end user through CLI
    """
    parser = argparse.ArgumentParser()
    parser.formatter_class = argparse.RawDescriptionHelpFormatter
    parser.add_argument("dir", help="the directory to watch")
    parser.add_argument(
        "--int",
        type=float,
        default=1.0,
        help="""how often to scan the directory, in seconds.
                        Defaults to 1.0""",
    )
    parser.add_argument(
        "ext",
        help="""extension for the type of files to be
                        monitored for "magic text" (i.e., .txt, .log, .doc)""",
    )
    parser.add_argument("magic", help='the "magic text" to search for')
    parser.epilog = """To exit this program, send either a SIGTERM or SIGINT signal.
        HINT: ctrl + C"""
    ns = parser.parse_args(args)
    validate_ext(parser, ns.ext)
    return ns


def signal_handler(sig_num, frame):
    """
    This is a handler for SIGTERM and SIGINT.
    Other signals can be mapped here as well (SIGHUP?)
    sets a global flag,
    and main() will exit its loop if the signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """
    global exit_flag
    sig_name = signal.Signals(sig_num).name

    # log the associated signal name
    logger.warning("Received " + sig_name)
    if sig_name == "SIGTERM" or sig_name == "SIGINT":
        logger.info("Exiting")
        exit_flag = True


def main(args):
    """
    Plucks input from command line parser.
    Writes banners to beginning and end of logs.
    Polls target directory for updates every :param polling_interval: seconds
    """

    # Hook into these two signals from the OS
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends
    # either of these to my process.

    ns = create_parser(args)
    path = os.path.abspath(os.path.join(os.getcwd(), ns.dir))
    polling_interval = ns.int
    ext = ns.ext
    magic = ns.magic

    global exit_flag

    logger.info(
        "\n"
        "-------------------------------------------------------------------\n"
        "Beginning dirwatcher.py\n"
        f"searching for {magic} in {textwrap.fill(path, 44)}\n"
        "-------------------------------------------------------------------"
    )

    while not exit_flag:
        try:
            watch_directory(path, magic, ext)
        except Exception as e:
            # This is an UNHANDLED exception
            # Logs an ERROR level message here
            logger.error(e)
            # Raises SIGTERM to exit program
            signal.raise_signal(signal.SIGTERM)

        # put a sleep inside my while loop so I don't peg the cpu usage at 100%
        time.sleep(polling_interval)

    # final exit point happens here
    # Logs a message that we are shutting down
    # Includes the overall uptime since program start
    runtime = time.perf_counter()
    S = runtime
    M = int(runtime) // 60
    H = M // 60
    logger.info(
        "\n"
        "-------------------------------------------------------------------\n"
        "Stopped dirwatcher.py\n"
        f"Uptime was {H:02d}:{M:02d}:"
        f"{S % 60 if S > 60 else S if S / 10 >= 1 else '0' + str(S)}\n"
        "-------------------------------------------------------------------\n"
    )


if __name__ == "__main__":
    main(sys.argv[1:])
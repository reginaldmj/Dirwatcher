<img height="120" src="img/DeerWatcher.jpg" />

# Dirwatcher

### Objectives
 - Create a long-running program
 - Demonstrate OS signal handling (SIGTERM, SIGINT)
 - Demonstrate program logging
 - Use exception handling to keep the program running
 - Structure your code repository using best practices
 - Read a set of requirements and deliver on them, asking for clarification if anything is unclear

### Goal
For this assessment, you will gain experience with structuring a long-running program by creating your own, called `dirwatcher.py`. The `dirwatcher.py` program should accept some command line arguments that will instruct it to monitor a given directory for text files that are created within the monitored directory. Your `dirwatcher.py` program will continually search within all files in the directory for a "magic string", which is provided as a command line argument. This can be implemented with a timed polling loop. If the magic string is found in a file, your program should log a message indicating which file, and the line number within the file where the magic text was found. Once a magic text occurrence has been logged, it should not be logged again unless it appears in the file as another subsequent line entry later on. Don't worry about reporting multiple occurrences of the magic string in a single line.

Files in the monitored directory may be added, deleted, or appended at any time by other processes. Your program should log a message when new files appear or other previously-watched files disappear. _Assume that files will only be changed by appending to them._ That is, anything that has previously been written to a file will not change. Only new content will be added to the end of the file, so you won't have to continually re-check sections of a file that you have already checked.

Your program should terminate itself when catching SIGTERM or SIGINT signals (be sure to log a termination message). The OS will send a signal event to processes that it wants to terminate from the outside, but your program will only act on those signals if it is listening for them. Think about when a system administrator wants to shutdown the entire computer for maintenance with a `sudo shutdown` command. If your process has open file handles, is writing to disk, or is managing other resources, this is the OS's way of telling your program that you need to clean up. Finish any writes in progress, and release resources before shutting down.

**NOTE**: Handling OS signals and polling the directory that is being watched will be two separate functions of your program. You won't be getting an OS signal when files are created or deleted.

### Success Criteria
 - Use all best practices that have been taught so far: docstrings, PEP8, clean and readable code, and meaningful commit messages
 - Have a demonstrable OS signal handler
 - Log messages for files containing "magic text"
 - Handle and log different exceptions such as "file not found", "directory does not exist", as well as handle and report top-level unknown exceptions so that your program stays alive
 - Include a startup and shutdown banner in your logs and report the total runtime (uptime) within your shutdown log banner (please see the hints below if you don't understand what a logging banner is)
 - **Read the rubric!**

### Hints
```python
import signal
import time

exit_flag = False


def signal_handler(sig_num, frame):
    """
    This is a handler for SIGTERM and SIGINT. Other signals can be mapped here as well (SIGHUP?)
    Basically, it just sets a global flag, and main() will exit its loop if the signal is trapped.
    :param sig_num: The integer signal number that was trapped from the OS.
    :param frame: Not used
    :return None
    """
    # log the associated signal name
    logger.warn('Received ' + signal.Signals(sig_num).name)


def main():
    # Hook into these two signals from the OS
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    # Now my signal_handler will get called if OS sends
    # either of these to my process.

    while not exit_flag:
        try:
            # call my directory watching function
            pass
        except Exception as e:
            # This is an UNHANDLED exception
            # Log an ERROR level message here
            pass

        # put a sleep inside my while loop so I don't peg the cpu usage at 100%
        time.sleep(polling_interval)

    # final exit point happens here
    # Log a message that we are shutting down
    # Include the overall uptime since program start
```

### More hints
Create a versatile command line argument parser that can handle these options:

 - An argument that controls the polling interval (instead of hard-coding it)
 - An argument that specifics the "magic text" to search for
 - An argument that filters what kind of file extension to search within (i.e., `.txt`, `.log`)
 - An argument to specify the directory to watch (*this directory may not yet exist!*)

### DOs and DON'Ts
**Don't** use a strategy where you are counting the number of files in the directory and then reporting files added or deleted if the count increases or decreases.
 - *Why Not?* &mdash; Well, what if your polling interval is long, and one file gets replaced by another with a different name? The file count will still be the same, but you will miss tracking the new file.

**Do** use a strategy of modeling the contents of the directory within your program using a dictionary. The keys will be filenames and the values will be the last line number that was read during the previous polling iteration. Keep track of the last line read. When opening and reading the file, skip over all the lines that you have previously examined.

**Do** synchronize your dictionary model with the actual directory contents. A sync must do these things:

1. For every file in the directory, add it to your dictionary if it is not already there (exclude files without proper extensions). Report new files that are added to your dictionary.
1. For every entry in your dictionary, find out if it still exists in the directory. If not, remove it from your dictionary and report it as deleted.
1. Once you have synchronized your dictionary, it is time to iterate through all of its files and look for magic text, starting from the line number where you left off last time.

**Don't** structure your program as one big monolithic function.

**Do** break up your code into small functions such as `scan_single_file()`, `detect_added_files()`, `detect_removed_files()`, and `watch_directory()`.

**Do** **Read the attached Rubric as your key to maximizing points**! Many students will submit their projects without reading the rubric points. Don't be *that* person.


### Testing the Program
Test your Dirwatcher program using **two** terminal windows. In the first window, start your Dirwatcher with various sets of command line arguments. Open a second terminal window and navigate to the same directory where your Dirwatcher is running and try the following:

 - Run Dirwatcher with non-existent directory &mdash; At each polling interval, it should complain about the missing watch directory.
 - Create the watched directory with `mkdir` &mdash; Dirwatcher should stop complaining.
 - Add an empty file with a target extension to the watched directory &mdash; Dirwatcher should report a new file added.
 - Append some magic text to the first line of the empty file &mdash; Dirwatcher should report that some magic text was found on line 1, only once.
 - Append a few other non-magic text lines to the file and then another line with two or more magic texts &mdash; Dirwatcher should correctly report the line number just once (don't report previous line numbers).
 - Add a file with a non-magic extension and some magic text &mdash; Dirwatcher should not report anything.
 - Delete the file containing the magic text &mdash; Dirwatcher should report the file as removed, only once.
 - Remove entire watched directory -- Dirwatcher should revert to complaining about a missing watch directory, at each polling interval.

### Testing the Signal Handler
To test the OS signal handler part of your Dirwatcher, send a SIGTERM to your program from a separate terminal window.

1. While your Dirwatcher is running, open a new terminal.
1. Find the process id (PID) of your Dirwatcher. PID is the first column listed from the `ps` command line utility.
1. Send a SIGTERM to your Dirwatcher.
1. Your signal handler within your Python program should be called. Your code should exit gracefully with a Goodbye message.

*Example*: How to shutdown your program
```console
% ps aux | grep dirwatcher.py
48885 ttys000    0:00.80 python dirwatcher.py
49388 ttys002    0:00.00 grep dirwatcher.py
% kill -s SIGTERM 48885
```

*Example*:  How to log a shutdown from within your program 
```
2018-08-31 11:36:29.510 __main__     WARNING  [MainThread  ] Received SIGTERM
2018-08-31 11:36:29.834 __main__     INFO     [MainThread  ] 
-------------------------------------------------------------------
   Stopped dirwatcher.py
   Uptime was 0:33:39.316367
-------------------------------------------------------------------
```
### How robust is your exception handler?
Will your long-running program fail if the directory under watch is suddenly deleted? If your watcher is pointed at another program's logging directory (which may come or go under different circumstances), you may want to add an exception handler and do some longer-duration retries instead of bailing out. Perhaps you could retry the directory every 5 seconds. Once you have a valid directory, you could do the file polling every 1 second. This would require an outer loop and an inner loop.

### Credits
This assignment was inspired by the story of [The Cuckoo's Egg](https://en.wikipedia.org/wiki/The_Cuckoo%27s_Egg).

## Submitting your work
To submit your solution for grading, you will need to create a github [Pull Request (PR)](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests).  Refer to the `PR Workflow` article in your course content for details.

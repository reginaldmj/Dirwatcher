A long running program that will monitor a specified directory for changes to any files of a type specified by the end user. Determines if any instances of a user-specified string (aka "magic text") appear in the files being watched, and logs their location.

Install Python 3.9 or higher

Usage

python dirwatcher.py [dir] .[ext] [magic_text]

Example Usage

python dirwatcher.py ./test .txt hello

Example Output

2024-03-22 11:48:59,495 __main__	INFO
[MainThread  ]
-------------------------------------------------------------------
Beginning dirwatcher.py
searching for hello in /Users/reggie/dirwatcher/test
-------------------------------------------------------------------
2021-03-22 11:48:59,495 __main__	INFO
[MainThread  ] Adding test.txt to watchlist
2021-03-22 11:48:59,496 __main__	INFO
[MainThread  ] hello found on line 1 of test.txt
2021-03-22 11:48:59,496 __main__	INFO
[MainThread  ] hello found on line 2 of test.txt
2021-03-22 11:48:59,496 __main__	INFO
[MainThread  ] hello found on line 3 of test.txt
2021-03-22 11:48:59,496 __main__	INFO
[MainThread  ] hello found on line 5 of test.txt
^C2021-03-22 11:50:02,501 __main__	WARNING
[MainThread  ] Received SIGINT
2021-03-22 11:50:02,502 __main__	INFO
[MainThread  ] Exiting
2021-03-22 11:50:02,730 __main__	INFO
[MainThread  ]
-------------------------------------------------------------------
Stopped dirwatcher.py
Uptime was 00:01:3.2699471159999973
-------------------------------------------------------------------

Need Help?

python dirwatcher.py -h

OR

python dirwatcher.py --help


Author

Reginald Jefferson
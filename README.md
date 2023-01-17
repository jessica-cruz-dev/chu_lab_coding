# Coding problems for the Chu lab
Three coding problems pertinent to the Chu research lab at the University of Washington


Table of contents
=================

<!--ts-->
   * [Problem 1](#problem-1)
   * [Problem 2](#problem-2)
   * [Problem 3](#problem-3)
<!--te-->


Problem 1
============
**The combined set of cron expressions in the text file will launch a php job once
per month, at 8 AM on the first weekday occurring on or after the 15th
calendar day of each month.**

Assumption: /bin/php is where php is located on the machine launching the cron jobs.

```
cron_jobs.txt
```


Problem 2
============
**A script that 1) updates a JSON input file by appending a new set of randomly
generated identifiers, 2) prints only the new identifiers to the output.**

NOTE: I used argparse to make the command line arguments more identifiable. If you
want to run the script without having to specify the argparse options, you can switch
to the ***without_argparse*** branch and run this script there.

Example call:
```
python generate_ids.py --identifier-set-file identifier_set.json --new-identifiers-quantity 5
```


Problem 3
================
**A script that identifies all adult (18 years or older) participants with a
'positive' (virus detected) result dated within the past 30 days, and reports
out their age, most recent test result, and most recent test date.**

NOTE: I used argparse to make the command line arguments more identifiable. If you
want to run the script without having to specify the argparse options, you can switch
to the ***without_argparse*** branch and run this script there.

Example call:
```
python positive_adults.py --participant-file participants.json --results-file results.json
```

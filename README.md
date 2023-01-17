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

Example call:
```
python generate_ids.py identifier_set.json 5
```


Problem 3
================
**A script that identifies all adult (18 years or older) participants with a
'positive' (virus detected) result dated within the past 30 days, and reports
out their age, most recent test result, and most recent test date.**

Example call:
```
python positive_adults.py participants.json results.json
```

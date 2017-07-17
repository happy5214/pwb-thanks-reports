pwb-thanks-reports: A Pywikibot thanks report script
====================================================

This repository contains a Pywikibot script (/scripts/thanks_report.py) that
can be used to generate reports on the givers and recipients of thanking
actions on a particular wiki. You can generate reports by month, selecting
a minumum number of actions for each user to be included in the report.

The script takes three custom arguments, in addition to the standard Pywikibot
arguments for selecting a wiki:

- year and month: Used together to select a month for which to generate reports. Defaults to the current month.
- minimum: The minumum number of actions required for inclusion in the tables. Defaults to 1.

The tables contain three columns: a numerical index (tied users have the same
number), a link to that user's CentralAuth page, and the number of associated
actions for that user.

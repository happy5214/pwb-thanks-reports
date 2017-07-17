#!/usr/bin/python
# -*- coding: utf-8 -*-
"""Create reports for thankers and thankees by wiki and month.

These are the specific command line parameters for this script:

&params;

-minimum          The minimum number of thanks actions needed for inclusion.

-year             The year for which to generate the report.
-month            The month for which to generate the report (as a number).
"""
#
# (C) Alexander Jones, 2017
#
# Distributed under the terms of the MIT license.
#
from __future__ import absolute_import, unicode_literals

from collections import Counter
import datetime

import pywikibot

from tabulate import tabulate


class ThanksReportBot(object):

    """Bot class used to implement reports for thankers and thankees."""

    def __init__(self, minimum_actions, year, month):
        """Constructor.

        @param minimum_actions: The minimum numbers of actions (sending or
        receiving) needed for inclusion in the report.
        @type minimum_actions: int
        """
        self.site = pywikibot.Site()
        self.minimum_actions = minimum_actions
        self.year = year
        self.month = month

    def run(self):
        """Run the bot."""
        data = self.gather()
        month = datetime.date(self.year, self.month, 1)
        month_str = month.strftime('%B %Y')
        print "Thank givers for {}".format(month_str)
        self.format(data[0])
        print
        print "Thank recipients for {}".format(month_str)
        self.format(data[1])

    def gather(self):
        """Gather and parse the log data."""
        thankers = []
        thankees = []

        start_time = datetime.datetime(self.year, self.month, 1)
        end_time = datetime.datetime(self.year, self.month + 1, 1)
        for entry in self.site.logevents(logtype='thanks', start=end_time,
                                         end=start_time):
            thankers.append(entry.user())
            thankees.append(entry.page())
        thankers_count = Counter(thankers)
        thankees_count = Counter(thankees)

        included_thankers = []
        included_thankees = []
        for k,v in thankers_count.iteritems():
            if v >= self.minimum_actions:
                included_thankers.append((-v,k))
        for k,v in thankees_count.iteritems():
            if v >= self.minimum_actions:
                included_thankees.append((-v,k))
        included_thankers.sort()
        included_thankees.sort()
        return (included_thankers, included_thankees)

    def format(self, data):
        """Format the parsed data."""
        index = 1
        same = 0
        last_count = data[0][0] + 1
        rows = []
        for entry in data:
            count = entry[0]
            if count != last_count:
                index += same
                same = 1
            else:
                same += 1
            user = entry[1]
            if isinstance(user, pywikibot.User):
                user = user.username
            user_link = '[[Special:CentralAuth/{}]]'.format(user)
            rows.append([index, user_link, -count])
            last_count = count
        print tabulate(rows, ['#', 'User', 'Thanks'], tablefmt='mediawiki')


def main(*args):
    """
    Process command line arguments and invoke bot.

    If args is an empty list, sys.argv is used.

    @param args: command line arguments
    @type args: list of unicode
    """
    local_args = pywikibot.handle_args(args)
    minimum_actions = 1
    today = datetime.date.today()
    year = today.year
    month = today.month

    # Parse command line arguments
    for arg in local_args:
        option, sep, value = arg.partition(':')
        if option == '-minimum':
            minimum_actions = int(value)
        elif option == '-year':
            year = int(value)
        elif option == '-month':
            month = int(value)
        else:
            pywikibot.warning(
                u'argument "%s" not understood; ignoring.' % arg)

    bot = ThanksReportBot(minimum_actions, year, month)
    bot.run()


if __name__ == "__main__":
    main()

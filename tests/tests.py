# -*- coding: utf-8 -*-
"""Tests for thanks reporting bot code."""
#
# (C) Alexander Jones, 2017
#
# Distributed under the terms of the MIT license.
#
from __future__ import absolute_import, unicode_literals

import pywikibot
from pywikibot import User

from scripts.thanks_report import ThanksReportBot

from unittest.case import TestCase


class TestThanksReportBot(TestCase):

    """Base class for per-wiki test classes."""

    def _thanks_for_month(self, year, month, good_data, min_actions=1):
        """Test the thanks report for a given month."""
        bot = ThanksReportBot(year=year, month=month,
                              minimum_actions=min_actions)
        bot.site = pywikibot.Site(fam=self.family, code=self.code)
        (good_thankers, good_thankees_with_strings) = good_data
        good_thankees = {}
        for k,v in good_thankees_with_strings.items():
            good_thankees[User(bot.site, k)] = v
        (pulled_thankers, pulled_thankees) = bot.gather()
        self.assertDictContainsSubset(good_thankers, pulled_thankers,
                                      'Bad thankers report')
        self.assertDictContainsSubset(good_thankees, pulled_thankees,
                                      'Bad thankees report')


class TestOutreachThanks(TestThanksReportBot):

    """Test the thanks report with outreach."""

    family = 'outreach'
    code = 'outreach'

    def test_August2016(self):
        """Test on outreach using data from August 2016."""
        good_data = [
            {'Romaine': 20, 'Msannakoval': 13, 'Joalpe': 3, 'TFlanagan-WMF': 3,
             'Masssly': 3, 'PetrohsW': 2, 'Halibutt': 2, 'VIGNERON': 1,
             'MCruz (WMF)': 1, 'Slowking4': 1},
            {'Loreen.Ruiz': 5, 'Koavf': 4, 'Msannakoval': 3, 'Andycyca': 3,
             'Sadads': 2, 'Léna': 2, 'AKoval (WMF)': 2, 'Masssly': 2,
             'Pigsonthewing': 1, 'Ijon': 1}
        ]
        self._thanks_for_month(2016, 8, good_data, 1)

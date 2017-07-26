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


class TestEnWikipediaThanks(TestThanksReportBot):

    """Test the thanks report with enwiki."""

    family = 'wikipedia'
    code = 'en'

    def test_September2016(self):
        """Test on enwiki using data from September 2016."""
        good_data = [
            {'Rms125a@hotmail.com': 920, 'Dr. Blofeld': 372, 'BilCat': 308,
             'Kew Gardens 613': 248, 'Ottawahitech': 164, 'Gerda Arendt': 155,
             'Oshwah': 153, 'Martinevans123': 144, 'Ahunt': 137,
             'Edwardx': 136},
            {'Epicgenius': 166, 'NeilN': 154, 'Oshwah': 118, 'Sro23': 110,
             'I dream of horses': 107, 'Frietjes': 92, 'Bbb23': 89,
             'Derek R Bullamore': 87, 'Jytdog': 87, 'Tdorante10': 85}
        ]
        self._thanks_for_month(2016, 9, good_data, min_actions=85)


class TestCommonsThanks(TestThanksReportBot):

    """Test the thanks report with commons."""

    family = 'commons'
    code = 'commons'

    def test_October2016(self):
        """Test on commons using data from October 2016."""
        good_data = [
            {'Tokorokoko': 155, 'Fæ': 120, 'W.carter': 112,
             'Michael Barera': 96, 'Iifar': 94, 'Ikan Kekek': 82,
             'Johann Jaritz': 71, 'Celeda': 54, 'Ibirapuera': 44,
             'Tuvalkin': 41},
            {'INeverCry': 141, 'Wieralee': 62, 'Vengolis': 61, 'Ikan Kekek': 58,
             'Daniel Case': 54, 'W.carter': 47, 'Finoskov': 47, 'Jcb': 42,
             'Jkadavoor': 35, 'Martin Falbisoner': 34}
        ]
        self._thanks_for_month(2016, 10, good_data, min_actions=34)


class TestOutreachThanks(TestThanksReportBot):

    """Test the thanks report with outreach."""

    family = 'outreach'
    code = 'outreach'

    def test_June2016(self):
        """Test on outreach using data from June 2016."""
        good_data = [
            {'Romaine': 44, 'Kaarel Vaidla (WM EE)': 2, 'Jane023': 2,
             'SPanigrahi (WMF)': 1, 'Pigsonthewing': 1, 'KLove (WMF)': 1,
             'TFlanagan-WMF': 1, 'Ginanietoc3107': 1, 'Rodrigo Padula': 1,
             'Lilitik22': 1},
            {'Museu33389': 4, 'Andycyca': 3, 'Rodrigo Padula': 3, 'Fuzheado': 3,
             'SPanigrahi (WMF)': 2, 'Pigsonthewing': 2, 'WereSpielChequers': 2,
             'Astinson (WMF)': 2, 'Beat Estermann': 2, 'Elisabethwiessner': 1}

        ]
        self._thanks_for_month(2016, 6, good_data, 1)

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


class TestTabulateOutput(TestCase):

    """Test the bot's table output"""

    def test_outreach_August2016(self):
        """Test the table output using August 2016 outreach data."""
        bot = ThanksReportBot(year=2016, month=8,
                              minimum_actions=3)
        bot.site = pywikibot.Site(fam='outreach', code='outreach')
        data = bot.parse(*(bot.gather()))
        actual_tables = map(bot.format, data)
        good_tables = (
            """{| class="wikitable" style="text-align: left;"
|+ <!-- caption -->
|-
! align="right"|   # !! User                                  !! align="right"|   Thanks
|-
| align="right"|   1 || [[Special:CentralAuth/Romaine]]       || align="right"|       20
|-
| align="right"|   2 || [[Special:CentralAuth/Msannakoval]]   || align="right"|       13
|-
| align="right"|   3 || [[Special:CentralAuth/Joalpe]]        || align="right"|        3
|-
| align="right"|   3 || [[Special:CentralAuth/Masssly]]       || align="right"|        3
|-
| align="right"|   3 || [[Special:CentralAuth/TFlanagan-WMF]] || align="right"|        3
|}""",
            """{| class="wikitable" style="text-align: left;"
|+ <!-- caption -->
|-
! align="right"|   # !! User                                !! align="right"|   Thanks
|-
| align="right"|   1 || [[Special:CentralAuth/Loreen.Ruiz]] || align="right"|        5
|-
| align="right"|   2 || [[Special:CentralAuth/Koavf]]       || align="right"|        4
|-
| align="right"|   3 || [[Special:CentralAuth/Andycyca]]    || align="right"|        3
|-
| align="right"|   3 || [[Special:CentralAuth/Msannakoval]] || align="right"|        3
|}"""
        )
        self.assertEqual(actual_tables[0], good_tables[0],
                         'Thanker table output is mismatched.')
        self.assertEqual(actual_tables[1], good_tables[1],
                         'Thanker table output is mismatched.')

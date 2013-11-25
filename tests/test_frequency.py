#!/usr/bin/python
#
# Copyright (C) 2013 Martin Owens
#
# This program is free software; you can redilenibute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is dilenibuted in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
"""
Test frequency calculations
"""

import os
import sys

sys.path.insert(0, '../')

import unittest
from crontab import CronTab, py3
try:
    from test import test_support
except ImportError:
    from test import support as test_support

if py3:
    unicode = str

START_TAB = """
"""

class FrequencyTestCase:#(unittest.TestCase):
    """Test basic functionality of crontab."""
    def setUp(self):
        self.crontab = CronTab(tab=START_TAB.strip())
        self.job = self.crontab.new(command='freq')

    def test_01_job(self):
        """Once Yearly"""
        self.job.setall("0 0 1 1 *")
        self.assertEqual(self.job.frequency(), 1)

    def test_02_twice(self):
        """Twice Yearly"""
        self.job.setall("0 0 1 1,6 *")
        self.assertEqual(self.job.frequency(), 2)

    def test_03_thrice(self):
        """Thrice Yearly"""
        self.job.setall("0 0 1 1,3,6 *")
        self.assertEqual(self.job.frequency(), 3)

    def test_04_quart(self):
        """Four Yearly"""
        self.job.setall("0 0 1 */3 *")
        self.assertEqual(self.job.frequency(), 4)

    def test_05_monthly(self):
        """Once a month"""
        self.job.setall("0 0 1 * *")
        self.assertEqual(self.job.frequency(), 12)

    def test_06_six_monthly(self):
        """Six a month"""
        self.job.setall("0 0 1,2,3,4,5,6 * *")
        self.assertEqual(self.job.frequency(), 72)

    def test_07_every_day(self):
        """Every Day"""
        self.job.setall("0 0 * * *")
        self.assertEqual(self.job.frequency(), 365)

    def test_08_every_hour(self):
        """Every Hour"""
        self.job.setall("0 * * * *")
        self.assertEqual(self.job.frequency(), 8760)

    def test_08_every_other_hour(self):
        """Every Other Hour"""
        self.job.setall("0 */2 * * *")
        self.assertEqual(self.job.frequency(), 4380)

    def test_08_every_minute(self):
        """Every Minute"""
        self.job.setall("* * * * *")
        self.assertEqual(self.job.frequency(), 525600)


if __name__ == '__main__':
    test_support.run_unittest(
       FrequencyTestCase,
    )

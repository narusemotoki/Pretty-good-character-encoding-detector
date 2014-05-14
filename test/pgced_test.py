#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import unittest
import pgced


def u(text):
    return text.decode('utf-8')


class PgcedTest(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.resource_path = 'test/resource'
        self.pgced = pgced.Pgced()

    def _testDetectFile(self, f):
        return self.pgced.detectOne({
            'target_type': 'file',
            'uri': '{0}/{1}'.format(self.resource_path, f),
        })

    def testDetectAsciiFile(self):
        t = self._testDetectFile('ascii')
        self.assertEqual(t['encoding'], 'ascii')
        self.assertEqual(u(t['converted']).strip(), u'This is a ascii encoding file.')

    def testDetectUtf8File(self):
        t = self._testDetectFile('utf8')
        self.assertEqual(t['encoding'], 'utf-8')
        self.assertEqual(u(t['converted']).strip(), u'これはUTF8でエンコードされたファイル')

    def testDetectEucjpFile(self):
        t = self._testDetectFile('eucjp')
        self.assertEqual(t['encoding'], 'EUC-JP')
        self.assertEqual(u(t['converted']).strip(), u'これはEUC-JPでエンコードされたファイル')

    def testDetectShiftjisFile(self):
        t = self._testDetectFile('shiftjis')
        self.assertEqual(t['encoding'], 'SHIFT_JIS')
        self.assertEqual(u(t['converted']).strip(), u'これはSHIFT-JISでエンコードされたファイル')

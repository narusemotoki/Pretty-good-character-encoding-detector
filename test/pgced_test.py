#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
import pgced


class PgcedTest(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.setUp(self)
        self.resource_path = 'test/resource'
        self.pgced = pgced.Pgced()

    def _testDetectFile(self, f):
        return self.pgced.detectOne({
            'type': 'file',
            'uri': '{0}/{1}'.format(self.resource_path, f),
        })

    def testDetectAsciiFile(self):
        t = self._testDetectFile('ascii')
        self.assertEquals(t['encoding'], 'ascii')

    def testDetectUtf8File(self):
        t = self._testDetectFile('utf8')
        self.assertEquals(t['encoding'], 'utf-8')

    def testDetectEucjpFile(self):
        t = self._testDetectFile('eucjp')
        self.assertEquals(t['encoding'], 'EUC-JP')

    def testDetectShiftjisFile(self):
        t = self._testDetectFile('shiftjis')
        self.assertEquals(t['encoding'], 'SHIFT_JIS')

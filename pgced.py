#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Pretty good character encoding detector
Copyright (c) 2014, Motoki Naruse <motoki@naru.se>, All rights reserved.

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 3.0 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library.
"""

from __future__ import print_function
from chardet.universaldetector import UniversalDetector
import json
import urllib
import contextlib
import sys


class Pgced(object):
    def __init__(self, include_utf8=True):
        self.detector = UniversalDetector()
        self.include_utf8 = include_utf8
        for_file = self.forFile
        for_url = self.forUrl
        self.funcs = {
            'file': for_file,
            'url': for_url,
        }

    def forFile(self, uri):
        with contextlib.closing(urllib.urlopen(uri)) as r:
            return self.detect(r.readlines)

    def forUrl(self, uri):
        with open(uri) as f:
            return self.detect(lambda: f)

    def convert(self, lines, source_encode, target_encode='utf-8'):
        return [l.decode(source_encode).encode(target_encode) for l in lines]

    def detect(self, f):
        d, conv_utf8 = self.detector, self.include_utf8
        d.reset()
        lines = []
        for l in f():
            if not d.done:
                d.feed(l)

            if conv_utf8:
                lines.append(l)

            if d.done and not conv_utf8:
                break
        d.close()

        return dict(d.result, **{
            'converted': ''.join(self.convert(lines, d.result['encoding']))
        } if conv_utf8 else {})

    def detectOne(self, source):
        return dict(self.funcs[source['target_type']](source['uri']), **source)

    def detectMulti(self, sources):
        return [self.detectOne(s) for s in sources]


if __name__ == '__main__':
    if 1 < len(sys.argv):
        results = Pgced().detectMulti(json.loads(sys.argv[1])['sources'])
        print(json.dumps({'results': results}))

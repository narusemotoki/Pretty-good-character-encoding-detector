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
    def __init__(self):
        self.detector = UniversalDetector()
        for_file = self.forFile
        for_url = self.forUrl
        self.funcs = {
            'file': for_file,
            'url': for_url,
        }

    def forFile(self, uri):
        with contextlib.closing(urllib.urlopen(uri)) as r:
            return self.detect(r.readline)

    def forUrl(self, uri):
        with open(uri) as f:
            return self.detect(lambda: f)

    def detect(self, f):
        d = self.detector
        d.reset()
        for l in f():
            d.feed(l)
            if d.done:
                break
        d.close()
        return d.result

    def detectOne(self, source):
        return dict(self.funcs[source['type']](source['uri']), **source)

    def detectMulti(self, sources):
        return [self.detectOne(s) for s in sources]


if __name__ == '__main__':
    if 1 < len(sys.argv):
        results = Pgced().detectMulti(json.loads(sys.argv[1])['sources'])
        print(json.dumps({'results': results}))

#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re

s = "thisis A     table"


for_removing = ('a', 'the')

def format_text(text, for_removing, sep="_"):
    p = r'\s?\b[{}]?\b\s+'
    print(p)
    return re.sub(p, "_", text, flags=re.IGNORECASE)

a = 'a increase a acounter a fcrtusrty'


print(format_text(a, for_removing))
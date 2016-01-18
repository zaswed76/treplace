#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import json
import codecs
import requests

SEP = "_"
EXCLUDING_WORDS = ("a", "the", "is", "it")

def get_data_api(arg):
    """

    :return: ('path', 'start_line', 'end_line', ['select_text'])
    """
    file, start_num, end_num = arg[1:4]
    select_text = arg[4:]
    if start_num != end_num:
        sys.stdout.write("you need to select only one line")
        sys.exit(1)
    if not select_text:
        sys.stdout.write("no text selected")
        sys.exit(1)
    return file, start_num, end_num, select_text


def lines_from_file(path):
    with open(path, "r", encoding=sys.stdout.encoding) as f:
        return f.readlines()

def get_line(lines, num):
    """

    :param lines:
    :param num:
    :return:
    """
    line = re.sub('\s+', " ", lines[int(num) - 1])
    return line

def decode_text(s, enc="utf-8", dec="1251"):
        return s.encode(enc).decode(dec)


def list_to_decode_line(lst, enc="utf-8", dec="1251"):
    """
    возвращает строку собранную из списка слов декодируя каждое в 1251
    :param lst:
    :return: str
    """
    if codecs.lookup(dec).name == enc:
        decode_lst = [decode_text(w, enc, dec) for w in lst]
    else:
        decode_lst = lst

    return " ".join(decode_lst)

def translate(text, from_on):
    text = text.rstrip("\n")
    url = 'https://translate.yandex.net/api/v1.5/tr.json/translate?'
    key = 'trnsl.1.1.20160118T034046Z.e27999dc29670d9f.efb20585c9571f33a2ae818e936e415a8f5ff6e6'
    r = requests.post(url, data={'key': key, 'text': text, 'lang': from_on})
    print(r.text)
    return json.loads(r.text)["text"][0]

def format_text(text, for_removing, sep="_"):
    p = r'\s*\b({})?\b\s+'.format("|".join(for_removing))
    return re.sub(p, "_", text, flags=re.IGNORECASE)

file, start_num, end_num, select_text = get_data_api(sys.argv)
lines = lines_from_file(file)
print(lines)
line = get_line(lines, start_num)
select_line_str = list_to_decode_line(select_text, enc="utf-8",
                                      dec=sys.stdout.encoding)
target = translate(select_line_str, "ru-en")
print(format_text(target, EXCLUDING_WORDS, sep=SEP))

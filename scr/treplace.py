#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from textblob import TextBlob
import re

file, num, *select_text = sys.argv[1:]




def lines_from_file(path):
    with open(path, "r", encoding='1251') as f:
        return f.readlines()


def write_lines(file, lines):
    if lines:
        with open(file, "w") as f:
            f.writelines(lines)


def get_line(lines, num):
    """

    :param lines:
    :param num:
    :return:
    """
    return lines[int(num) - 1]


def list_to_decode_line(lst):
    """
    возвращает строку собранную из списка слов декодируя каждое в 1251
    :param lst:
    :return: str
    """
    return " ".join([w.encode("utf-8").decode("1251") for w in lst])


select_line_str = list_to_decode_line(select_text)
blob = TextBlob(" ".join(select_text))
translate_text = str(blob.translate(from_lang="ru", to="en"))
lines_file = lines_from_file(file)
line_for_replace = get_line(lines_file, num)
new_line = re.sub(select_line_str, translate_text, line_for_replace)

lines_file[int(num) - 1] = new_line

write_lines(file, lines_file)

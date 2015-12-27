#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import chardet
import codecs
from textblob import TextBlob, exceptions
import re

PRINT_DEBUGGING_INFORMATION = 1
if not PRINT_DEBUGGING_INFORMATION:
    def print(*args, **kwargs):
        pass

file, start_num, end_num = sys.argv[1:4]
select_text = sys.argv[4:]
if start_num != end_num:
    sys.stdout.write("you need to select only one line")
    sys.exit(1)

if not select_text:
    sys.stdout.write("no text selected")
    sys.exit(1)

SEP = "_"
EXCLUDING_WORDS = ("a", "the", "is", "it")


def detect_coding(line, ignore_reliability=False):
    """
     определяет кодировку строки
    :param line:
    :param ignore_reliability:
    :return: str or None (если кодировка не определена достоверно)
    """
    line = line[0:200]
    source_coding = chardet.detect(line)["encoding"]
    confidence = chardet.detect(line)["confidence"]
    if ignore_reliability:
        return source_coding
    elif confidence > 0.5:
        return source_coding
    else:
        print(
            "кодировка определена не достоверно - {}".format(
                confidence))
        return None


def format_text(text, for_removing, sep="_"):
    p = r'\s*\b({})?\b\s+'.format("|".join(for_removing))
    return re.sub(p, "_", text, flags=re.IGNORECASE)


def translate_line(text):
    blob = TextBlob(" ".join(select_text))
    try:
        translate_text = str(blob.translate(to="en"))
    except exceptions.NotTranslated as i:
        sys.stdout.write("TextBlob: {}".format(i))
        sys.exit(1)
    else:
        return translate_text


def get_str_from_file(path):
    with open(path, "rb") as f:
        return f.read()


def lines_from_file(path):
    with open(path, "r", encoding=sys.stdout.encoding) as f:
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


s = get_str_from_file(file)

select_line_str = list_to_decode_line(select_text, enc="utf-8",
                                      dec=sys.stdout.encoding)

print("select_line_str", select_line_str, sep=": --> ")

translate_text = translate_line(select_line_str)
print("translate_text", translate_text, sep=": --> ")
finish_text = format_text(translate_text, EXCLUDING_WORDS, sep=SEP)
print("finish_text", finish_text, sep=": --> ")
lines_file = lines_from_file(file)
line_for_replace = get_line(lines_file, start_num)
print('line_for_replace', line_for_replace, sep=": --> ")

new_line = re.sub(select_line_str, finish_text, line_for_replace)

print("new_line", new_line, sep=": --> ")

lines_file[int(start_num) - 1] = new_line

write_lines(file, lines_file)

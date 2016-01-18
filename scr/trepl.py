#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import json
import codecs

import chardet
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

def write_lines(file, lines):
    if lines:
        with open(file, "w") as f:
            f.writelines(lines)

def detect_coding(line, ignore_reliability=False):
    """
     определяет кодировку строки
    :param line:
    :param ignore_reliability:
    :return: str or None (если кодировка не определена достоверно)
    """
    line = line[0:200]
    print(line, "!!!")
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

# получить файл, строку нач., строку кон., выделенный текст > [str, str]
file, start_num, end_num, select_text = get_data_api(sys.argv)

# получить строки файла в список
lines_lst = lines_from_file(file)

# получить строку в которой выделили
line_str = get_line(lines_lst, start_num)

# подготовленная декодированная если надо строка для перевода
_original_selected_text = list_to_decode_line(select_text, enc="utf-8",
                                              dec=sys.stdout.encoding)



# переведёнаая строка
target = translate(_original_selected_text, "ru-en")

# форматированная строка
finish_text = format_text(target, EXCLUDING_WORDS, sep=SEP)

_original_selected_text = decode_text(_original_selected_text)
print(translate(_original_selected_text, "ru-en"))
print(_original_selected_text)
new_line = re.sub(_original_selected_text, finish_text, line_str) + "\n"

lines_lst[int(start_num) - 1] = new_line



write_lines(file, lines_lst)

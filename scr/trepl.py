#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import codecs
import json
import os
import re
import sys

import requests


def arg_parse():
    parser = argparse.ArgumentParser(
            description='''
                переводит и заменяет выделенный текст;
            аргументы получает из api редактора (Pycharm)''')
    parser.add_argument("file_path", type=str,
                        help="полный путь к текущему файлу")
    parser.add_argument("start_select", type=str,
                        help="начало выделения")
    parser.add_argument("end_select", type=str,
                        help="конец выделения")
    parser.add_argument("select_text_lst", nargs='+', type=str,
                        help="список выделенных слов")
    parser.add_argument('-m', '--multi', action='store_true',
                        default=False,
                        help="если указан этот ключ то возможно выделение текста в нескольких строках")
    return parser.parse_args()


def get_conf(path):
    with open(path, "r") as obj:
        return json.load(obj)


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


def translate(yandex_key, url, text, from_on):
    text = text.rstrip("\n")
    r = requests.post(url, data={'key': yandex_key, 'text': text,
                                 'lang': from_on})
    return json.loads(r.text)["text"][0]


def format_text(text, for_removing, sep="_"):
    p = r'\s*\b({})?\b\s+'.format("|".join(for_removing))
    return re.sub(p, "_", text, flags=re.IGNORECASE)


def write_to_file(file, lst):
    if lst:
        with open(file, "w") as f:
            f.writelines(lst)


def modified_list(lst, num, old, new):
    """

    :param lst: исходный список строк
    :param num: индекс строки для замены
    :param old: выделенныи текс
    :param new: переведённый текст
    :return: изменённый список строк
    """
    line_str = get_line(lst, num)
    new_str = line_str.replace(old, new) + "\n"
    lst[int(num) - 1] = new_str
    return lst


def do_one_line_selected(start, end):
    if start != end:
        sys.stdout.write("you need to select only one line")
        sys.exit(1)


def main(translation_opt, sep, excluding_words, yandex_key, url):
    """
    получить:  файл, строку нач., строку кон., выделенный текст > [str, str]
    :return:
    """
    name_arg = arg_parse()
    file = name_arg.file_path
    num_selected_line = name_arg.start_select
    end_select = name_arg.end_select
    select_text_lst = name_arg.select_text_lst
    multi_select = name_arg.multi

    # выбрана ли одна линия
    if not multi_select:
        do_one_line_selected(num_selected_line, end_select)
    else:
        raise Exception("пока эта ветка не работет")

    select_text_str = " ".join(select_text_lst)

    translate_text = translate(yandex_key, url, select_text_str,
                               translation_opt)

    # переведённый отформатированый текст
    formatted_text = format_text(translate_text, excluding_words,
                                 sep=sep)
    # прочитать файл в список
    lst_from_file = lines_from_file(file)
    # произвести замену в списке полученном из файла
    modified_lst = modified_list(lst_from_file, num_selected_line,
                                 select_text_str, formatted_text)
    write_to_file(file, modified_lst)


if __name__ == '__main__':
    root = os.path.abspath(os.path.dirname(__file__))
    config_file = os.path.join(root, "conf.json")
    config = get_conf(config_file)
    translation_opt = config["translation_opt"]
    sep = config["sep"]
    excluding_words = config["excluding_words"]
    yandex_key = config["key"]
    url = config["url"]
    main(translation_opt, sep, excluding_words, yandex_key, url)

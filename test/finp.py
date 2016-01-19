#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse


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


print(arg_parse())

import logging.handlers
import os

import clang.cindex

slash = '\\'
current_path = os.path.abspath(os.path.dirname(__file__))


def gen_ast_by_Cdb(analysis_file, node, scope, indent):
    text = node.spelling or node.displayname
    kind = '|' + str(node.kind)[str(node.kind).index('.') + 1:]
    data = ' ' * indent + '{} {} {} {} '.format(kind, text, node.location.line, node.location.column)
    unit = str(scope + kind).replace(' ', '')
    with open('thread_test_tmp.txt', 'a') as fileWriter:
        fileWriter.write(data + '\n')

    for c in node.get_children():
        gen_ast_by_Cdb(analysis_file, c, scope + '' + kind, indent + 2)


def get_all_filename(dir_path):
    filename_list = []
    for root, dirs, files in os.walk(dir_path):
        for i in files:
            filename_list.append(root + slash + i)
    logging.info(('Under this dir -- {dir}: There are {num} files ').format(dir=dir_path, num=len(filename_list)))
    return filename_list


def filter_file_by_suffixation(dir_path, *keySuffixation):
    filename_list = get_all_filename(dir_path)
    file_contain_suffixation = []
    for file in filename_list:
        if os.path.splitext(file)[1] in tuple(keySuffixation):
            file_contain_suffixation.append(file)
    logging.info(('Under this dir -- {dir}: There are {num} files, '
                  'suffix called {key}').format(dir=dir_path, num=len(file_contain_suffixation), key=keySuffixation))
    return file_contain_suffixation
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from tqdm import tqdm

import clang.cindex

slash = '\\'

WORKER_DICT = {}
class_dict = {}
scope_dict = {}

cons_lst = []
constructor_name = ''
worker_name = ''
worker_type = ''
constructor_worker_lst = []


def gen_ast(analysis_file, node, scope, indent):
    global cons_lst, constructor_name, worker_name, worker_type
    text = node.spelling or node.displayname
    kind_spelling_element = '|' + \
                            str(node.kind)[str(node.kind).index('.') + 1:] + ':' + str(text)
    data = ' ' * indent + '{} {} {} {} '.format(
        kind_spelling_element, text, node.location.line, node.location.column)
    unit = str(scope + kind_spelling_element).replace(' ', '')

    if 'CLASS_DECL' in kind_spelling_element:
        print unit, text, node.location.line, node.location.column
        tmp = unit
    print str(node.kind)

    if ('major_worker' in str(text) or 'minor_worker' in str(
            text)) and unit.split('|')[-1].startswith('CALL_EXPR'):
        key_line = node.location.line
        print unit, node.location.line, node.location.column
        if 'CONSTRUCTOR' in unit:
            for i in unit.split('|'):
                if i.startswith('CONSTRUCTOR'):
                    constructor_name = i.split(':')[1]
                    cons_lst.append(constructor_name +
                                    '-' +
                                    text +
                                    '-' +
                                    str(node.location.line) +
                                    '-' +
                                    str(node.location.column))

    # and str(node.location.line) == 58: # and str(node.location.line) == 58:
    # # i[-2:]:
    if unit.split(
            '|')[-1].startswith('MEMBER_REF_EXPR') and node.location.line == 58:
        print unit, node.location.line, node.location.column
        # pass

    print cons_lst
    if not cons_lst:
        for i in cons_lst:
            if unit.split(
                    '|')[-1].startswith('MEMBER_REF_EXPR') and str(node.location.line) == 58:  # i[-2:]:
                print unit, node.location.line, node.location.column
    print kind_spelling_element

    # media_worker_ = utils::minor_worker("LocalPipeLineWorker");
    if str(node.kind) == 'CursorKind.CONSTRUCTOR':
        constructor_name = text
        # print constructor_name
    if constructor_name in unit and 'CALL_EXPR' in unit and 'operator=' in unit and unit.split(
            '|')[-1].startswith('MEMBER_REF_EXPR'):
        worker_name = unit.split('|')[-1].split(':')[1]
        # print worker_name
    if constructor_name in unit and 'CALL_EXPR' in unit and 'operator=' in unit and unit.split(
            '|')[-1].startswith('CALL_EXPR') and (unit.endswith('minor_worker') or unit.endswith('major_worker')):
        worker_type = unit.split('|')[-1].split(':')[1]
        constructor_worker_lst.append(
            analysis_file +
            ' :: ' +
            constructor_name +
            ' :: ' +
            worker_name +
            ' :: ' +
            worker_type)
        with open('constructor_worker_lst.txt', 'a') as fileWriter:
            fileWriter.write(
                analysis_file +
                ' :: ' +
                constructor_name +
                ' :: ' +
                worker_name +
                ' :: ' +
                worker_type +
                '\n')

    for c in node.get_children():
        gen_ast(
            analysis_file,
            c,
            scope +
            '' +
            kind_spelling_element,
            indent +
            2)


current_path = os.path.abspath(os.path.dirname(__file__))


def main():
    compilation_database_path = 'C:/Users/liqiu/Desktop/dead_lock/build/win/x64'
    tmp = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\core\video\video_local_track.cpp'
    tmp_2 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\core\media_node_factory.cpp'
    tmp_3 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\net_test\network_tester.cpp'
    tmp_4 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\core\video\video_remote_track.cpp'
    tmp_5 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\utils\thread\thread_pool.cpp'
    # try:
    #     from handle_compile_json_file import HandleCompileCommandsJsonFile
    #     FILE_LST = HandleCompileCommandsJsonFile(compilation_database_path).get_abs_file()
    # except Exception as e:
    #     e.args += ('Could not load compilation flags !!! ',)
    #     raise

    from handle_compile_json_file import HandleCompileCommandsJsonFile
    FILE_LST = HandleCompileCommandsJsonFile(
        compilation_database_path).get_abs_file()
    from gen_dependent_parameters import GenDependentParametersByCdb

    for file_item in tqdm(
            [tmp, tmp_2, tmp_3, tmp_4, tmp_5], desc="WSX", ncols=100):
        # for file_item in FILE_LST:
        args_ = GenDependentParametersByCdb(
            compilation_database_path, file_item).get_args()
        index = clang.cindex.Index.create()
        tu = index.parse(file_item, args=args_)
        os.chdir(current_path)
        root = tu.cursor
        gen_ast(file_item, root, '|' + str(root.kind)
        [str(root.kind).index('.') + 1:], 0)
    for i in constructor_worker_lst:
            print i

if __name__ == '__main__':
    main()
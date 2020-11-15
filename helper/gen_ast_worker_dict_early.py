#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging.handlers
import os

import clang.cindex

slash = '\\'

WORKER_CONSTRUCTOR_DICT = {}
class_dict = {}
scope_dict = {}
mem_dict = {}
major_minor_dict = {}


def gen_ast(analysis_file, node, scope, indent):
    global WORKER_CONSTRUCTOR_DICT, mem_dict

    text = node.spelling or node.displayname
    kind = '|' + str(node.kind)[str(node.kind).index('.') + 1:]
    data = ' ' * indent + \
           '{} {} {} {} '.format(kind, text, node.location.line, node.location.column)
    # print str(indent) + ' ' * indent + '{} {} {} {} '.format(kind, text, node.location.line, node.location.column)
    kind_unit = str(scope + kind).replace(' ', '')
    # node = '|' + node
    node_unit = str(scope + node).replace(' ', '')
    # print unit
    # print data
    # with open('gen_ast124.txt', 'a') as fileWriter:
    #         fileWriter.write(data + '\n')
    # if unit.endswith('VAR_DECL'):
    #     pass
    print node_unit

    if kind == '|CONSTRUCTOR':
        pass
        # print text, node.location.line

    if 'major_worker' in str(text) or 'minor_worker' in str(text):
        major_minor_dict[text] = node.location.line

    if kind == '|MEMBER_REF_EXPR':
        mem_dict[text] = (node.location.line, node.location.column)
        # print text, node.location.line
    #
    #     # WORKER_CONSTRUCTOR_DICT[text] = node.location.line
    #     # print WORKER_CONSTRUCTOR_DICT
    #     # tmp = text
    #     # if 'MEMBER_REF_EXPR' in unit:
    #     #     # print 222
    #     #     # member_ref_expr_displayname = text
    #     #     mem_dict[text] = node.location.line
    #     #     #if 'major_worker' in str(text) or 'minor_worker' in str(text):
    #
    #
    #     # print unit, text, node.location.line, node.location.column

    # if 'MEMBER_REF_EXPR' in kind:
    #     member_ref_expr_displayname = text
    #
    # if 'major_worker' in str(text) or 'minor_worker' in str(text):
    #
    #     worker_line = node.location.line
    #     worker_displayname = text

    # print unit, text, node.location.line, node.location.column
    # print str(indent) + ' ' * indent + '{} {} {} {} {}'.format(kind, text, node.location.line, node.location.column,
    #                                                            analysis_file)
    # WORKER_DICT[tmp] = unit

    # if node.location ==

    # if 'media_worker_' in str(text):
    #     # pass
    #     print unit, text, node.location.line, node.location.column

    # if 'major_worker' in str(text) or 'minor_worker' in str(text):
    #     with open('worker_thread.txt', 'a') as fileWriter:
    #         fileWriter.write(data + '--' + analysis_file + '\n')
    #     print str(indent) + ' ' * indent + '{} {} {} {} {}'.format(kind, text, node.location.line, node.location.column,
    #                                                                analysis_file)

    # if unit.endswith('major_worker'):
    #     print unit
    # with open('python_gen_ast.txt', 'a') as fileWriter:
    #     fileWriter.write(str(indent) + str(data) + '\n')
    for c in node.get_children():
        gen_ast(analysis_file, c + '' + scope + '' + kind, indent + 2)


# print WORKER_CONSTRUCTOR_DICT
# print mem_dict


def get_all_filename(dir_path):
    filename_list = []
    for root, dirs, files in os.walk(dir_path):
        for i in files:
            filename_list.append(root + slash + i)
    logging.info(
        ('Under this dir -- {dir}: There are {num} files ').format(
            dir=dir_path,
            num=len(filename_list)))
    return filename_list


def filter_file_by_suffixation(dir_path, *keySuffixation):
    filename_list = get_all_filename(dir_path)
    file_contain_suffixation = []
    for file in filename_list:
        if os.path.splitext(file)[1] in tuple(keySuffixation):
            file_contain_suffixation.append(file)
    logging.info(
        ('Under this dir -- {dir}: There are {num} files, '
         'suffix called {key}').format(
            dir=dir_path,
            num=len(file_contain_suffixation),
            key=keySuffixation))
    return file_contain_suffixation


current_path = os.path.abspath(os.path.dirname(__file__))


def main():
    # try:
    #     from gen_dependent_parameters import args_
    # except Exception as e:
    #     e.args += ('Import ARGS Error ',)
    #     raise

    # C:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3/src/main/core/video/video_local_track_screen.cpp
    # INPUT_SOURCE_ORIGIN = [r'C:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3/src/main/core/video']
    # for path_item in INPUT_SOURCE_ORIGIN:
    #     for file_item in filter_file_by_suffixation(path_item, '.c', '.cxx', '.cc', '.c++', '.cpp'):
    #         index = clang.cindex.Index.create()
    #         tu = index.parse(file_item, args=ARGS)
    #         root = tu.cursor
    #         gen_ast(file_item, root, '|' + str(root.kind)[str(root.kind).index('.') + 1:], 0)

    # tmpFile = 'C:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3/src/main/core/video/video_local_track_screen.cpp'
    # compilation_database_path = 'C:/Users/liqiu/Desktop/dead_lock/build/win/x64'
    # source_file_path = 'C:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3/src/main/core/video/video_local_track_screen.cpp'
    # index = clang.cindex.Index.create()
    # compdb = clang.cindex.CompilationDatabase.fromDirectory(compilation_database_path)

    # file_args = compdb.getCompileCommands(source_file_path)
    # try:
    #     from gen_dependent_parameters import GenDependentParametersByCdb
    #     _args = GenDependentParametersByCdb(compilation_database_path, source_file_path).get_args()
    #     print os.getcwd()
    # except Exception as e:
    #     e.args += ('Could not load compilation flags !!! ',)
    #     raise
    #
    # index = clang.cindex.Index.create()
    # translation_unit = index.parse(source_file_path, _args)
    # file_nodes = get_nodes_in_file(translation_unit.cursor, source_file_path)

    # tu = index.parse(source_file_path, _args)
    # current_path = os.path.abspath(os.path.dirname(__file__))
    # os.chdir(current_path)
    # root = tu.cursor
    # gen_ast(source_file_path, root, '|' + str(root.kind)[str(root.kind).index('.') + 1:], 0)

    # INPUT_SOURCE_ORIGIN = [r'C:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3']
    compilation_database_path = 'C:/Users/liqiu/Desktop/dead_lock/build/win/x64'
    tmp = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\core\video\video_local_track.cpp'

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

    # print len(FILE_LST)

    # if tmp in FILE_LST:
    #     print 'okay'

    for file_item in [tmp]:
        args_ = GenDependentParametersByCdb(
            compilation_database_path, file_item).get_args()
        index = clang.cindex.Index.create()
        tu = index.parse(file_item, args=args_)

        os.chdir(current_path)
        root = tu.cursor
        gen_ast(file_item, root, '|' + str(root.kind)
        [str(root.kind).index('.') + 1:], 0)

    # compilation_database_path = 'C:/Users/liqiu/Desktop/dead_lock'
    # # compilation_database_path = 'C:/Users/liqiu/Desktop/md/gn/build/win/x64/'
    # # print compilation_database_path
    # # compilation_database_path = 'C:/Users/liqiu/Desktop/md/gn/build/win/x64'
    # source_file_path = 'C:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3/src/main/core/video/video_local_track_screen.cpp'
    # # source_file_path = 'C:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3'
    #
    # # clang_args = ['-x', 'c++', '-std=c++11', '-p', compilation_database_path]
    # index = clang.cindex.Index.create()
    # compdb = clang.cindex.CompilationDatabase.fromDirectory(compilation_database_path)
    #
    # try:
    #     file_args = compdb.getCompileCommands(source_file_path)
    #     print file_args
    #     translation_unit = index.parse(source_file_path, str(file_args))
    #     file_nodes = get_nodes_in_file(translation_unit.cursor, source_file_path)
    #     print [p.spelling for p in file_nodes]
    # except clang.cindex.CompilationDatabaseError:
    #     print 'Could not load compilation flags for', source_file_path


# def main():
#     tmpFile = 'C:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3/src/main/core/video/video_local_track_screen.cpp'
#     index = clang.cindex.Index.create()
#     tu = index.parse(tmpFile, args=args)
#     gen_ast(tu.cursor, 0)

# def main():


if __name__ == '__main__':
    main()
    print 'major_minor_dict:', major_minor_dict
    print 'mem_dict:', mem_dict

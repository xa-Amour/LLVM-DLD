#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging.handlers
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
worker_lst = []
worker_dict = {}


def gen_ast(analysis_file, node, scope, indent):
    global cons_lst, constructor_name, worker_name, worker_type, worker_lst, worker_location_line  # , constructor_name

    # 方法一 列表生成式：
    if node.kind == clang.cindex.CursorKind.CALL_EXPR and (  # CASE_1:'operator='
            node.spelling or node.displayname) == 'operator=':  # and node.location.line == 58 and node.location.column == 7:

        child_node_cursor_lst = [child_node_cursor for child_node_cursor in
                                 node.get_children()]  # 子节点的游标列表：[<clang.cindex.Cursor object at 0x00000000040E85C8>, <clang.cindex.Cursor object at 0x00000000040E88C8>, <clang.cindex.Cursor object at 0x00000000040E8CC8>]
        worker_name = child_node_cursor_lst[0].spelling  # 第一个节点游标的名字，即 media_worker_
        if len(child_node_cursor_lst) >= 3:
            third_para_cursor = child_node_cursor_lst[2]  # 第三个参数的游标
            third_para_cursor_lst = [child_node_cursor for child_node_cursor in
                                     third_para_cursor.get_children()]  # 第三个参数的游标列表：[<clang.cindex.Cursor object at 0x0000000004DC3248>]
            if len(third_para_cursor_lst) >= 1:
                third_para_cursor_first_para_cursor = third_para_cursor_lst[0]  # 第三个参数的第一个参数游标
                third_para_cursor_first_cursor_para_lst = [child_node_cursor for child_node_cursor in
                                                           third_para_cursor_first_para_cursor.get_children()]  # 第三个参数的第一个参数的第一个参数的游标列表：[<clang.cindex.Cursor object at 0x00000000047732C8>]
                if len(third_para_cursor_first_cursor_para_lst) >= 1:
                    if third_para_cursor_first_cursor_para_lst[0].kind == clang.cindex.CursorKind.CALL_EXPR:
                        worker_type = third_para_cursor_first_cursor_para_lst[0].spelling  # minor_worker
                        if worker_type == 'minor_worker' or worker_type == 'major_worker_':
                            worker_lst.append(
                                analysis_file + ' :: ' + worker_name + ' :: ' + worker_type + ' :: ' + str(
                                    node.location.line) + ' :: ' + str(node.location.column) + ' :: ' + 'CASE_1')

    if node.kind == clang.cindex.CursorKind.VAR_DECL:  # and node.location.line == 22 and node.location.column == 8:  # CASE_2:VAR_DECL
        worker_name = node.spelling or node.displayname
        child_node_cursor_lst = [child_node_cursor for child_node_cursor in
                                 node.get_children()]
        if len(child_node_cursor_lst) > 0 and child_node_cursor_lst[0].kind == clang.cindex.CursorKind.UNEXPOSED_EXPR:
            fst_para_cursor = child_node_cursor_lst[0]  # 游标 UNEXPOSED_EXPR  22 18
            fst_para_lst = [child_node_cursor for child_node_cursor in
                            fst_para_cursor.get_children()]
            sec_para_cursor = fst_para_lst[0]  # 游标 CALL_EXPR  22 18
            if sec_para_cursor.kind == clang.cindex.CursorKind.CALL_EXPR and (
                    sec_para_cursor.spelling or sec_para_cursor.spelling == ''):
                node_location_column_flag = sec_para_cursor.location.column
                sec_para_lst = [child_node_cursor for child_node_cursor in
                                sec_para_cursor.get_children()]
                if len(sec_para_lst) > 0 and sec_para_lst[0].kind == clang.cindex.CursorKind.UNEXPOSED_EXPR:
                    trd_para_cursor = sec_para_lst[0]
                    trd_para_lst = [child_node_cursor for child_node_cursor in
                                    trd_para_cursor.get_children()]
                    if len(trd_para_lst) > 0 and trd_para_lst[0].kind == clang.cindex.CursorKind.UNEXPOSED_EXPR:
                        four_para_cursor = trd_para_lst[0]  # 游标 UNEXPOSED_EXPR  22 18
                        four_para_lst = [child_node_cursor for child_node_cursor in
                                         four_para_cursor.get_children()]
                        if len(four_para_lst) > 0 and four_para_lst[0].kind == clang.cindex.CursorKind.CALL_EXPR and \
                                four_para_lst[0].location.column == node_location_column_flag:
                            fif_para_cursor = four_para_lst[0]  # 游标 CALL_EXPR minor_worker 22 18
                            worker_type = (fif_para_cursor.spelling or fif_para_cursor.displayname)
                            if worker_type == 'minor_worker' or worker_type == 'major_worker_':
                                # print analysis_file + ' :: ' + worker_name + ' :: ' + worker_type + ' :: ' + str(
                                #     node.location.line) + ' :: ' + str(node.location.column) + ' :: ' + 'CASE_2'
                                worker_lst.append(
                                    analysis_file + ' :: ' + worker_name + ' :: ' + worker_type + ' :: ' + str(
                                        node.location.line) + ' :: ' + str(node.location.column) + ' :: ' + 'CASE_2')

    # 方法二 生成器：
    # print node.get_children().next()
    # worker_name = node.get_children().next().spelling  # 第一个节点游标的名字，即 media_worker_
    # print worker_name
    # # print worker_name
    # print node.get_children().next().kind
    # third_para_cursor = node.get_children().next()
    # print third_para_cursor.kind
    #
    # worker_lst.append(worker_name + ' :: ' + worker_type)
    # print worker_type.location.line, worker_type.location.column
    # print worker_type.spelling
    # print child_node_cursor_lst
    # print worker_name

    # tmp_lst = [tmp for tmp in child_node_cursor_lst[1].get_children()]
    # print tmp_lst
    # print  tmp_lst[0].spelling, tmp_lst[1].spelling

    # print node.get_children(), node.location.line, node.location.column

    if node.kind == clang.cindex.CursorKind.CALL_EXPR and (  # CASE_3  寻找 make_unique 传入的worker 情况，类比 new A（b_worker);
            node.spelling == 'make_unique' or node.displayname == 'make_unique'):
        child_node_cursor_lst = [child_node_cursor for child_node_cursor in
                                 node.get_children()]
        if len(child_node_cursor_lst) >= 2:
            fst_para_lst = [child_node_cursor for child_node_cursor in
                            child_node_cursor_lst[0].get_children()]
            sec_para_lst = [child_node_cursor for child_node_cursor in
                            fst_para_lst[0].get_children()]
            if sec_para_lst > 1:
                sec_para_inline_cursor = sec_para_lst[1]
                worker_name = (sec_para_inline_cursor.spelling or sec_para_inline_cursor.displayname)
                sec_para_cursor = child_node_cursor_lst[1]
                if sec_para_cursor.kind == clang.cindex.CursorKind.MEMBER_REF_EXPR:
                    worker_type = (sec_para_cursor.spelling or sec_para_cursor.displayname)  # help 有可能线程的命名方式都叫 worker
                    if 'worker' in worker_type.lower():  # 有可能会多筛选
                        worker_lst.append(
                            analysis_file + ' :: ' + worker_name + ' :: ' + worker_type + ' :: ' + str(
                                node.location.line) + ' :: ' + str(node.location.column) + ' :: ' + 'CASE_3')

    if node.kind == clang.cindex.CursorKind.CONSTRUCTOR:
        constructor_name = node.spelling or node.displayname

    if node.kind == clang.cindex.CursorKind.MEMBER_REF:
        worker_name = constructor_name + ' :: ' + node.spelling or node.displayname
        worker_location_line = node.location.line
        # worker_location_column = node.location.column

    if node.kind == clang.cindex.CursorKind.CALL_EXPR and (  # CASE_4  m_baseWorker(utils::major_worker())
            (node.spelling == 'major_worker' or node.displayname == 'major_worker') or (
            node.spelling == 'minor_worker' or node.displayname == 'minor_worker')):
        if node.location.line == worker_location_line:
            worker_type = (node.spelling or node.displayname)
            worker_lst.append(
                analysis_file + ' :: ' + worker_name + ' :: ' + worker_type + ' :: ' + str(
                    node.location.line) + ' :: ' + str(node.location.column) + ' :: ' + 'CASE_4')

    text = node.spelling or node.displayname
    kind_spelling_element = '|' + str(node.kind)[str(node.kind).index('.') + 1:] + ':' + str(text)
    data = ' ' * indent + '{} {} {} {} '.format(kind_spelling_element, text, node.location.line, node.location.column)
    # print str(indent) + ' ' * indent + '{} {} {} {} '.format(kind_spelling_element, text, node.location.line, node.location.column)
    unit = str(scope + kind_spelling_element).replace(' ', '')

    if str(node.kind) == 'CursorKind.CONSTRUCTOR':  # media_worker_ = utils::minor_worker("LocalPipeLineWorker");
        constructor_name = text
    if constructor_name in unit and 'CALL_EXPR' in unit and 'operator=' in unit and unit.split('|')[-1].startswith(
            'MEMBER_REF_EXPR'):
        worker_name = unit.split('|')[-1].split(':')[1]
    if constructor_name in unit and 'CALL_EXPR' in unit and 'operator=' in unit and unit.split('|')[-1].startswith(
            'CALL_EXPR') and (unit.endswith('minor_worker') or unit.endswith('major_worker')):
        worker_type = unit.split('|')[-1].split(':')[1]
        constructor_worker_lst.append(
            analysis_file + ' :: ' + constructor_name + ' :: ' + worker_name + ' :: ' + worker_type)
        with open('constructor_worker_lst.txt', 'a') as fileWriter:
            fileWriter.write(
                analysis_file + ' :: ' + constructor_name + ' :: ' + worker_name + ' :: ' + worker_type + '\n')

    for c in node.get_children():
        gen_ast(analysis_file, c, scope + '' + kind_spelling_element, indent + 2)


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

    tmp = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\base_context.cpp'  # m_worker = utils::major_worker();
    tmp_2 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\network_monitor.cpp'  # auto worker = utils::major_worker();
    tmp_3 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\test\smoke_test\src\audio_sdk\audio_sdk_smoke_test.cpp'  # worker_ = company::utils::major_worker();
    tmp_4 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\test\unit_test\thread_test.cpp'  # auto worker1 = company::utils::major_worker(); auto worker2 = company::utils::minor_worker("worker_2"); auto worker3 = company::utils::minor_worker("worker_3");auto worker4 = company::utils::minor_worker("worker_4");
    tmp_5 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\core\media_node_factory.cpp'  # video_device_worker_ = utils::minor_worker("VideoDeviceWorker");
    tmp_6 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\core\video\video_local_track.cpp'  # media_worker_ = utils::minor_worker("LocalPipeLineWorker");
    tmp_7 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\core\video\video_remote_track.cpp'  # media_worker_ = utils::minor_worker("RemotePipeLineWorker");
    tmp_8 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\net_test\network_tester.cpp'  # m_testWorker = utils::minor_worker("NetworkTester");
    tmp_9 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\common\dns_parser.cpp'
    tmp_10 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\ap_manager.cpp'
    tmp_11 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\network_monitor.cpp'
    tmp_12 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\core\company_service_impl.cpp'
    tmp_13 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\argus\report_service.cpp'
    tmp_14 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\ap_manager.cpp'
    tmp_15 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\rtc_context.cpp'
    tmp_16 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\worker_manager_channel.cpp'

    # try:
    #     from handle_compile_json_file import HandleCompileCommandsJsonFile
    #     FILE_LST = HandleCompileCommandsJsonFile(compilation_database_path).get_abs_file()
    # except Exception as e:
    #     e.args += ('Could not load compilation flags !!! ',)
    #     raise

    from handle_compile_json_file import HandleCompileCommandsJsonFile
    FILE_LST = HandleCompileCommandsJsonFile(compilation_database_path).get_abs_file()
    from gen_dependent_parameters import GenDependentParametersByCdb

    # print len(FILE_LST)

    # if tmp_4 in FILE_LST:
    #     print 'okay'
    # print FILE_LST

    # for file_item in tqdm([tmp, tmp_2, tmp_3, tmp_4, tmp_5, tmp_6, tmp_7, tmp_8,tmp_9,tmp_10,tmp_11,tmp_12,tmp_13,tmp_14,tmp_15,tmp_16], desc="WSX", ncols=100):
    for file_item in tqdm([tmp, tmp_2, tmp_5, tmp_16], desc="WSX", ncols=100):
        # for file_item in FILE_LST:
        args_ = GenDependentParametersByCdb(compilation_database_path, file_item).get_args()
        index = clang.cindex.Index.create()
        tu = index.parse(file_item, args=args_)
        # print '111'
        os.chdir(current_path)
        root = tu.cursor
        gen_ast(file_item, root, '|' + str(root.kind)[str(root.kind).index('.') + 1:], 0)

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
    # print worker_lst
    for i in worker_lst:
        # worker_dict[i.split('::')[1]] = i.split('::')[2]
        print i
    print len(worker_lst)

    from prettytable import PrettyTable

    table = PrettyTable(['编号', 'analysis_file', 'scope', 'worker_name', 'worker_type', 'line', 'colum', 'case_type'])
    i = 1
    for item in worker_lst:
        if len(item.split('::')) == 7:
            table.add_row([i, item.split('::')[0], item.split('::')[1], item.split('::')[2], item.split('::')[3],
                           item.split('::')[4], item.split('::')[5], item.split('::')[6]])
        else:
            table.add_row(
                [i, item.split('::')[0], ' ', item.split('::')[1], item.split('::')[2], item.split('::')[3],
                 item.split('::')[4],
                 item.split('::')[5]])
        i += 1
    print table

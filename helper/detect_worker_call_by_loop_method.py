#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging.handlers
import os

from tqdm import tqdm

import clang.cindex

slash = '\\'

constructor_name = ''
worker_name = ''
worker_type = ''
constructor_worker_lst = []
worker_lst = []
worker_path_lst = []
worker_path_glo_lst = []


def gen_ast(analysis_file, node, scope, indent):
    global constructor_name, domian_name, worker_name, worker_type, worker_lst, worker_identity, worker_location_line, worker_path_lst, worker_path_glo_lst

    # 方法一 列表生成式：
    if node.kind == clang.cindex.CursorKind.CALL_EXPR and (  # CASE_1:'operator='
            node.spelling or node.displayname) == 'operator=':  # and node.location.line == 58 and node.location.column == 7:

        # 子节点的游标列表：[<clang.cindex.Cursor object at 0x00000000040E85C8>, <clang.cindex.Cursor object at 0x00000000040E88C8>, <clang.cindex.Cursor object at 0x00000000040E8CC8>]
        child_node_cursor_lst = [
            child_node_cursor for child_node_cursor in node.get_children()]
        # 第一个节点游标的名字，即 media_worker_
        worker_name = child_node_cursor_lst[0].spelling
        if len(child_node_cursor_lst) >= 3:
            third_para_cursor = child_node_cursor_lst[2]  # 第三个参数的游标
            # 第三个参数的游标列表：[<clang.cindex.Cursor object at 0x0000000004DC3248>]
            third_para_cursor_lst = [
                child_node_cursor for child_node_cursor in third_para_cursor.get_children()]
            if len(third_para_cursor_lst) >= 1:
                # 第三个参数的第一个参数游标
                third_para_cursor_first_para_cursor = third_para_cursor_lst[0]
                # 第三个参数的第一个参数的第一个参数的游标列表：[<clang.cindex.Cursor object at 0x00000000047732C8>]
                third_para_cursor_first_cursor_para_lst = [
                    child_node_cursor for child_node_cursor in third_para_cursor_first_para_cursor.get_children()]
                if len(third_para_cursor_first_cursor_para_lst) >= 1:
                    #
                    if third_para_cursor_first_cursor_para_lst[0].kind == clang.cindex.CursorKind.CALL_EXPR:
                        # minor_worker
                        worker_type = third_para_cursor_first_cursor_para_lst[0].spelling

                        if worker_type == 'major_worker':
                            domian_name = ''
                            worker_identity = ''
                            worker_lst.append(analysis_file +
                                              ' - ' +
                                              domian_name +
                                              ' - ' +
                                              worker_name +
                                              ' - ' +
                                              worker_type +
                                              ' - ' +
                                              worker_identity +
                                              ' - ' +
                                              str(node.location.line) +
                                              ' - ' +
                                              str(node.location.column) +
                                              ' - ' +
                                              'CASE_1')
                        elif worker_type == 'minor_worker':

                            third_para_cursor_first_cursor_para_fst_para_lst = third_para_cursor_first_cursor_para_lst[
                                0]
                            third_para_cursor_first_cursor_para_first_para_lst = [
                                child_node_cursor for child_node_cursor in
                                third_para_cursor_first_cursor_para_fst_para_lst.get_children()]
                            if len(
                                    third_para_cursor_first_cursor_para_first_para_lst) >= 2:
                                third_para_cursor_first_cursor_para_first_para_lst_sec_para_cursor = \
                                    third_para_cursor_first_cursor_para_first_para_lst[1]
                                third_para_cursor_first_cursor_para_first_para_sec_para_lst = [
                                    child_node_cursor for child_node_cursor in
                                    third_para_cursor_first_cursor_para_first_para_lst_sec_para_cursor.get_children()]
                                if len(
                                        third_para_cursor_first_cursor_para_first_para_sec_para_lst) >= 1:
                                    if third_para_cursor_first_cursor_para_first_para_sec_para_lst[
                                        0].kind == clang.cindex.CursorKind.STRING_LITERAL:
                                        domian_name = ''
                                        worker_identity = (third_para_cursor_first_cursor_para_first_para_sec_para_lst[
                                                               0].spelling or
                                                           third_para_cursor_first_cursor_para_first_para_sec_para_lst[
                                                               0].displayname)
                                        worker_lst.append(analysis_file +
                                                          ' - ' +
                                                          domian_name +
                                                          ' - ' +
                                                          worker_name +
                                                          ' - ' +
                                                          worker_type +
                                                          ' - ' +
                                                          worker_identity +
                                                          ' - ' +
                                                          str(node.location.line) +
                                                          ' - ' +
                                                          str(node.location.column) +
                                                          ' - ' +
                                                          'CASE_1')

    # and node.location.line == 22 and node.location.column == 8:  #
    # CASE_2:VAR_DECL
    if node.kind == clang.cindex.CursorKind.VAR_DECL:
        worker_name = node.spelling or node.displayname
        child_node_cursor_lst = [child_node_cursor for child_node_cursor in
                                 node.get_children()]
        if len(
                child_node_cursor_lst) > 0 and child_node_cursor_lst[0].kind == clang.cindex.CursorKind.UNEXPOSED_EXPR:
            # 游标 UNEXPOSED_EXPR  22 18
            fst_para_cursor = child_node_cursor_lst[0]
            fst_para_lst = [child_node_cursor for child_node_cursor in
                            fst_para_cursor.get_children()]
            sec_para_cursor = fst_para_lst[0]  # 游标 CALL_EXPR  22 18
            if sec_para_cursor.kind == clang.cindex.CursorKind.CALL_EXPR and (
                    sec_para_cursor.spelling or sec_para_cursor.spelling == ''):
                node_location_column_flag = sec_para_cursor.location.column
                sec_para_lst = [child_node_cursor for child_node_cursor in
                                sec_para_cursor.get_children()]
                if len(
                        sec_para_lst) > 0 and sec_para_lst[0].kind == clang.cindex.CursorKind.UNEXPOSED_EXPR:
                    trd_para_cursor = sec_para_lst[0]
                    trd_para_lst = [child_node_cursor for child_node_cursor in
                                    trd_para_cursor.get_children()]
                    if len(
                            trd_para_lst) > 0 and trd_para_lst[0].kind == clang.cindex.CursorKind.UNEXPOSED_EXPR:
                        # 游标 UNEXPOSED_EXPR  22 18
                        four_para_cursor = trd_para_lst[0]
                        four_para_lst = [
                            child_node_cursor for child_node_cursor in four_para_cursor.get_children()]
                        if len(four_para_lst) > 0 and four_para_lst[0].kind == clang.cindex.CursorKind.CALL_EXPR and \
                                four_para_lst[0].location.column == node_location_column_flag:
                            # 游标 CALL_EXPR minor_worker 22 18
                            fif_para_cursor = four_para_lst[0]
                            worker_type = (
                                    fif_para_cursor.spelling or fif_para_cursor.displayname)
                            if worker_type == 'major_worker':
                                worker_identity = ''
                                domian_name = ''
                                worker_lst.append(analysis_file +
                                                  ' - ' +
                                                  domian_name +
                                                  ' - ' +
                                                  worker_name +
                                                  ' - ' +
                                                  worker_type +
                                                  ' - ' +
                                                  worker_identity +
                                                  ' - ' +
                                                  str(node.location.line) +
                                                  ' - ' +
                                                  str(node.location.column) +
                                                  ' - ' +
                                                  'CASE_2')
                            elif worker_type == 'minor_worker':
                                fif_para_lst = [
                                    child_node_cursor for child_node_cursor in fif_para_cursor.get_children()]
                                if len(fif_para_lst) >= 2:
                                    six_para_cursor = fif_para_lst[1]
                                    six_para_lst = [
                                        child_node_cursor for child_node_cursor in six_para_cursor.get_children()]
                                    if len(six_para_lst) >= 1:
                                        if six_para_lst[0].kind == clang.cindex.CursorKind.STRING_LITERAL:
                                            worker_identity = six_para_lst[0].spelling or six_para_lst[0].displayname
                                            domian_name = ''
                                            worker_lst.append(analysis_file +
                                                              ' - ' +
                                                              domian_name +
                                                              ' - ' +
                                                              worker_name +
                                                              ' - ' +
                                                              worker_type +
                                                              ' - ' +
                                                              worker_identity +
                                                              ' - ' +
                                                              str(node.location.line) +
                                                              ' - ' +
                                                              str(node.location.column) +
                                                              ' - ' +
                                                              'CASE_2')

    if node.kind == clang.cindex.CursorKind.CALL_EXPR and (  # CASE_3  寻找 make_unique 传入的worker 情况，类比 new A（b_worker);
            node.spelling == 'make_unique' or node.displayname == 'make_unique'):  # 解析结果：class company::rtc::VideoNodeFilter    |  media_worker_
        child_node_cursor_lst = [child_node_cursor for child_node_cursor in
                                 node.get_children()]
        if len(child_node_cursor_lst) >= 2:
            fst_para_lst = [child_node_cursor for child_node_cursor in
                            child_node_cursor_lst[0].get_children()]
            sec_para_lst = [child_node_cursor for child_node_cursor in
                            fst_para_lst[0].get_children()]
            if len(sec_para_lst) > 1:
                for sec_para in sec_para_lst:
                    if sec_para.kind == clang.cindex.CursorKind.TYPE_REF:
                        domian_name = (
                                sec_para.spelling or sec_para.displayname)
                if 'class' in domian_name.lower():  # 避免出现以下情况：5    | placeholder_sdk_script\placeholder_sdk3\src\main\core\video\video_local_track_yuv.cpp  |        |  rtc                                      |  media_worker_  |                 |  40  |  12   |  CASE_3
                    # sec_para_cursor = child_node_cursor_lst[1]
                    for child_node_cursor in child_node_cursor_lst:
                        if child_node_cursor.kind == clang.cindex.CursorKind.MEMBER_REF_EXPR:
                            worker_name = (
                                    child_node_cursor.spelling or child_node_cursor.displayname)
                            if 'worker' in worker_name.lower():  # 有可能会多筛选
                                worker_type = ''
                                worker_identity = ''
                                worker_lst.append(analysis_file +
                                                  ' - ' +
                                                  domian_name +
                                                  ' - ' +
                                                  worker_name +
                                                  ' - ' +
                                                  worker_type +
                                                  ' - ' +
                                                  worker_identity +
                                                  ' - ' +
                                                  str(node.location.line) +
                                                  ' - ' +
                                                  str(node.location.column) +
                                                  ' - ' +
                                                  'CASE_3')
                        # 不存在 MEMBER_REF_EXPR 的node，存在 DECL_REF_EXPR 的 node，例如：|DECL_REF_EXPR pipeline_worker 31 53
                        elif child_node_cursor.kind == clang.cindex.CursorKind.DECL_REF_EXPR:
                            worker_name = child_node_cursor.spelling or child_node_cursor.displayname
                            if 'worker' in worker_name.lower():  # 有可能会多筛选
                                worker_type = ''
                                worker_identity = ''
                                worker_lst.append(analysis_file +
                                                  ' - ' +
                                                  domian_name +
                                                  ' - ' +
                                                  worker_name +
                                                  ' - ' +
                                                  worker_type +
                                                  ' - ' +
                                                  worker_identity +
                                                  ' - ' +
                                                  str(node.location.line) +
                                                  ' - ' +
                                                  str(node.location.column) +
                                                  ' - ' +
                                                  'CASE_3')

    # 'audio_device_core_win.cc' 中情况：company::utils::minor_worker("AudioDeviceWorker")
    if node.kind == clang.cindex.CursorKind.CALL_EXPR and (
            node.spelling == 'minor_worker' or node.displayname == 'minor_worker'):
        worker_type = (node.spelling or node.displayname)
        child_node_cursor_lst = [child_node_cursor for child_node_cursor in
                                 node.get_children()]
        for child_node_cursor in child_node_cursor_lst:
            if child_node_cursor.kind == clang.cindex.CursorKind.UNEXPOSED_EXPR and (
                    child_node_cursor.spelling == '' or child_node_cursor.displayname == ''):
                fst_para_lst = [child_node_cursor for child_node_cursor in
                                child_node_cursor.get_children()]
                if len(
                        fst_para_lst) >= 1 and fst_para_lst[0].kind == clang.cindex.CursorKind.STRING_LITERAL:
                    worker_identity = (
                            fst_para_lst[0].spelling or fst_para_lst[0].displayname)
                    domian_name = ''
                    worker_name = ''
                    worker_lst.append(analysis_file +
                                      ' - ' +
                                      domian_name +
                                      ' - ' +
                                      worker_name +
                                      ' - ' +
                                      worker_type +
                                      ' - ' +
                                      worker_identity +
                                      ' - ' +
                                      str(node.location.line) +
                                      ' - ' +
                                      str(node.location.column) +
                                      ' - ' +
                                      'CASE_4')

    # CASE_5 寻找 new 构造传入的worker 情况，类比 new StreamInWorker（b_worker);
    if node.kind == clang.cindex.CursorKind.CXX_NEW_EXPR:
        child_node_cursor_lst = [child_node_cursor for child_node_cursor in
                                 # media_node_factory.cpp: return new
                                 # RefCountedObject<rtc::VideoCameraSourceWrapper>(video_device_worker_);
                                 node.get_children()]
        if len(child_node_cursor_lst) >= 1:
            for item in child_node_cursor_lst:
                if item.kind == clang.cindex.CursorKind.TYPE_REF:
                    domian_name = (item.spelling or item.displayname)
                if item.kind == clang.cindex.CursorKind.CALL_EXPR:
                    sec_para_lst = [child_node_cursor for child_node_cursor in
                                    item.get_children()]
                    if len(sec_para_lst) >= 1:
                        for i in sec_para_lst:
                            if i.kind == clang.cindex.CursorKind.MEMBER_REF_EXPR and (
                                    'worker' in i.spelling.lower() or 'worker' in i.displayname.lower()):
                                worker_name = (i.spelling or i.displayname)
                                worker_type = ''
                                worker_identity = ''
                                worker_lst.append(analysis_file +
                                                  ' - ' +
                                                  domian_name +
                                                  ' - ' +
                                                  worker_name +
                                                  ' - ' +
                                                  worker_type +
                                                  ' - ' +
                                                  worker_identity +
                                                  ' - ' +
                                                  str(node.location.line) +
                                                  ' - ' +
                                                  str(node.location.column) +
                                                  ' - ' +
                                                  'CASE_5')

    # VideoCameraSourceWrapper::VideoCameraSourceWrapper(utils::worker_type
    # worker): worker_(worker),
    if node.kind == clang.cindex.CursorKind.CONSTRUCTOR:
        child_node_cursor_lst = [child_node_cursor for child_node_cursor in
                                 node.get_children()]
        domian_name = (node.spelling or node.displayname)
        if len(child_node_cursor_lst) >= 1:
            if_has_worker_type = False
            for child_node_cursor in child_node_cursor_lst:

                if child_node_cursor.kind == clang.cindex.CursorKind.PARM_DECL:
                    sec_para_lst = [child_node_cursor for child_node_cursor in
                                    child_node_cursor.get_children()]

                    if len(sec_para_lst) >= 1 and (clang.cindex.CursorKind.TYPE_REF in [
                        sec_para_cursor.kind for sec_para_cursor in sec_para_lst]):
                        for sec_para_cursor in [
                            (sec_para_cursor.spelling.lower() or sec_para_cursor.displayname.lower()) for
                            sec_para_cursor in sec_para_lst]:
                            if 'worker_type' in sec_para_cursor:
                                if_has_worker_type = True

                if if_has_worker_type and child_node_cursor.kind == clang.cindex.CursorKind.MEMBER_REF and (
                        'worker' in child_node_cursor.spelling or 'worker' in child_node_cursor.displayname):
                    worker_name = (
                            child_node_cursor.spelling or child_node_cursor.displayname)
                    worker_type = ''
                    worker_identity = ''
                    worker_lst.append(analysis_file +
                                      ' - ' +
                                      domian_name +
                                      ' - ' +
                                      worker_name +
                                      ' - ' +
                                      worker_type +
                                      ' - ' +
                                      worker_identity +
                                      ' - ' +
                                      str(node.location.line) +
                                      ' - ' +
                                      str(node.location.column) +
                                      ' - ' +
                                      'CASE_7')

                if if_has_worker_type and (
                        clang.cindex.CursorKind.MEMBER_REF not in [child_node_cursor.kind for child_node_cursor in
                                                                   child_node_cursor_lst] or (
                                child_node_cursor.kind == clang.cindex.CursorKind.MEMBER_REF and
                                'worker' not in child_node_cursor.spelling and 'worker' not in child_node_cursor.displayname)):  # (没有 MEMBER_REF 或者有 MEMBER_REF and 'worker' in node.spelling)
                    worker_name = 'worker_'
                    worker_type = ''
                    worker_identity = ''
                    if_has_worker_type = False
                    worker_lst.append(analysis_file +
                                      ' - ' +
                                      domian_name +
                                      ' - ' +
                                      worker_name +
                                      ' - ' +
                                      worker_type +
                                      ' - ' +
                                      worker_identity +
                                      ' - ' +
                                      str(node.location.line) +
                                      ' - ' +
                                      str(node.location.column) +
                                      ' - ' +
                                      'CASE_8')

    if node.kind == clang.cindex.CursorKind.CONSTRUCTOR:
        domian_name = node.spelling or node.displayname

    if node.kind == clang.cindex.CursorKind.MEMBER_REF:
        worker_name = node.spelling or node.displayname
        worker_location_line = node.location.line

    if node.kind == clang.cindex.CursorKind.CALL_EXPR and (  # CASE_4  m_baseWorker(utils-major_worker())
            (node.spelling == 'major_worker' or node.displayname == 'major_worker') or (
            node.spelling == 'minor_worker' or node.displayname == 'minor_worker')):
        if node.location.line == worker_location_line:
            worker_type = (node.spelling or node.displayname)
            worker_identity = ''
            worker_lst.append(analysis_file +
                              ' - ' +
                              domian_name +
                              ' - ' +
                              worker_name +
                              ' - ' +
                              worker_type +
                              ' - ' +
                              worker_identity +
                              ' - ' +
                              str(node.location.line) +
                              ' - ' +
                              str(node.location.column) +
                              ' - ' +
                              'CASE_6')

    text = node.spelling or node.displayname
    kind_spelling_element = '|' + \
                            str(node.kind)[str(node.kind).index('.') + 1:] + ':' + str(text)

    for cn in node.get_children():
        if node.kind == clang.cindex.CursorKind.CALL_EXPR and (
                node.spelling == 'sync_call' or node.displayname == 'sync_call') and node.location.line == 62 and node.location.column == 3:
            print cn.spelling, cn.kind, cn.location.line, cn.location.column
        if cn.kind == clang.cindex.CursorKind.DECL_REF_EXPR and 'worker' in cn.spelling:
            print cn.spelling, cn.kind, cn.location.line, cn.location.column
            worker_path_lst.append(cn.spelling)
        gen_ast(
            analysis_file,
            cn,
            scope +
            '' +
            kind_spelling_element,
            indent +
            2)

    if node.kind == clang.cindex.CursorKind.CALL_EXPR and (
            node.spelling == 'sync_call' or node.displayname == 'sync_call') and node.location.line == 62 and node.location.column == 3:

        for cn in node.get_children():
            detect_worker_call(analysis_file, cn)

    worker_path_glo_lst.append(worker_path_lst)

    for c in node.get_children():
        gen_ast(
            analysis_file,
            c,
            scope +
            '' +
            kind_spelling_element,
            indent +
            2)

        print 444, c.spelling, c.kind, c.location.line, c.location.column

    data = ' ' * indent + '{} {} {} {} '.format(
        kind_spelling_element, text, node.location.line, node.location.column)
    # print str(indent) + ' ' * indent + '{} {} {} {} '.format(kind_spelling_element, text, node.location.line, node.location.column)
    unit = str(scope + kind_spelling_element).replace(' ', '')

    # media_worker_ = utils-minor_worker("LocalPipeLineWorker");
    if str(node.kind) == 'CursorKind.CONSTRUCTOR':
        constructor_name = text
    if constructor_name in unit and 'CALL_EXPR' in unit and 'operator=' in unit and unit.split(
            '|')[-1].startswith('MEMBER_REF_EXPR'):
        worker_name = unit.split('|')[-1].split(':')[1]
    if constructor_name in unit and 'CALL_EXPR' in unit and 'operator=' in unit and unit.split(
            '|')[-1].startswith('CALL_EXPR') and (unit.endswith('minor_worker') or unit.endswith('major_worker')):
        worker_type = unit.split('|')[-1].split(':')[1]
        constructor_worker_lst.append(
            analysis_file +
            ' - ' +
            constructor_name +
            ' - ' +
            worker_name +
            ' - ' +
            worker_type)
        with open('constructor_worker_lst.txt', 'a') as fileWriter:
            fileWriter.write(
                analysis_file +
                ' - ' +
                constructor_name +
                ' - ' +
                worker_name +
                ' - ' +
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


def detect_worker_call(analysis_file, node):  # 单独写一个递归函数，组装到功能函数上去
    for child_node in node.get_children():
        detect_worker_call(analysis_file, child_node)
        if child_node.kind == clang.cindex.CursorKind.DECL_REF_EXPR and 'worker' in (
                child_node.spelling or child_node.displayname):
            worker_path_lst.append(
                child_node.spelling or child_node.displayname)


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
    compilation_database_path = 'C:/Users/liqiu/Desktop/dead_lock/build/win/x64'

    # m_worker = utils-major_worker();
    tmp = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\base_context.cpp'
    # auto worker = utils-major_worker();
    tmp_2 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\network_monitor.cpp'
    # worker_ = company-utils-major_worker();
    tmp_3 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\test\smoke_test\src\audio_sdk\audio_sdk_smoke_test.cpp'
    # auto worker1 = company-utils-major_worker(); auto worker2 =
    # company-utils-minor_worker("worker_2"); auto worker3 =
    # company-utils-minor_worker("worker_3");auto worker4 =
    # company-utils-minor_worker("worker_4");
    tmp_4 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\test\unit_test\thread_test.cpp'
    # video_device_worker_ = utils-minor_worker("VideoDeviceWorker");
    tmp_5 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\core\media_node_factory.cpp'
    # media_worker_ = utils-minor_worker("LocalPipeLineWorker");
    tmp_6 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\core\video\video_local_track.cpp'
    # media_worker_ = utils-minor_worker("RemotePipeLineWorker");
    tmp_7 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\core\video\video_remote_track.cpp'
    # m_testWorker = utils-minor_worker("NetworkTester");
    tmp_8 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\net_test\network_tester.cpp'
    tmp_9 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\common\dns_parser.cpp'
    tmp_10 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\ap_manager.cpp'
    tmp_11 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\core\company_service_impl.cpp'
    tmp_12 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\argus\report_service.cpp'
    tmp_13 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\ap_manager.cpp'
    tmp_14 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\rtc_context.cpp'
    tmp_15 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\worker_manager_channel.cpp'
    tmp_16 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\core\audio\audio_remote_track.cpp'
    tmp_17 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\media_engine2\company\modules\chromium\media\audio\win\audio_device_core_win.cc'
    tmp_18 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\core\video\video_local_track_yuv.cpp'  # CASE_3
    tmp_19 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\core\video\video_local_track_camera.cpp'  # CASE_3
    tmp_20 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\core\video\video_local_track_direct_image.cpp'  # CASE_3
    tmp_21 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\core\video\video_local_track_image.cpp'  # CASE_3
    tmp_22 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\core\video\video_local_track_screen.cpp'  # CASE_3
    tmp_23 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\engine_adapter\video\video_engine.cpp'
    tmp_24 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\test\smoke_test\src\connection_sdk\connection_test.cpp'
    # VideoCameraSourceWrapper::VideoCameraSourceWrapper(utils::worker_type
    # worker): worker_(worker),
    tmp_25 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\core\video\video_camera_source.cpp'
    tmp_26 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\core\video\video_screen_source.cpp'
    tmp_27 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\core\video\video_renderer.cpp'
    tmp_28 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\main\core\video\video_file_sink.cpp'
    tmp_29 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\engine_adapter\video\video_node_filter.cpp'
    tmp_30 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\common\dns_parser.cpp'
    tmp_31 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\argus\report_link_manager.cpp'
    tmp_32 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\argus\report_lbs.cpp'
    tmp_33 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\engine_adapter\video\video_node_encoder.cpp'
    tmp_34 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\engine_adapter\video\video_node_renderer.cpp'
    tmp_35 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\engine_adapter\video\video_node_tee.cpp'
    tmp_36 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\engine_adapter\video\video_node_custom_source.cpp'
    tmp_37 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\engine_adapter\video\video_node_cc_sender.cpp'
    tmp_38 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\engine_adapter\video\video_node_camera_source.cpp'
    tmp_39 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\engine_adapter\video\video_node_image_sender.cpp'
    tmp_40 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\engine_adapter\video\video_node_screen_source.cpp'
    tmp_41 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\placeholder_sdk3\src\engine_adapter\video\video_node_decoder.cpp'
    tmp_42 = r'C:\Users\liqiu\Desktop\md\placeholder_sdk_script\media_engine2\company\modules\chromium\media\audio\win\wavein_input_win_in_worker.cc'

    from handle_compile_json_file import HandleCompileCommandsJsonFile
    FILE_LST = HandleCompileCommandsJsonFile(
        compilation_database_path).get_abs_file()
    from gen_dependent_parameters import GenDependentParametersByCdb

    # for file_item in tqdm(
    #         [tmp, tmp_2, tmp_3, tmp_4, tmp_5, tmp_6, tmp_7, tmp_8, tmp_9, tmp_10, tmp_11, tmp_12, tmp_13, tmp_14,
    # tmp_15, tmp_16, tmp_17, tmp_18, tmp_19, tmp_20, tmp_21, tmp_22, tmp_23,
    # tmp_24,tmp_25,tmp_26,tmp_27,tmp_28,tmp_29,tmp_30,tmp_31,tmp_32,tmp_33,tmp_34,tmp_35,tmp_36,tmp_37,tmp_38,tmp_39,tmp_40,tmp_41],
    # desc="WSX", ncols=100):
    for file_item in tqdm([tmp_4], desc="WSX", ncols=100):
        args_ = GenDependentParametersByCdb(
            compilation_database_path, file_item).get_args()
        index = clang.cindex.Index.create()
        tu = index.parse(file_item, args=args_)
        os.chdir(current_path)
        root = tu.cursor
        gen_ast(file_item, root, '|' + str(root.kind)
        [str(root.kind).index('.') + 1:], 0)
    print worker_path_lst


if __name__ == '__main__':
    main()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

worker_identity_dict = {
    'major_worker': {
        'worker_name': 'major_worker',
        'inheritance_worker': 'base_worker',
        'worker_type': 'major_worker',
        'if_called_by_constructor': 'False',
        'worker_identity': {
            'major_worker': [
                'major_worker',
            ]}},

    'video_device_worker_': {
        'worker_name': 'video_device_worker_',
        'inheritance_worker': 'base_worker',
        'worker_type': 'minor_worker',
        'if_called_by_constructor': 'True',
        'Constructor_call': [
            'company::rtc::VideoCameraSourceWrapper',
            'company::rtc::VideoScreenSourceWrapper',
            'company::rtc::VideoRendererWrapper',
            'company::rtc::FileSink'],
        'worker_identity': {
            'worker_': [
                'VideoDeviceWorker',
            ],
            'capturer_worker_': [
                'VideoDeviceWorker',
            ]}},

    'media_worker_': {
        'worker_name': 'media_worker_',
        'inheritance_worker': 'base_worker',
        'worker_type': 'minor_worker',
        'if_called_by_constructor': 'True',
        'Constructor_call': [
            'company::rtc::VideoNodeFilter',
            'company::rtc::VideoNodeRenderer',
            'company::rtc::VideoNodeTee',
            'company::rtc::VideoNodeCustomSource',
            'company::rtc::VideoNodeFilter',
            'company::rtc::VideoNodeTxProcessor',
            'company::rtc::VideoNodeGccSender',
            'company::rtc::VideoNodeCameraSource',
            'company::rtc::VideoNodeImageSender',
            'company::rtc::VideoNodeScreenSource',
            'company::rtc::VideoNodeRxProcessor',
            ''],
        'worker_identity': {
            'worker_': [
                'LocalPipeLineWorker',
                'RemotePipeLineWorker']}},

    'capturer_worker_': {
        'worker_name': 'capturer_worker_',
        'inheritance_worker': 'base_worker',
        'worker_type': 'minor_worker',
        'if_called_by_constructor': 'False',
        'worker_identity': {
            'capturer_worker_': [
                'VideoDeviceWorker',
            ]}},

    'm_testWorker': {
        'worker_name': 'm_testWorker',
        'inheritance_worker': 'base_worker',
        'worker_type': 'minor_worker',
        'if_called_by_constructor': 'True',
        'Constructor_call': [
            'company::commons::dns_parser_manager'],
        'worker_identity': {
            'worker_': [
                'NetworkTester',
            ]}},

    'm_worker': {
        'worker_name': 'm_worker',
        'inheritance_worker': 'base_worker',
        'worker_type': 'major_worker',
        'if_called_by_constructor': 'False',
        'worker_identity': {
            'm_worker': [
                'major_worker',
            ]}},

    'worker': {
        'worker_name': 'worker',
        'inheritance_worker': 'base_worker',
        'worker_type': 'major_worker',
        'if_called_by_constructor': 'False',
        'worker_identity': {
            'worker': [
                'major_worker',
            ]}},

    'worker_': {
        'worker_name': 'worker_',
        'inheritance_worker': 'base_worker',
        'worker_type': 'major_worker',
        'if_called_by_constructor': 'False',
        'worker_identity': {
            'worker_': [
                'major_worker',
            ]}},

    'worker_f': {
        'worker_name': 'worker_f',
        'inheritance_worker': 'base_worker',
        'worker_type': 'major_worker',
        'if_called_by_constructor': 'False',
        'worker_identity': {
            'worker_f': [
                'major_worker',
            ]}},

    'm_baseWorker': {
        'worker_name': 'm_baseWorker',
        'inheritance_worker': 'base_worker',
        'worker_type': 'major_worker',
        'if_called_by_constructor': 'False',
        'worker_identity': {
            'm_baseWorker': [
                'major_worker',
            ]}},

    'worker_s': {
        'worker_name': 'worker_s',
        'inheritance_worker': 'base_worker',
        'worker_type': 'minor_worker',
        'if_called_by_constructor': 'False',
        'worker_identity': {
            'worker_s': [
                'worker_2',
            ]}},

    'worker_t': {
        'worker_name': 'worker_t',
        'inheritance_worker': 'base_worker',
        'worker_type': 'minor_worker',
        'if_called_by_constructor': 'False',
        'worker_identity': {
            'worker_t': [
                'worker_3',
            ]}},

    'worker_r': {
        'worker_name': 'worker_r',
        'inheritance_worker': 'base_worker',
        'worker_type': 'minor_worker',
        'if_called_by_constructor': 'False',
        'worker_identity': {
            'worker_r': [
                'worker_4',
            ]}},

}

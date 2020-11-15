#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

pipe = os.popen('clang -Xclang -ast-dump -fsyntax-only     '
                '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/media_engine2/webrtc/third_party/libyuv/include '
                '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/media_engine2/webrtc '
                '-IC:/Users/liqiu/Desktop/md/gn/build/win/x64/gen '
                '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3/include '
                '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3/interface/cpp '
                '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3/interface/c '
                '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3/lib/include '
                '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3/src '
                '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/media_engine2/webrtc '
                '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/media_engine2 '
                '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/media_engine2/company '
                '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/media_engine2/webrtc/third_party/abseil-cpp '
                '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3/src/common/log '
                '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/media_engine2/company'
                '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3_private/src'
                '-I"C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Tools\\MSVC\\14.16.27023\\ATLMFC\\include"  '
                '-I"C:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Tools\\MSVC\\14.16.27023\\include"   '
                '-I"C:\\Program Files (x86)\\Windows Kits\\NETFXSDK\\4.6.1\\include\\um"   '
                '-I"C:\\Program Files (x86)\\Windows Kits\\10\\include\\10.0.17134.0\\ucrt"  '
                '-I"C:\\Program Files (x86)\\Windows Kits\\10\\include\\10.0.17134.0\\shared"  '
                '-I"C:\\Program Files (x86)\\Windows Kits\\10\\include\\10.0.17134.0\\um"  '
                '-I"C:\\Program Files (x86)\\Windows Kits\\10\\include\\10.0.17134.0\\winrt"  '
                '-I"C:\\Program Files (x86)\\Windows Kits\\10\\include\\10.0.17134.0\\cppwinrt"   '
                'C:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3/src/main/core/video/video_local_track_screen.cpp')

text = pipe.read()
with open('video-ast-dump.txt', 'w') as fileWriter:
    for data in text:
        fileWriter.write(data)
print 'Clang Parser Done!'

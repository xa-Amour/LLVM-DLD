#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pprint
import shlex

import ccsyspath

import clang.cindex

syspath = ccsyspath.system_include_paths('clang++')

incargs = [b'-I' + inc for inc in syspath]
print incargs

args_ = '-x c++ -v    -IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/media_engine2/webrtc/third_party/libyuv/include -IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/media_engine2/webrtc -IC:/Users/liqiu/Desktop/md/gn/build/win/x64/gen -IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3/include -IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3/interface/cpp -IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3/interface/c -IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3/lib/include -IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3/src -IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/media_engine2/webrtc -IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/media_engine2 -IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/media_engine2/company -IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/media_engine2/webrtc/third_party/abseil-cpp -IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3/src/common/log -IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/media_engine2/company -IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3_private/src    -IC:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Tools\\MSVC\\14.16.27023\\ATLMFC\\include  -IC:\\Program Files (x86)\\Microsoft Visual Studio\\2017\\Community\\VC\\Tools\\MSVC\\14.16.27023\\include   -IC:\\Program Files (x86)\\Windows Kits\\NETFXSDK\\4.6.1\\include\\um   -IC:\\Program Files (x86)\\Windows Kits\\10\\include\\10.0.17134.0\\ucrt  -IC:\\Program Files (x86)\\Windows Kits\\10\\include\\10.0.17134.0\\shared  -IC:\\Program Files (x86)\\Windows Kits\\10\\include\\10.0.17134.0\\um  -IC:\\Program Files (x86)\\Windows Kits\\10\\include\\10.0.17134.0\\winrt  -IC:\\Program Files (x86)\\Windows Kits\\10\\include\\10.0.17134.0\\cppwinrt'.split(
) + incargs

args = shlex.split('-x c++ -v  '
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
                   '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/media_engine2/company '
                   '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3_private/src   '

                   # '-I../../../../placeholder_sdk_script/media_engine2/webrtc/third_party/libyuv/include '
                   # '-I../../../../placeholder_sdk_script/media_engine2/webrtc '
                   # '-Igen '
                   # '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3/include '
                   # '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3/interface/cpp '
                   # '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3/interface/c '
                   # '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3/lib/include '
                   # '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3/src '
                   # '-I../../../../placeholder_sdk_script/media_engine2/webrtc '
                   # '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/media_engine2 '
                   # '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/media_engine2/company '
                   # '-I../../../../placeholder_sdk_script/media_engine2/webrtc/third_party/abseil-cpp '
                   # '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3/src/common/log '
                   # '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/media_engine2/company '
                   # '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3_private/src  '
                   # '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/media_engine2/webrtc/third_party/libyuv/include '
                   # '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/media_engine2/webrtc '
                   # '-IC:/Users/liqiu/Desktop/md/gn/build/win/x64/gen '
                   # '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3/include '
                   # '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3/interface/cpp '
                   # '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3/interface/c '
                   # '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3/lib/include '
                   # '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3/src '
                   # '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/media_engine2/webrtc '
                   # '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/media_engine2 '
                   # '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/media_engine2/company '
                   # '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/media_engine2/webrtc/third_party/abseil-cpp '
                   # '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3/src/common/log '
                   # '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/media_engine2/company '
                   # '-IC:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3_private/src    '

                   '-DV8_DEPRECATION_WARNINGS -DUSE_AURA=1 -DNO_TCMALLOC -DFULL_SAFE_BROWSING -DSAFE_BROWSING_CSD -DSAFE_BROWSING_DB_LOCAL -DGOOGLE_CHROME_BUILD -D_HAS_NODISCARD -D_HAS_EXCEPTIONS=0 -D__STD_C -D_CRT_RAND_S -D_CRT_SECURE_NO_DEPRECATE -D_SCL_SECURE_NO_DEPRECATE -D_ATL_NO_OPENGL -D_WINDOWS -DCERT_CHAIN_PARA_HAS_EXTRA_FIELDS -DPSAPI_VERSION=1 -DWIN32 -D_SECURE_ATL -D_USING_V110_SDK71_ -DWINAPI_FAMILY=WINAPI_FAMILY_DESKTOP_APP -DWIN32_LEAN_AND_MEAN -DNOMINMAX -D_UNICODE -DUNICODE -DNTDDI_VERSION=0x0A000002 -D_WIN32_WINNT=0x0A00 -DWINVER=0x0A00 -DNDEBUG -DNVALGRIND -DDYNAMIC_ANNOTATIONS_ENABLED=0 -DFEATURE_OLD_APISET -DFEATURE_EVENT_ENGINE -DFEATURE_AUDIO -DFEATURE_VIDEO_SEI -DFEATURE_VIDEO -DFEATURE_DATA_CHANNEL -DFEATURE_BUILTIN_ENCRYPTION -DFEATURE_STATIC_CRYPTO_LIB -DFEATURE_PLUGIN_MANAGER -DFEATURE_BACKWARD_COMPATIBILITY -DFEATURE_SOCKET_PORT_ALLOCATION -DFEATURE_SOCKS5 -DFEATURE_P2P -DFEATURE_TCP -DFEATURE_HTTP -DFEATURE_RECORDING_SERVICE -DFEATURE_PING_PROBE -DFEATURE_STRING_UID -DFEATURE_ENABLE_UT -D_SILENCE_TR1_NAMESPACE_DEPRECATION_WARNING -DFEATURE_ENABLE_MS_MF -DFEATURE_ENABLE_INTEL_MFX -DFEATURE_ENABLE_NVIDIA_CODEC -DFEATURE_NETWORK_TEST -DFEATURE_ENABLE_PROFILER -DcompanyRTC_HAS_EXCEPTION=0 -DWEBRTC_WIN -DNOMINMAX -D_CRT_SECURE_NO_WARNINGS -D_WINSOCK_DEPRECATED_NO_WARNINGS -DUNICODE -D_UNICODE -DFEATURE_ENABLE_CHROMIUM_MODULE -DFEATURE_ENABLE_SAURON -I"C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/VC/Tools/MSVC/14.16.27023/ATLMFC/include"') + incargs


def gen_ast(node, indent):
    text = node.spelling or node.displayname
    kind = '|' + str(node.kind)[str(node.kind).index('.') + 1:]
    data = ' ' * indent + \
           '{} {} {} {} '.format(kind, text, node.location.line, node.location.column)
    with open('gen_ast_21.txt', 'a') as fileWriter:
        fileWriter.write(str(indent) + str(data) + '\n')
    for i in node.get_children():
        gen_ast(i, indent + 2)


def main():
    tmpFile = 'C:/Users/liqiu/Desktop/md/placeholder_sdk_script/placeholder_sdk3/src/main/core/video/video_local_track_screen.cpp'
    index = clang.cindex.Index.create()
    tu = index.parse(tmpFile, args=args)
    gen_ast(tu.cursor, 0)
    pprint.pprint(args)


if __name__ == '__main__':
    main()

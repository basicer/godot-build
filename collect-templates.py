import sys
import urllib.request
import os
from subprocess import check_output, Popen, PIPE, STDOUT

TARGETS = [

    (None, 'android_debug.apk'),
    ('android_release.apk', 'android_release.apk'),
    ('android_source.zip', 'android_source.zip'),
    (None, 'ios.zip'),
    (None, 'linux_debug.arm32'),
    (None, 'linux_debug.arm64'),
    (None, 'linux_debug.x86_32'),
    (None, 'linux_debug.x86_64'),
    (None, 'linux_release.arm32'),
    (None, 'linux_release.arm64'),
    (None, 'linux_release.x86_32'),
    (None, 'linux_release.x86_64'),
    (None, 'macos.zip'),
    (None, 'macos_template.app'),
    (None, 'version.txt'),
    (None, 'web_debug.zip'),
    (None, 'web_dlink_debug.zip'),
    (None, 'web_dlink_nothreads_debug.zip'),
    (None, 'web_dlink_nothreads_release.zip'),
    (None, 'web_dlink_release.zip'),
    (None, 'web_nothreads_debug.zip'),
    (None, 'web_nothreads_release'),
    (None, 'web_nothreads_release.zip'),
    ('godot.web.template_release.wasm32.zip', 'web_release.zip'),
    (None, 'windows_debug_arm64.exe'),
    (None, 'windows_debug_arm64_console.exe'),
    (None, 'windows_debug_x86_32.exe'),
    (None, 'windows_debug_x86_32_console.exe'),
    (None, 'windows_debug_x86_64.exe'),
    (None, 'windows_debug_x86_64_console.exe'),
    (None, 'windows_release_arm64.exe'),
    (None, 'windows_release_arm64_console.exe'),
    (None, 'windows_release_x86_32.exe'),
    (None, 'windows_release_x86_32_console.exe'),
    ('godot.windows.template_release.x86_64.exe', 'windows_release_x86_64.exe'),
    (None, 'windows_release_x86_64_console.exe'),
]

for ((uripart, filename)) in TARGETS:
    p = f'templates/{filename}'
    if os.path.isfile(p):
        continue

    if uripart == None:
        continue

    url = f'https://github.com/basicer/godot-build/releases/download/latest/{uripart}'
    print(url)
    contents = urllib.request.urlopen(url).read()
    with open(p, 'wb') as h:
        h.write(contents)


check_output(['/bin/sh', '-c', 'zip -q -9 -r -D "export_templates.tpz" templates/*'])
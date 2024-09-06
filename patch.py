import sys
import urllib.request
from subprocess import Popen, PIPE, STDOUT

PRS_TO_ADD = [ 91263, 95788, 91884 ]

print("Patching!")
print("Python version: ", sys.version)

for pr in PRS_TO_ADD:
    url = "https://github.com/godotengine/godot/pull/" + str(pr) + ".patch"
    print(url)
    contents = urllib.request.urlopen(url).read()
    sys.stdout.write(contents.decode('utf-8'))
    p = Popen(['git', 'am'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
    out = p.communicate(input=contents)[0]
    print(out.decode('utf-8'))

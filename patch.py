import sys
import os
import argparse
import urllib.request
from subprocess import check_output, Popen, PIPE, STDOUT

parser = argparse.ArgumentParser(
    prog='Patch.py',
    description='Apply patches to Godot',
)

parser.add_argument('-p', '--push', action='store_true')

PRS_TO_ADD = [
    91884, # Specify key when loading pack
    91263, # QOI Import
    95788, # WASM Interperter
    96897, # Resource Preview request_draw_and_wait
]

print("Patching!")
print("Python version: ", sys.version)

ident = None
try:
    ident = check_output("git config --get user.email".split(" "))
except:
    pass

if not ident or len(ident) < 5:
	print(check_output("git config --global user.email patch@basicer.com".split(" ")))
	print(check_output("git config --global user.name patch".split(" ")))

args = parser.parse_args()

my_env = os.environ.copy()

for pr in PRS_TO_ADD:
    pr = str(pr)
    org = "godotengine"
    parts = pr.split("/")
    if len(parts) == 2:
       org = parts[0]
       pr = parts[1]

    url = "https://github.com/" + org + "/godot/pull/" + str(pr) + ".patch"
    print(f"Fetching {url} for patch.")
    contents = urllib.request.urlopen(url).read()
    p = Popen(['git', 'am'], stdout=PIPE, stdin=PIPE, stderr=STDOUT, env=my_env)
    out = p.communicate(input=contents)[0]
    print(out.decode('utf-8'))
    if p.returncode != 0:
       sys.exit(1)

if args.push:
    print(check_output("git push -f git@github.com:basicer/godot HEAD:patched".split(" ")))

print("Jobs done")

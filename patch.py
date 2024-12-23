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
parser.add_argument('--no-patches', action='store_true', help='Dont download and apply patches')

run_no = os.environ.get('GITHUB_RUN_NUMBER', 0)


PRS_TO_ADD = [
    'basicer/4', # Revert TBN fixes.
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

if not args.no_patches:
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

cwd = check_output(["git","rev-parse","--show-toplevel"]).decode("ascii").strip()

def modify_lines_in_file(file, modify):
	with open(file, mode='r+') as h:
		h.seek(0)
		lines = [modify(x) for x in h.readlines()]
		result = ''.join(lines)
		h.seek(0)
		h.write(result)
		h.truncate()

def modify_mirror(x: str):
	x = x.replace('"https://godotengine.org/mirrorlist/" + current_version + ".json"', '"https://raw.githubusercontent.com/basicer/godot-build/refs/heads/main/mirrors.json"')
	return x

modify_lines_in_file(f'{cwd}/editor/export/export_template_manager.cpp', modify_mirror)

def modify_version(x: str):
	[key,value] = x.split(" = ")
	if key == "status":
		x = 'status = "basicer%03d"\n' % (int(run_no))
	return x

modify_lines_in_file(f'{cwd}/version.py', modify_version)

print(check_output('git commit -a -m Patch'.split(" ")))

print("Jobs done")

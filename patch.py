import sys
import os
import urllib.request
from subprocess import check_output, Popen, PIPE, STDOUT

PRS_TO_ADD = [
    91263,
    95788,
    91884,
    96897, # Resource Preview request_draw_and_wait
    96904, # Fix import deadlock
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


my_env = os.environ.copy()

for pr in PRS_TO_ADD:
    pr = str(pr)
    org = "godotengine"
    parts = pr.split("/")
    if len(parts) == 2:
       org = parts[0]
       pr = parts[1]

    url = "https://github.com/" + org + "/godot/pull/" + str(pr) + ".patch"
    print(url)
    contents = urllib.request.urlopen(url).read()
    p = Popen(['git', 'am'], stdout=PIPE, stdin=PIPE, stderr=STDOUT, env=my_env)
    out = p.communicate(input=contents)[0]
    print(out.decode('utf-8'))
    if p.returncode != 0:
       sys.exit(1)

print("Jobs done")

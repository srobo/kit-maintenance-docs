#!/usr/bin/env python

import argparse
import json
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('mount_point', metavar='MOUNT_POINT')
args = parser.parse_args()

with open("{}/mode.json".format(args.mount_point)) as f:
    data = json.load(f)
    print(data)

    if data["zone"] not in range(4):
         exit("invalid zone")
    if data["arena"] != "B":
        exit("invalid arena")

print("Pass")

subprocess.check_call(['umount', args.mount_point])

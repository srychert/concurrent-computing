# -*- coding: utf-8 -*-
import argparse
import os
import sys

parser = argparse.ArgumentParser(
    description='Fork searching')
parser.add_argument('--p', type=str, help='File path to begin search')
parser.add_argument('--s', type=str, help='Word to search for')

args = parser.parse_args()

if (args.p is None):
    exit("'--p' flag not found")

if (args.s is None):
    exit("'--s' flag not found")

# rozgałęziamy proces
pid = os.fork()

print(pid)
import os
import sys
sys.path.insert(0, os.getcwd())

import re
import argparse
import pprint
import logging

from source.common import TagInspector

def parse_args():
	ap = argparse.ArgumentParser()

	ap.add_argument('-p', dest='pattern', default='(.*)',
		help='The pattern, in Python regex format')
	ap.add_argument('-r', dest='replacement', default=r'\1',
		help='The replacement, in Python regex format')
	ap.add_argument('-w', dest='commit_changes', action='store_const', const=True,
		default=False, help='Must be specified for changes to be committed')
	ap.add_argument('file_list', type=str, nargs='+',
		help='The list of files to process')

	return ap.parse_args()

def apply_substitution(pat, rep, file_list, dry_run=True):
	if len(file_list) == 0:
		raise RuntimeError("No files specified.")

	file_list  = [TagInspector(f) for f in file_list]
	pat        = re.compile(pat)
	get_change = lambda f: (f.name, pat.sub(rep, f.name))
	changes    = {f : get_change(f) for f in file_list}

	pprint.PrettyPrinter(width=180).pprint(changes)

	if dry_run:
		print("Terminating dry run (rerun with '-w' to commit changes).")
		return

	for f, names in changes.items():
		try:
			f.name = names[1]
		except:
			logging.exception(f"Error while processing {f}.")

if __name__ == '__main__':
	args = parse_args()
	apply_substitution(args.pattern, args.replacement, args.file_list, not args.commit_changes)

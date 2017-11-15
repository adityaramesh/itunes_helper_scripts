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

	ap.add_argument('-b', dest='base_index', type=int, default=1,
		help='Index from which to start the new numbering scheme')
	ap.add_argument('-w', dest='commit_changes', action='store_const', const=True,
		default=False, help='Must be specified for changes to be committed')
	ap.add_argument('target_dir', type=str, help='The directory of files to reindex')

	return ap.parse_args()

def reindex_directory(target_dir, base_index, dry_run=True):
	rel_path  = lambda f: os.path.join(target_dir, f)
	file_list = [f for f in os.listdir(target_dir) if os.path.isfile(rel_path(f))]

	if len(file_list) == 0:
		raise RuntimeError("Directory contains no files to process.")

	file_list = [TagInspector(rel_path(f)) for f in file_list]
	file_list = sorted(file_list, key=lambda f: f.track_info[0])
	new_track_info = lambda off: (off + base_index, base_index + len(file_list) - 1)

	for i, f in enumerate(file_list):
		print(f, f.track_info, new_track_info(i))

	if dry_run:
		print("Terminating dry run (rerun with '-w' to commit changes).")
		return

	for i, f in enumerate(file_list):
		f.track_info = new_track_info(i)

if __name__ == '__main__':
	args = parse_args()
	reindex_directory(args.target_dir, args.base_index, not args.commit_changes)

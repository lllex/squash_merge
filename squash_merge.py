#!/usr/bin/env python2.7

import sys
from subprocess import check_call, check_output
from argparse import ArgumentParser

#------------------------------------------------------------------------------

def parse_commandline():
    parser = ArgumentParser(description='merge with squash branch1 to branch2')
    parser.add_argument(dest='branch1',
                        help='branch that will be merged')
    parser.add_argument(dest='branch2',
                        help='merge destination branch')
    args = parser.parse_args()
    return args

#------------------------------------------------------------------------------

def get_last_commit_msg():
    return check_output('git log -1 --format=%s', shell=True).rstrip()

#------------------------------------------------------------------------------

def main():
    args = parse_commandline()
    check_call('git checkout %s' % args.branch2, shell=True)

    # check if already merged
    SQUASH_COMMIT_MSG = "merge(squash) branch"
    last_commit_msg = get_last_commit_msg()
    if last_commit_msg.startswith(SQUASH_COMMIT_MSG):
        last_merged_branch = last_commit_msg.split()[-1]
        if last_merged_branch == args.branch1:
            check_call('git reset --hard HEAD~', shell=True)

    check_call('git merge --squash %s' % args.branch1, shell=True)
    check_call('git commit -m "%s %s"' % (SQUASH_COMMIT_MSG, args.branch1), shell=True)

#------------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(main())

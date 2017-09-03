#!/usr/bin/env python2.7

import sys
from subprocess import check_call, check_output

SQUASH_COMMIT_MSG = "merge(squash) branch"

#------------------------------------------------------------------------------

def get_last_commit_msg():
    return check_output('git log -1 --format=%s', shell=True).rstrip()

#------------------------------------------------------------------------------

def main():
    branch1, branch2 = sys.argv[1:3]

    check_call('git checkout %s' % branch2, shell=True)

    # check if already merged
    last_commit_msg = get_last_commit_msg()
    if last_commit_msg.startswith(SQUASH_COMMIT_MSG):
        last_merged_branch = last_commit_msg.split()[-1]
        if last_merged_branch == branch1:
            check_call('git reset --hard HEAD~', shell=True)

    check_call('git merge --squash %s' % branch1, shell=True)
    check_call('git commit -m "%s %s"' % (SQUASH_COMMIT_MSG, branch1), shell=True)

#------------------------------------------------------------------------------

if __name__ == "__main__":
    sys.exit(main())

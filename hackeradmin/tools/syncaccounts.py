#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import sys
import pwd
import json
import sets
import shutil
import argparse


MANAGED_UID_RANGE = (10000, 20000)

class Config:
    dry_run = False

def shell(cmd):
    if Config.dry_run:
        print(cmd)
    else:
        os.system(cmd)

def check_username_matches_pid(account):
    uid = account['uid']
    try:
        u = pwd.getpwuid(uid)
        if u.pw_name != account['username']:
            return False, "Uid %d has username %s on system, but hackeradmin wants username %s" % (uid, u.pw_name, account['username'])
    except KeyError:
        # UID not found
        try:
            u = pwd.getpwnam(account['username'])
            # Username exists, but must have different PID otherwise we'd seen it above
            return False, "Username %s exists, but with uid %d, while hackeradmin wants uid %d" % (u.pw_name, u.pw_uid, uid)
        except KeyError:
            # Username not found
            pass
    # Did not find uid nor username. That's okay.
    return True, None

def uid_exists(account):
    try:
        pwd.getpwuid(account['uid'])
        return True
    except KeyError:
        return False

def create_user(account):
    raise "not impl"

def name_matches(account):
    u = pwd.getpwuid(account['uid'])
    name = u.pw_gecos.split(',')[0]
    return name == account['name']

def update_name(account):
    shell('chfn -f "%s" %s' % (account['name'], account['username']))

def ensure_dir(dir, uid):
    if not os.path.isdir(dir):
        os.makedirs(dir)
    fd = os.open(dir, os.O_RDONLY)
    os.fchown(fd, uid, -1)
    os.close(fd)

def authorized_keys_contains_key(account):
    keyfile = os.path.expanduser("~%s/.ssh/authorized_keys" % account["username"])
    desired = sets.ImmutableSet(key.strip() for key in account['authorized_keys'].split("\n"))
    found = sets.ImmutableSet()
    if os.path.isfile(keyfile):
        with open(keyfile) as f:
            found = sets.ImmutableSet(line.strip() for line in f.readlines())
    return desired.issubset(found)

def add_authorized_key(account):
    keyfile = os.path.expanduser("~%s/.ssh/authorized_keys" % account["username"])
    keys = sets.Set(key.strip() for key in account['authorized_keys'].split("\n"))
    if os.path.isfile(keyfile):
        with open(keyfile) as f:
            for line in f.readlines():
                keys.add(line.strip())
    else:
        if not Config.dry_run:
            ensure_dir(os.path.expanduser("~%s/.ssh" % account["username"]), account["uid"])
    if not Config.dry_run:
        with open(keyfile, "w") as f:
            for key in keys:
                f.write(key + "\n")
        fd = os.open(keyfile, os.O_RDONLY)
        os.fchmod(fd, 0644)
        os.close(fd)

def login_shell_is_enabled(account):
    u = pwd.getpwuid(account['uid'])
    return u.pw_shell != "/bin/false"

def enable_login_shell(account):
    # FIXME store preferred shell somewhere?
    shell("chsh -s /bin/bash %s" % account["username"])

def synchronize_accounts(accounts):
    results = []
    for account in accounts:
        uid = account['uid']
        ok, err = check_username_matches_pid(account)
        if not ok:
            results.append({ 'uid' : uid, 'status' : 'username_uid_mismatch', 'error' : err })
            continue
        if not uid_exists(account):
            create_user(account)
            results.append({ 'uid' : uid, 'status' : 'user_created' })
            continue
        if not name_matches(account):
            update_name(account)
            results.append({ 'uid' : uid, 'status' : 'user_description_updated' })
        if not authorized_keys_contains_key(account):
            add_authorized_key(account)
            results.append({ 'uid' : uid, 'status' : 'ssh_key_added' })
        if not login_shell_is_enabled(account):
            enable_login_shell(account)
            results.append({ 'uid' : uid, 'status' : 'login_shell_enabled' })
    return results

def detect_unmanaged_logins(accounts):
    known_accounts = sets.ImmutableSet(a['uid'] for a in accounts)
    results = []
    for u in pwd.getpwall():
        uid = u.pw_uid
        if uid < MANAGED_UID_RANGE[0] or uid > MANAGED_UID_RANGE[1]:
            continue
        if uid not in known_accounts:
            results.append({ 'uid' : uid, 'err' : 'Spurious UID on system in managed UID range that is not known by hackeradmin' })
    return results

def main():
    parser = argparse.ArgumentParser(description='Synchronize Unix users on local system based on hackeradmin Unix account snapshot')
    parser.add_argument('accounts', help='JSON file with Unix accounts')
    parser.add_argument('--dry-run', help='Compute all desired changes, but do not modify the system', action='store_true')

    args = parser.parse_args()

    Config.dry_run = args.dry_run

    if not os.path.isfile(args.accounts):
        print >>sys.stderr, "Error: %s is not a readable file" % args.accounts
        sys.exit(1)

    with open(args.accounts) as f:
        accounts = json.load(f)
        results = []
        results = synchronize_accounts(accounts)
        results = results + detect_unmanaged_logins(accounts)
        print(results)

if __name__ == '__main__':
    main()

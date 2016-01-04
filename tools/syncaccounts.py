#! /usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import re
import sys
import pwd
import json
import sets
import time
import base64
import shutil
import urllib
import urllib2
import argparse
import traceback
import ConfigParser

MANAGED_UID_RANGE = (10000, 20000)
SSH_AUTHORIZED_KEYS_PATH = "/etc/ssh/user_keys/%s.pub"

class Config:
    dry_run = False

def shell(cmd):
    if Config.dry_run:
        print(cmd)
        return True
    else:
        return os.system(cmd) == 0

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

def validate(string, legal_chars):
    p = re.compile(ur"^[%s]*$" % legal_chars, re.UNICODE)
    if p.match(string):
        return string
    return None

def validate_name(name):
    return validate(name, u"a-zA-Z0-9äöüÄÖÜæøåÆØÅáéóàèòâêô\- ")

def validate_username(username):
    return validate(username, u"a-z")

def validate_uid(uid):
    if uid >= MANAGED_UID_RANGE[0] and uid <= MANAGED_UID_RANGE[1]:
        return uid
    return None

def create_user(account):
    if not validate_username(account['username']):
        return False, "Username contains bad characters"
    if not validate_name(account['name']):
        return False, "Name contains bad characters"
    if not validate_uid(account['uid']):
        return False, "Uid is outside managed range"
    if not shell('adduser %s --disabled-password --gecos "%s,,," --uid %d' % (account['username'], account['name'], account['uid'])):
        return False, "Adduser invocation failed"
    if not add_authorized_key(account):
        return False, "Failed to add SSH keys"
    return True, None

def name_matches(account):
    u = pwd.getpwuid(account['uid'])
    name = u.pw_gecos.split(',')[0]
    return name == account['name']

def update_name(account):
    if not validate_name(account['name']):
        return False, "New name contains bad characters"
    if not validate_username(account['username']):
        return False, "Username contains bad characters"
    if not shell('chfn -f "%s" %s' % (account['name'], account['username'])):
        return False, "Failed to execute chfn"
    return True, None

def ensure_dir(dir, uid):
    if not os.path.isdir(dir):
        os.makedirs(dir)
    fd = os.open(dir, os.O_RDONLY)
    os.fchown(fd, uid, -1)
    os.close(fd)

def authorized_keys_contains_key(account):
    keyfile = SSH_AUTHORIZED_KEYS_PATH % account['username']
    desired = sets.ImmutableSet(key.strip() for key in account['authorized_keys'].split("\n"))
    found = sets.ImmutableSet()
    if os.path.isfile(keyfile):
        with open(keyfile) as f:
            found = sets.ImmutableSet(line.strip() for line in f.readlines())
    return desired.issubset(found)

def add_authorized_key(account):
    keyfile = SSH_AUTHORIZED_KEYS_PATH % account['username']
    keys = sets.Set(key.strip() for key in account['authorized_keys'].split("\n"))
    if not Config.dry_run:
        dir = os.path.dirname(keyfile)
        if not os.path.isdir(dir):
            os.makedirs(dir)
        with open(keyfile, "w") as f:
            for key in keys:
                f.write(key + "\n")
        fd = os.open(keyfile, os.O_RDONLY)
        os.fchmod(fd, 0600)
        os.close(fd)
        return True, None
    else:
        print("Add SSH key for user %s to %s " % (account['username'], keyfile))
        return True, None

def login_shell_is_enabled(account):
    u = pwd.getpwuid(account['uid'])
    return u.pw_shell != "/bin/false"

def enable_login_shell(account):
    # FIXME store preferred shell somewhere?
    if not shell("chsh -s /bin/bash %s" % account["username"]):
        return False, "Failed to execute chsh"
    return True, None

def report(uid, code, error=None):
    if error:
        return { 'uid' : uid, 'status' : 'fail', 'code' : code, 'timestamp' : int(time.time()), 'error' : error }
    else:
        return { 'uid' : uid, 'status' : 'ok', 'code' : code, 'timestamp' : int(time.time()) }

def synchronize_accounts(accounts):
    results = []
    for account in accounts:
        uid = account['uid']
        ok, err = check_username_matches_pid(account)
        if not ok:
            results.append(report(uid, 'username_uid_mismatch', err))
            continue
        if not uid_exists(account):
            ok, err = create_user(account)
            if ok:
                results.append(report(uid, 'user_created'))
            else:
                results.append(report(uid, 'user_creation_failed', err))
            continue
        if not name_matches(account):
            ok, err = update_name(account)
            if ok:
                results.append(report(uid, 'user_description_updated'))
            else:
                results.append(report(uid, 'name_modification_failed', err))
        if not authorized_keys_contains_key(account):
            ok, err = add_authorized_key(account)
            if ok:
                results.append(report(uid, 'ssh_key_added'))
            else:
                results.append(report(uid, 'ssh_key_modification_failed', err))
        if not login_shell_is_enabled(account):
            ok, err = enable_login_shell(account)
            if ok:
                results.append(report(uid, 'login_shell_enabled'))
            else:
                results.append(report(uid, 'login_shell_enabling_failed', err))
    return results

def detect_unmanaged_logins(accounts):
    known_accounts = sets.ImmutableSet(a['uid'] for a in accounts)
    results = []
    for u in pwd.getpwall():
        uid = u.pw_uid
        if uid < MANAGED_UID_RANGE[0] or uid > MANAGED_UID_RANGE[1]:
            continue
        if uid not in known_accounts:
            results.append(report(uid, 'spurious_user', 'Uid %d (%s) is in managed range, but not known by hackeradmin' % (u.pw_uid, u.pw_name)))
    return results

def slurp(url, params={}, headers={}):
  params = urllib.urlencode(params, doseq=True)
  request = urllib2.Request(url)
  for (k,v) in headers.iteritems():
    request.add_header(k, v)
  response = urllib2.urlopen(request)
  content = response.read()
  response.close()
  return content

def cmd_file(filename):
    if not os.path.isfile(filename):
        print >>sys.stderr, "Error: %s is not a readable file" % args.file
        sys.exit(1)

    results = []
    with open(filename) as f:
        accounts = json.load(f)
        results = synchronize_accounts(accounts)
        results = results + detect_unmanaged_logins(accounts)
    print(results)

def cmd_poll():
    cfgfile = os.path.expanduser("~/.hackeradmin/config")
    if not os.path.isfile(cfgfile):
        print >>sys.stderr, "Error: Missing configuration file ~/.hackeradmin/config"
        sys.exit(1)

    config = ConfigParser.ConfigParser()
    config.readfp(open(cfgfile))
    username = config.get("default", "api_user")
    password = config.get("default", "api_password")
    url = config.get("default", "base_url")

    basic_auth = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    doc = slurp(url + "/member/unixaccount", headers={ "Authorization" : "Basic %s" % basic_auth })
    accounts = json.loads(doc)
    results = []
    results = synchronize_accounts(accounts)
    results = results + detect_unmanaged_logins(accounts)
    print(results)

def main():
    parser = argparse.ArgumentParser(description='Synchronize Unix users on local system based on hackeradmin Unix account snapshot')
    parser.add_argument('-f', '--file', help='JSON file with Unix accounts')
    parser.add_argument('--poll', help="Pull Unix account snapshot from online", action='store_true')
    parser.add_argument('--dry-run', help='Compute all desired changes, but do not modify the system', action='store_true')

    args = parser.parse_args()

    Config.dry_run = args.dry_run

    if not (args.file or args.poll):
        parser.print_help()
        sys.exit(1)

    try:
        if args.file:
            cmd_file(args.file)
        elif args.poll:
            cmd_poll()
    except:
        print([{"status" : "fail", "err" : traceback.format_exc()}])

if __name__ == '__main__':
    main()


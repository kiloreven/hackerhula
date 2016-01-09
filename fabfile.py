from fabric.api import env, run, cd, hosts, settings, sudo, local, lcd
import os, sys, pprint, subprocess

def test():
    run_testsuite()

def run_testsuite():
    cmd = ["git", "rev-parse", "--show-toplevel"]
    topdir = subprocess.check_output(cmd, stderr=subprocess.STDOUT).strip()
    with lcd(os.path.join(topdir, "hackerhula")):
        local("./manage.py test")

def lint():
    cmd = ["git", "rev-parse", "--show-toplevel"]
    topdir = subprocess.check_output(cmd, stderr=subprocess.STDOUT).strip()
    cmd = ["pylint", "--rcfile=" + topdir + "/pylint.rc", "--errors-only", "*py"]
    local(" ".join(cmd))

@hosts('webapp-hackerhula@blade.hackeriet.no')
def deploy():
    run_testsuite()
    # send upstream foerst, kjipt aa ha divergerende tre.
    #local("git push origin HEAD")

    with settings(warn_only=True):
        if run("test -d hackerhula").failed:
            run("git clone https://github.com/hackeriet/hackerhula.git")

    with cd("hackerhula"):
        run("git pull")
        run("git checkout master")
        #run('hackerhula/manage.py collectstatic --noinput')
        run('hackerhula/manage.py syncdb --noinput')
        run('hackerhula/manage.py migrate --noinput')
        run('./deploy-crontab')
    run('touch .reload')

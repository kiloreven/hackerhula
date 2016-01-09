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

@hosts("webapp-hackerhula@blade.hackeriet.no")
def deploy():
    run_testsuite()

    local("git push origin HEAD")

    with settings(warn_only=True):
        if run("test -d hackerhula").failed:
            run("git clone https://github.com/hackeriet/hackerhula.git")
            run("cd hackerhula/hackerhula/hackerhula && ln -s $HOME/config/localsettings.py")

    with settings(warn_only=True):
        if run("test -d venv").failed:
            run("virtualenv --system-site-packages venv")
            run("venv/bin/pip install --quiet -r hackerhula/requirements.txt")

    with cd("hackerhula"):
        run("git pull")
        run("git checkout master")
        run("../venv/bin/python hackerhula/manage.py collectstatic --noinput")
        run("../venv/bin/python hackerhula/manage.py migrate --noinput")
        run("./deploy-crontab")
    run("touch .reload")

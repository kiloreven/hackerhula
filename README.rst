Administrative interface for Hackeriet
======================================

Glorified spreadsheet to manage:

* members.
* membership payment status.
* physical keys.


Development setup
-----------------

::
    git clone ..
    sudo apt-get install python-virtualenv python-pil
    virtualenv --system-site-packages venv
    . ./venv/bin/activate
    pip install -r requirements.txt
    cd hackeradmin
    ./manage.py syncdb
    ./manage.py migrate
    # Populate with some fake members.
    ./manage.py loaddata member/fixtures/small_memberset.json
    ./manage.py runserver


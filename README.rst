Hula - Administrative interface for Hackeriet
=============================================

Glorified spreadsheet to manage:

* members.
* membership payment status.
* physical keys.


Development setup
-----------------

This is how you get going::

  git clone ..
  sudo apt-get install python-virtualenv python-pil python-psycopg2
  virtualenv --system-site-packages venv
  . ./venv/bin/activate
  pip install -r requirements.txt
  cd hackerhula
  ./manage.py syncdb
  ./manage.py migrate
  # Populate with some fake members.
  ./manage.py loaddata member/fixtures/small_memberset.json
  ./manage.py runserver



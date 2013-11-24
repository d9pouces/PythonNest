PythonNest
==========

Pypi mirror, with export / import functionnalities based on Django 1.5.

Installing
==========

As every Python package, you may use several ways to install PythonNest.
Python 3.3+ is required, with the following packages:

  * setuptools >= 0.7
  * django >= 1.5
  * South >= 0.8
  * rpc4django (warning! you must install django 1.5 until rpc4django is patched to support django 1.6)


From the source::

  $ cd PythonNest
  $ sudo python setup.py install

With easyinstall::

  $ sudo easy_install pythonnest

You can also use pip ::

  $ sudo pip install pythonnest

We strongly advise to use virtualenv and gunicorn to run your server.


Configuring
===========


PythonNest use a small configuration file named `pythonnest.ini`. Its location depends on the location of the package,
more precisely of the location of the `pythonnest.djangoproject.settings` package.

If the location is `/foo/bar/lib/baz/pythonnest/djangoproject/settings.py`, the configuration file is expected at
`/foo/bar/etc/pythonnest.ini`. Use `pythonnest-manage config` to display its exact location.

Its content is quite limited::

    [pythonnest]
    ROOT_PATH = /var/data/pythonnest  ; root path for all data files (static files like CSS, and python packages)
    HOST = http://localhost:8000/  ; complete URL of your package
    DEBUG = True
    ADMIN_EMAIL = flanker@19pouces.net
    TIME_ZONE = Europe/Paris
    LANGUAGE_CODE = fr-fr
    USE_XSENDFILE = False  ; if your mirror is behind a Apache with mod_xsendfile, use this option to increase perfs
    DATABASE_ENGINE = django.db.backends.sqlite3  ; 'postgresql_psycopg2', mysql', 'sqlite3' or 'oracle'
    DATABASE_NAME =  ; location of your sqlite db, or name of the sql database
    DATABASE_USER =
    DATABASE_PASSWORD =
    DATABASE_HOST =
    DATABASE_PORT =


Virtual environment
===================

To create a functionnal virtual env and launch the service::

  mkvirtualenv -p `which python3.3` pythonnest
  workon pythonnest
  pip install gunicorn pythonnest
  pythonnest-manage syncdb
  pythonnest-manage collectstatic
  gunicorn -b 0.0.0.0:8080 -D pythonnest.djangoproject.wsgi:application


[TODO]
- rss feeds
- administration view (delete packages/versions/files)
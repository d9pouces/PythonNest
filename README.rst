PythonNest
==========

Pypi mirror, with advanced export / import functionnalities compared to other Pypi mirrors.

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
  $ sudo python setup.py install  # global installation
  $ python setup.py install --user  # installation without root access

With easyinstall::

  $ sudo easy_install pythonnest

You can also use pip ::

  $ sudo pip install pythonnest  # global installation
  $ pip install pythonnest --user  # installation without root access

We strongly advise to use virtualenv and gunicorn to run your server.


Configuring
===========


PythonNest uses a small configuration file named `pythonnest.ini`. Its location depends on the location of the package,
more precisely on the location of the `pythonnest.djangoproject.settings` file.

If the location is `/foo/bar/lib/baz/pythonnest/djangoproject/settings.py`, then the configuration file is expected to
be `/foo/bar/etc/pythonnest.ini`. Use `pythonnest-manage config` to display its exact location.

Its content is quite limited::

    [pythonnest]
    ; root path for all data files (static files like CSS, and python packages)
    ROOT_PATH = /var/data/pythonnest
    ; full URI of your repository
    HOST = http://localhost:8000/
    DEBUG = True
    ADMIN_EMAIL = admin@localhost
    TIME_ZONE = Europe/Paris
    LANGUAGE_CODE = fr-fr
    ; if your mirror is behind a Apache with mod_xsendfile, use this option to increase perfs
    USE_XSENDFILE = false
    ; 'postgresql_psycopg2', mysql', 'sqlite3' or 'oracle'
    DATABASE_ENGINE = django.db.backends.sqlite3
    ; location of your sqlite db, or name of the sql database
    DATABASE_NAME =
    DATABASE_USER =
    DATABASE_PASSWORD =
    DATABASE_HOST =
    DATABASE_PORT =

The package `mysql` seems to be a bit broken with Python 3.3, or at least cannot be directely installed with `pip`.

Virtual environment
===================

To create a functionnal virtual env and launch the service through gunicorn (assuming mkvirtual is installed) ::

  VIRTUALENV=pythonnest
  mkvirtualenv -p `which python3.3` $VIRTUALENV
  workon $VIRTUALENV
  pip install gunicorn pythonnest
  pythonnest-manage config
  [modify the configuration file]
  pythonnest-manage syncdb
  pythonnest-manage collectstatic
  gunicorn -b 0.0.0.0:8080 -D pythonnest.djangoproject.wsgi:application


Dumping an existing mirror
==========================

You can populate your mirror by copying an existing mirror such as pypi.python.org::

  workon $VIRTUALENV
  pythonnest-manage update [--url http://pypi.python.org/pypi] [--init-all] [-h]

The source mirror must implement the XML-RPC API (of course, pypi.python.org does).
You have to download around 10 GB to dump an official Pypi mirror if you restrict yourself to the last version of the
downloaded packages.


Exporting and exporting data
============================

If you want to maintain an offline repository, you need two PythonNest instances, the first one being able to run
the `update` command::

  workon $VIRTUALENV
  pythonnest-manage export [--path <path_you_want_to_export_data_to>] [--tag <tag_to_identify_this_export>] \
    [--serial <serial>]

All packages imported into PythonNest (through `update` or `import` command, or added by users) are associated to
a unique serial. The export command stores the last exported serial associated to the given tag. By default,
the export starts to export data from the last stored serial.
If you only want to dump an existing mirror and export collected data, you can delete the directory
$ROOT_PATH/media/downloads after the export without breaking the database (you only need to be sure that you wan't
export these files again!).

Importing data::

  workon $VIRTUALENV
  pythonnest manage import [--path <path_with_exported_data>] [--tag <tag_to_identify_this_import>] [--force]

Import all data previously exported by the other PythonNest instance. The last imported serial is stored into database,
so any missing import can be tracked (and further importations are forbidden, unless you specify the --force option).


The `tag` option allow to export data to/to import from different PythonNest instances.
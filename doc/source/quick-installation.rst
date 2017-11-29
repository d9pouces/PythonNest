Quick installation
==================

Pythonnest mainly requires Python (3.5, 3.6, 3.7).

You should create a dedicated virtualenvironment on your system to isolate Pythonnest.
You can use `pipenv <http://docs.python-guide.org/en/latest/dev/virtualenvs/>`_ or `virtualenvwrapper <https://virtualenvwrapper.readthedocs.io>`_.

For example, on Debian-based systems like Ubuntu:

.. code-block:: bash

    sudo apt-get install python3.6 python3.6-dev build-essential






If these requirements are fullfilled, then you can gon on and install Pythonnest:

.. code-block:: bash

    pip install pythonnest --user
    pythonnest-ctl collectstatic --noinput  # prepare static files (CSS, JS, …)
    pythonnest-ctl migrate  # create the database (SQLite by default)
    pythonnest-ctl createsuperuser  # create an admin user
    pythonnest-ctl check  # everything should be ok




You can easily change the root location for all data (SQLite database, uploaded or temp files, static files, …) by
editing the configuration file.

.. code-block:: bash

    CONFIG_FILENAME=`pythonnest-ctl config ini -v 2 | grep -m 1 ' - .ini file' | cut -d '"' -f 2`
    # prepare a limited configuration file
    mkdir -p `dirname $CONFIG_FILENAME`
    cat << EOF > $CONFIG_FILENAME
    [global]
    data = $HOME/pythonnest
    EOF

Of course, you must run again the `migrate` and `collectstatic` commands (or moving data to this new folder).




You can launch the server process:

.. code-block:: bash

    pythonnest-ctl server


Then open http://localhost:8130 with your favorite browser.



You can install Pythonnest in your home (with the `--user` option), globally (without this option), or (preferably)
inside a virtualenv.

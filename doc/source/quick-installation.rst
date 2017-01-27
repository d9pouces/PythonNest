Quick installation
==================

You can quickly test Pythonnest, storing all data in $HOME/pythonnest:

.. code-block:: bash

    sudo apt-get install python3.5 python3.5-dev build-essential
    pip install pythonnest
    pythonnest-manage migrate  # create the database (SQLite by default)
    pythonnest-manage collectstatic --noinput  # prepare static files (CSS, JS, …)
    pythonnest-manage createsuperuser  # create an admin user



You can easily change the root location for all data (SQLite database, uploaded or temp files, static files, …) by
editing the configuration file:

.. code-block:: bash

    CONFIG_FILENAME=`pythonnest-manage  config ini -v 2 | head -n 1 | grep ".ini" | cut -d '"' -f 2`
    # create required folders
    mkdir -p `dirname $FILENAME` $HOME/pythonnest
    # prepare a limited configuration file
    cat << EOF > $FILENAME
    [global]
    data = $HOME/pythonnest
    EOF

Of course, you must run again the `migrate` and `collectstatic` commands (or moving data to this new folder).


You can launch the server processes (the second process is required for background tasks):

.. code-block:: bash

    pythonnest-gunicorn
     worker -Q celery


Then open http://localhost:9000 in your favorite browser.

You should use virtualenv or install Pythonnest using the `--user` option.
Complete configuration
======================

You can look current settings with the following command::

    pythonnest-manage config

Here is the complete list of settings::

    [global]
    server_name = pythonnest.example.org
    protocol = https
    bind_address = 127.0.0.1:9000
    data_path = /var/pythonnest
    admin_email = admin@example.org
    time_zone = Europe/Paris
    language_code = fr-fr
    x_send_file =  true
    x_accel_converter = false
    debug = false

    [database]
    engine =
    name =
    user =
    password =
    host =
    port =

If you need more complex settings, you can override default values (given in `djangofloor.defaults` and
`pythonnest.defaults`) by creating a file named `[prefix]/etc/pythonnest/settings.py`.

Valid engines for your database are:

  - `django.db.backends.sqlite3` (use `name` option for its filepath)
  - `django.db.backends.postgresql_psycopg2`
  - `django.db.backends.mysql`
  - `django.db.backends.oracle`

Use `x_send_file` with Apache, and `x_accel_converter` with nginx.

Debugging
---------

If something does not work as expected, you can look at logs (in /var/log/supervisor if you use supervisor)
or try to run the server interactively:

.. code-block:: bash

  sudo service supervisor stop
  sudo -u pythonnest -i
  workon pythonnest
  pythonnest-manage runserver
  pythonnest-gunicorn

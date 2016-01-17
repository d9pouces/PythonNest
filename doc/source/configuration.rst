Complete configuration
======================

You can look current settings with the following command:

.. code-block:: bash

    pythonnest-manage config

Here is the complete list of settings:

.. code-block:: ini

  [database]
  engine = django.db.backends.postgresql_psycopg2
  # SQL database engine, can be 'django.db.backends.[postgresql_psycopg2|mysql|sqlite3|oracle]'.
  host = localhost
  # Empty for localhost through domain sockets or "127.0.0.1" for localhost + TCP
  name = pythonnest
  # Name of your database, or path to database file if using sqlite3.
  password = 5trongp4ssw0rd
  # Database password (not used with sqlite3)
  port = 5432
  # Database port, leave it empty for default (not used with sqlite3)
  user = pythonnest
  # Database user (not used with sqlite3)
  [global]
  admin_email = admin@pythonnest.example.org
  # error logs are sent to this e-mail address
  bind_address = localhost:8130
  # The socket (IP address:port) to bind to.
  data_path = /var/pythonnest
  # Base path for all data
  debug = False
  # A boolean that turns on/off debug mode.
  language_code = fr-FR
  # A string representing the language code for this installation.
  protocol = http
  # Protocol (or scheme) used by your webserver (apache/nginx/…, can be http or https)
  secret_key = ap6WerC2w8c6SGCPvFM5YDHdTXvBnzHcToS0J3r6LeetzReng6
  # A secret key for a particular Django installation. This is used to provide cryptographic signing, and should be set to a unique, unpredictable value.
  server_name = pythonnest.example.org
  # the name of your webserver (should be a DNS name, but can be an IP address)
  time_zone = Europe/Paris
  # A string representing the time zone for this installation, or None. 



If you need more complex settings, you can override default values (given in `djangofloor.defaults` and
`pythonnest.defaults`) by creating a file named `[prefix]/etc/pythonnest/settings.py`.

Valid engines for your database are:

  - `django.db.backends.sqlite3` (use the `name` option for its filepath)
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

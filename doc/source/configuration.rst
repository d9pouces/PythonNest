
Complete configuration
======================


Configuration options
---------------------

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
  extra_apps = 
  # List of extra installed Django apps (separated by commas).
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
  [sentry]
  dsn_url = 
  # Sentry URL to send data to. https://docs.getsentry.com/



If you need more complex settings, you can override default values (given in `djangofloor.defaults` and
`pythonnest.defaults`) by creating a file named `/home/pythonnest/.virtualenvs/pythonnest/etc/pythonnest/settings.py`.



Debugging
---------

If something does not work as expected, you can look at logs (in /var/log/supervisor if you use supervisor)
or try to run the server interactively:

.. code-block:: bash

  sudo service supervisor stop
  sudo -u pythonnest -i
  workon pythonnest
  pythonnest-manage config
  pythonnest-manage runserver
  pythonnest-gunicorn




Backup
------

A complete PythonNest installation is made a different kinds of files:

    * the code of your application and its dependencies (you should not have to backup them),
    * static files (as they are provided by the code, you can lost them),
    * configuration files (you can easily recreate it, or you must backup it),
    * database content (you must backup it),
    * user-created files (you must also backup them).

Many backup strategies exist, and you must choose one that fits your needs. We can only propose general-purpose strategies.

We use logrotate to backup the database, with a new file each day.

.. code-block:: bash

  sudo mkdir -p /var/backups/pythonnest
  sudo chown -r pythonnest: /var/backups/pythonnest
  sudo -u pythonnest -i
  cat << EOF > /home/pythonnest/.virtualenvs/pythonnest/etc/pythonnest/backup_db.conf
  /var/backups/pythonnest/backup_db.sql.gz {
    daily
    rotate 20
    nocompress
    missingok
    create 640 pythonnest pythonnest
    postrotate
    myproject-manage dumpdb | gzip > /var/backups/pythonnest/backup_db.sql.gz
    endscript
  }
  EOF
  touch /var/backups/pythonnest/backup_db.sql.gz
  crontab -e
  MAILTO=admin@pythonnest.example.org
  0 1 * * * /home/pythonnest/.virtualenvs/pythonnest/bin/pythonnest-manage clearsessions
  0 2 * * * logrotate -f /home/pythonnest/.virtualenvs/pythonnest/etc/pythonnest/backup_db.conf


Backup of the user-created files can be done with rsync, with a full backup each month:
If you have a lot of files to backup, beware of the available disk place!

.. code-block:: bash

  sudo mkdir -p /var/backups/pythonnest/media
  sudo chown -r pythonnest: /var/backups/pythonnest
  cat << EOF > /home/pythonnest/.virtualenvs/pythonnest/etc/pythonnest/backup_media.conf
  /var/backups/pythonnest/backup_media.tar.gz {
    monthly
    rotate 6
    nocompress
    missingok
    create 640 pythonnest pythonnest
    postrotate
    tar -C /var/backups/pythonnest/media/ -czf /var/backups/pythonnest/backup_media.tar.gz .
    endscript
  }
  EOF
  touch /var/backups/pythonnest/backup_media.tar.gz
  crontab -e
  MAILTO=admin@pythonnest.example.org
  0 3 * * * rsync -arltDE /var/pythonnest/data/media/ /var/backups/pythonnest/media/
  0 5 0 * * logrotate -f /home/pythonnest/.virtualenvs/pythonnest/etc/pythonnest/backup_media.conf

Restoring a backup
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

  cat /var/backups/pythonnest/backup_db.sql.gz | gunzip | /home/pythonnest/.virtualenvs/pythonnest/bin/pythonnest-manage dbshell
  tar -C /var/pythonnest/data/media/ -xf /var/backups/pythonnest/backup_media.tar.gz





Monitoring
----------


Nagios or Shinken
~~~~~~~~~~~~~~~~~

You can use Nagios checks to monitor several points:

  * connection to the application server (gunicorn or uwsgi):
  * connection to the database servers (PostgreSQL),
  * connection to the reverse-proxy server (apache or nginx),
  * the validity of the SSL certificate (can be combined with the previous check),
  * creation date of the last backup (database and files),
  * living processes for gunicorn, postgresql, apache,
  * standard checks for RAM, disk, swap…

Here is a sample NRPE configuration file:

.. code-block:: bash

  cat << EOF | sudo tee /etc/nagios/nrpe.d/pythonnest.cfg
  command[pythonnest_wsgi]=/usr/lib/nagios/plugins/check_http -H localhost -p 8130
  command[pythonnest_database]=/usr/lib/nagios/plugins/check_tcp -H localhost -p 5432
  command[pythonnest_reverse_proxy]=/usr/lib/nagios/plugins/check_http -H pythonnest.example.org -p 80 -e 401
  command[pythonnest_backup_db]=/usr/lib/nagios/plugins/check_file_age -w 172800 -c 432000 /var/backups/pythonnest/backup_db.sql.gz
  command[pythonnest_backup_media]=/usr/lib/nagios/plugins/check_file_age -w 3024000 -c 6048000 /var/backups/pythonnest/backup_media.sql.gz
  command[pythonnest_gunicorn]=/usr/lib/nagios/plugins/check_procs -C python -a '/home/pythonnest/.virtualenvs/pythonnest/bin/pythonnest-gunicorn'
  EOF

Sentry
~~~~~~

For using Sentry to log errors, you must add `raven.contrib.django.raven_compat` to the installed apps.

.. code-block:: ini

  [global]
  extra_apps = raven.contrib.django.raven_compat
  [sentry]
  dsn_url = https://[key]:[secret]@app.getsentry.com/[project]

Of course, the Sentry client (Raven) must be separately installed, before testing the installation:

.. code-block:: bash

  sudo -u pythonnest -i
  pythonnest-manage raven test





LDAP groups
-----------

There are two possibilities to use LDAP groups, with their own pros and cons:

  * on each request, use an extra LDAP connection to retrieve groups instead of looking in the SQL database,
  * regularly synchronize groups between the LDAP server and the SQL servers.

The second approach can be used without any modification in your code and remove a point of failure
in the global architecture (if you allow some delay during the synchronization process).
A tool exists for such synchronization: `MultiSync <https://github.com/d9pouces/Multisync>`_.

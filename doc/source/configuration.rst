
Complete configuration
======================


Configuration options
---------------------

You can look current settings with the following command:

.. code-block:: bash

    pythonnest-manage config ini -v 2

You can also display the actual list of Python settings

.. code-block:: bash

    pythonnest-manage config python -v 2


Here is the complete list of settings:

.. code-block:: ini

  [database]
  db = django_data/database.sqlite3 
  	# Main database name (or path of the sqlite3 database)
  engine = sqlite3 
  	# Main database engine ("mysql", "postgresql", "sqlite3", "oracle", or the dotted name of the Django backend)
  host =  
  	# Main database host
  password =  
  	# Main database password
  port =  
  	# Main database port
  user =  
  	# Main database user
  
  [email]
  host = localhost 
  	# SMTP server
  password =  
  	# SMTP password
  port = 25 
  	# SMTP port (often 25, 465 or 587)
  use_ssl = False 
  	# "true" if your SMTP uses SSL (often on port 465)
  use_tls = False 
  	# "true" if your SMTP uses STARTTLS (often on port 587)
  user =  
  	# SMTP user
  
  [global]
  admin_email = admin@localhost 
  	# e-mail address for receiving logged errors
  data = ./django_data 
  	# where all data will be stored (static/uploaded/temporary files, …)If you change it, you must run the collectstatic and migrate commands again.
  language_code = fr-FR 
  	# default to fr_FR
  listen_address = localhost:9000 
  	# address used by your web server.
  log_remote_url =  
  	# Send logs to a syslog or systemd log daemon.  
  	# Examples: syslog+tcp://localhost:514/user, syslog:///local7,syslog:///dev/log/daemon, logd:///project_name
  server_url = http://localhost:9000/ 
  	# Public URL of your website.  
  	# Default to "http://listen_address" but should be ifferent if you use a reverse proxy like Apache or Nginx. Example: http://www.example.org.
  time_zone = Europe/Paris 
  	# default to Europe/Paris
  



If you need more complex settings, you can override default values (given in `djangofloor.defaults` and
`pythonnest.defaults`) by creating a file named `/pythonnest/settings.py`.



Optional components
-------------------

Efficient page caching
~~~~~~~~~~~~~~~~~~~~~~

You just need to install `django-redis-sessions`. Settings are automatically changed for using a local Redis server (of course, you can change it in your config file).

.. code-block:: bash

  pip install django-redis-sessions

Faster session storage
~~~~~~~~~~~~~~~~~~~~~~

You just need to install `redis-sessions` for storing sessions into user sessions in Redis instead of storing them in the main database.
Redis is not designed to be backuped; if you loose your Redis server, sessions are lost and all users must login again.
However, Redis is faster than your main database server and sessions take a huge place if they are not regularly cleaned.
Settings are automatically changed for using a local Redis server (of course, you can change it in your config file).

.. code-block:: bash

  pip install redis-sessions

Optimized media files
~~~~~~~~~~~~~~~~~~~~~

You can use `Django-Pipeline <https://django-pipeline.readthedocs.io/en/latest/configuration.html>`_ to merge all media files (CSS and JS) for a faster site.

.. code-block:: bash

  pip install django-pipeline

Optimized JavaScript files are currently deactivated due to syntax errors in generated files (not my fault ^^).



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
   worker -Q celery




Backup
------

A complete Pythonnest installation is made a different kinds of files:

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
  cat << EOF > /etc/pythonnest/backup_db.conf
  /var/backups/pythonnest/backup_db.sql.gz {
    daily
    rotate 20
    nocompress
    missingok
    create 640 pythonnest pythonnest
    postrotate
    moneta-manage dumpdb | gzip > /var/backups/pythonnest/backup_db.sql.gz
    endscript
  }
  EOF
  touch /var/backups/pythonnest/backup_db.sql.gz
  crontab -e
  MAILTO=admin@localhost
  0 1 * * * pythonnest-manage clearsessions
  0 2 * * * logrotate -f /etc/pythonnest/backup_db.conf


Backup of the user-created files can be done with rsync, with a full backup each month:
If you have a lot of files to backup, beware of the available disk place!

.. code-block:: bash

  sudo mkdir -p /var/backups/pythonnest/media
  sudo chown -r pythonnest: /var/backups/pythonnest
  cat << EOF > /etc/pythonnest/backup_media.conf
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
  MAILTO=admin@localhost
  0 3 * * * rsync -arltDE django_data/media/ /var/backups/pythonnest/media/
  0 5 0 * * logrotate -f /etc/pythonnest/backup_media.conf

Restoring a backup
~~~~~~~~~~~~~~~~~~

.. code-block:: bash

  cat /var/backups/pythonnest/backup_db.sql.gz | gunzip | pythonnest-manage dbshell
  tar -C django_data/media/ -xf /var/backups/pythonnest/backup_media.tar.gz






LDAP groups
-----------

There are two possibilities to use LDAP groups, with their own pros and cons:

  * on each request, use an extra LDAP connection to retrieve groups instead of looking in the SQL database,
  * regularly synchronize groups between the LDAP server and the SQL servers.

The second approach can be used without any modification in your code and remove a point of failure
in the global architecture (if you can afford regular synchronizations instead of instant replication).
At least one tool exists for such synchronization: `MultiSync <https://github.com/d9pouces/Multisync>`_.


Complete configuration
======================


Configuration options
---------------------

You can look current settings with the following command:

.. code-block:: bash

    pythonnest-ctl config ini -v 2

You can also display the actual list of Python settings (for more complex tweaks):

.. code-block:: bash

    pythonnest-ctl config python -v 2


Here is the complete list of settings:

.. code-block:: ini

  [cache]
  db = 2 
  	# Database number of the Redis Cache DB. 
  	# Python package "django-redis" is required.
  host = localhost 
  	# Redis Cache DB host
  password =  
  	# Redis Cache DB password (if required)
  port = 6379 
  	# Redis Cache DB port
  
  [database]
  db = pythonnest 
  	# Main database name (or path of the sqlite3 database)
  engine = postgresql 
  	# Main database engine ("mysql", "postgresql", "sqlite3", "oracle", or the dotted name of the Django backend)
  host = localhost 
  	# Main database host
  password = 5trongp4ssw0rd 
  	# Main database password
  port = 5432 
  	# Main database port
  user = pythonnest 
  	# Main database user
  
  [email]
  from = admin@pythonnest.example.org 
  	# Displayed sender email
  host = localhost 
  	# SMTP server
  password =  
  	# SMTP password
  port = 25 
  	# SMTP port (often 25, 465 or 587)
  use_ssl = false 
  	# "true" if your SMTP uses SSL (often on port 465)
  use_tls = false 
  	# "true" if your SMTP uses STARTTLS (often on port 587)
  user =  
  	# SMTP user
  
  [global]
  admin_email = admin@pythonnest.example.org 
  	# e-mail address for receiving logged errors
  data = $DATA_ROOT 
  	# where all data will be stored (static/uploaded/temporary files, …). If you change it, you must run the collectstatic and migrate commands again.
  language_code = fr-fr 
  	# default to fr_FR
  listen_address = localhost:8130 
  	# address used by your web server.
  log_directory = $DATA_ROOT/log/ 
  	# Write all local logs to this directory.
  log_remote_access = true 
  	# If true, log of HTTP connections are also sent to syslog/logd
  log_remote_url =  
  	# Send logs to a syslog or systemd log daemon.  
  	# Examples: syslog+tcp://localhost:514/user, syslog:///local7, syslog:///dev/log/daemon, logd:///project_name
  read_only = true
  server_url = http://pythonnest.example.org 
  	# Public URL of your website.  
  	# Default to "http://{listen_address}/" but should be different if you use a reverse proxy like Apache or Nginx. Example: http://www.example.org/.
  ssl_certfile =  
  	# Public SSL certificate (if you do not use a reverse proxy with SSL)
  ssl_keyfile =  
  	# Private SSL key (if you do not use a reverse proxy with SSL)
  time_zone = Europe/Paris 
  	# default to Europe/Paris
  
  [server]
  processes = 2 
  	# The number of web server processes for handling requests.
  threads = 2 
  	# The number of web server threads for handling requests.
  timeout = 30 
  	# Web workers silent for more than this many seconds are killed and restarted.
  
  [sessions]
  db = 3 
  	# Database number of the Redis sessions DB 
  	# Python package "django-redis-sessions" is required.
  host = localhost 
  	# Redis sessions DB host
  password =  
  	# Redis sessions DB password (if required)
  port = 6379 
  	# Redis sessions DB port
  



If you need more complex settings, you can override default values (given in `djangofloor.defaults` and
`pythonnest.defaults`) by creating a file named `/pythonnest/settings.py`.



Optional components
-------------------

Efficient page caching
~~~~~~~~~~~~~~~~~~~~~~

You just need to install `django-redis`.
Settings are automatically changed for using a local Redis server (of course, you can change it in your config file).

.. code-block:: bash

  pip install django-redis

Faster session storage
~~~~~~~~~~~~~~~~~~~~~~

You just need to install `django-redis-sessions` for storing sessions into user sessions in Redis instead of storing them in the main database.
Redis is not designed to be backuped; if you loose your Redis server, sessions are lost and all users must login again.
However, Redis is faster than your main database server and sessions take a huge place if they are not regularly cleaned.
Settings are automatically changed for using a local Redis server (of course, you can change it in your config file).

.. code-block:: bash

  pip install django-redis-sessions



Debugging
---------

If something does not work as expected, you can look at logs (check the global configuration for determining their folder)
or try to run the server interactively:

.. code-block:: bash

  sudo service supervisor stop
  sudo -H -u pythonnest -i
  workon pythonnest
  pythonnest-ctl check
  pythonnest-ctl config ini
  pythonnest-ctl server


You can also enable the DEBUG mode which is more verbose (and displays logs to stdout):

.. code-block:: bash

  FILENAME=`easydemo-ctl config ini -v 2 | grep -m 1 ' - .ini file' | cut -d '"' -f 2 | sed  's/.ini$/.py/'`
  echo "DEBUG = True" >> $FILENAME
  pythonnest-ctl runserver




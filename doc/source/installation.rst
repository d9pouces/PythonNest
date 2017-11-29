Installation
============

Here is a simple tutorial to install Pythonnest on a basic Debian/Linux installation.
You should easily adapt it on a different Linux or Unix flavor.

Like many Python packages, you can use several methods to install Pythonnest.
Of course you can install it from source, but the preferred way is to install it as a standard Python package, via pip.


Upgrading
---------

If you want to upgrade an existing installation, just install the new version (with the `--upgrade` flag for `pip`) and run
the `collectstatic` and `migrate` commands (for updating both static files and the database).



Preparing the environment
-------------------------

.. code-block:: bash

    sudo adduser --disabled-password pythonnest
    sudo chown pythonnest:www-data $DATA_ROOT
    sudo apt-get install virtualenvwrapper python3.6 python3.6-dev build-essential postgresql-client libpq-dev
    sudo -u pythonnest -H -i
    mkvirtualenv pythonnest -p `which python3.6`
    workon pythonnest


Database
--------

PostgreSQL is often a good choice for Django sites:

.. code-block:: bash

   sudo apt-get install postgresql
   echo "CREATE USER pythonnest" | sudo -u postgres psql -d postgres
   echo "ALTER USER pythonnest WITH ENCRYPTED PASSWORD '5trongp4ssw0rd'" | sudo -u postgres psql -d postgres
   echo "ALTER ROLE pythonnest CREATEDB" | sudo -u postgres psql -d postgres
   echo "CREATE DATABASE pythonnest OWNER pythonnest" | sudo -u postgres psql -d postgres


Pythonnest can use Redis for caching pages and storing sessions:

.. code-block:: bash

    sudo apt-get install redis-server





Apache
------

Only the Apache installation is presented, but an installation behind nginx should be similar.
Only the chosen server name (like `pythonnest.example.org`) can be used for accessing your site. For example, you cannot use its IP address.



.. code-block:: bash

    SERVICE_NAME=pythonnest.example.org
    sudo apt-get install apache2 libapache2-mod-xsendfile
    sudo a2enmod headers proxy proxy_http xsendfile
    sudo a2dissite 000-default.conf
    # sudo a2dissite 000-default on Debian7
    cat << EOF | sudo tee /etc/apache2/sites-available/pythonnest.conf
    <VirtualHost *:80>
        ServerName $SERVICE_NAME
        Alias /static/ $DATA_ROOT/static/
        ProxyPass /static/ !
        <Location /static/>
            Order deny,allow
            Allow from all
            Satisfy any
        </Location>
        # CAUTION: THE FOLLOWING LINES ALLOW PUBLIC ACCESS TO ANY UPLOADED CONTENT
        Alias /media/ $DATA_ROOT/media/
        # the right value is provided by "pythonnest-ctl config python | grep MEDIA_ROOT"
        ProxyPass /media/ !
        <Location /media/>
            Order deny,allow
            Allow from all
            Satisfy any
        </Location>
        ProxyPass / http://localhost:8130/
        ProxyPassReverse / http://localhost:8130/
        DocumentRoot $DATA_ROOT/static/
        # the right value is provided by "pythonnest-ctl config python | grep STATIC_ROOT"
        ServerSignature off
    </VirtualHost>
    EOF
    sudo mkdir $DATA_ROOT
    sudo chown -R www-data:www-data $DATA_ROOT
    sudo a2ensite pythonnest.conf
    sudo apachectl -t
    sudo apachectl restart






If you want to use SSL:

.. code-block:: bash

    sudo apt-get install apache2 libapache2-mod-xsendfile
    PEM=/etc/apache2/`hostname -f`.pem
    # ok, I assume that you already have your certificate
    sudo a2enmod headers proxy proxy_http ssl
    openssl x509 -text -noout < $PEM
    sudo chown www-data $PEM
    sudo chmod 0400 $PEM

    SERVICE_NAME=pythonnest.example.org
    cat << EOF | sudo tee /etc/apache2/sites-available/pythonnest.conf
    <VirtualHost *:80>
        ServerName $SERVICE_NAME
        RedirectPermanent / https://$SERVICE_NAME/
    </VirtualHost>
    <VirtualHost *:443>
        ServerName $SERVICE_NAME
        SSLCertificateFile $PEM
        SSLEngine on
        Alias /static/ $DATA_ROOT/static/
        ProxyPass /static/ !
        <Location /static/>
            Order deny,allow
            Allow from all
            Satisfy any
        </Location>
        # CAUTION: THE FOLLOWING LINES ALLOW PUBLIC ACCESS TO ANY UPLOADED CONTENT
        Alias /media/ $DATA_ROOT/media/
        # the right value is provided by "pythonnest-ctl config python | grep MEDIA_ROOT"
        ProxyPass /media/ !
        <Location /media/>
            Order deny,allow
            Allow from all
            Satisfy any
        </Location>
        ProxyPass / http://localhost:8130/
        ProxyPassReverse / http://localhost:8130/
        DocumentRoot $DATA_ROOT/static/
        # the right value is provided by "pythonnest-ctl config python | grep STATIC_ROOT"
        ServerSignature off
        RequestHeader set X_FORWARDED_PROTO https
    </VirtualHost>
    EOF
    sudo mkdir $DATA_ROOT
    sudo chown -R www-data:www-data $DATA_ROOT
    sudo a2ensite pythonnest.conf
    sudo apachectl -t
    sudo apachectl restart




Application
-----------

Now, it's time to install Pythonnest:

.. code-block:: bash

    pip install setuptools --upgrade
    pip install pip --upgrade
    pip install pythonnest psycopg2
    mkdir -p $VIRTUAL_ENV/etc/pythonnest
    cat << EOF > $VIRTUAL_ENV/etc/pythonnest/settings.ini
    [global]
    data = $HOME/pythonnest
    [database]
    db = pythonnest
    engine = postgresql
    host = localhost
    password = 5trongp4ssw0rd
    port = 5432
    user = pythonnest
    EOF
    chmod 0400 $VIRTUAL_ENV/etc/pythonnest/settings.ini
    # protect passwords in the config files from by being readable by everyone
    pythonnest-ctl collectstatic --noinput
    pythonnest-ctl migrate



Look at :doc:`operating` for actually dumping the official mirror Pypi.





supervisor
----------

Supervisor can be used to automatically launch pythonnest:

.. code-block:: bash


    sudo apt-get install supervisor
    cat << EOF | sudo tee /etc/supervisor/conf.d/pythonnest.conf
    [program:pythonnest_aiohttp]
    command = $VIRTUAL_ENV/bin/pythonnest-ctl server
    user = pythonnest
    EOF
    sudo service supervisor stop
    sudo service supervisor start

Now, Supervisor should start pythonnest after a reboot.


systemd
-------

You can also use systemd (present in many modern Linux distributions) to launch pythonnest:

.. code-block:: bash

    cat << EOF | sudo tee /etc/systemd/system/pythonnest-ctl.service
    [Unit]
    Description=Pythonnest HTTP process
    After=network.target
    [Service]
    User=pythonnest
    Group=pythonnest
    WorkingDirectory=$DATA_ROOT/
    ExecStart=$VIRTUAL_ENV/bin/pythonnest-ctl server
    ExecReload=/bin/kill -s HUP \$MAINPID
    ExecStop=/bin/kill -s TERM \$MAINPID
    [Install]
    WantedBy=multi-user.target
    EOF
    systemctl enable pythonnest-ctl.service
    sudo service pythonnest-ctl start




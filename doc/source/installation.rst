Installation
============

As every Python package, you may use several ways to install PythonNest.
The following packages are required:

  * setuptools >= 3.0
  * djangofloor >= 0.17.0

Installing or Upgrading
-----------------------

Here is a simple tutorial to install PythonNest on a basic Debian/Linux installation.
You should easily adapt it on a different Linux or Unix flavor.



Database
--------

PostgreSQL is often a good choice for Django sites:

.. code-block:: bash

   sudo apt-get install postgresql
   echo "CREATE USER pythonnest" | sudo -u postgres psql -d postgres
   echo "ALTER USER pythonnest WITH ENCRYPTED PASSWORD '5trongp4ssw0rd'" | sudo -u postgres psql -d postgres
   echo "ALTER ROLE pythonnest CREATEDB" | sudo -u postgres psql -d postgres
   echo "CREATE DATABASE pythonnest OWNER pythonnest" | sudo -u postgres psql -d postgres




Apache
------

I only present the installation with Apache, but an installation behind nginx should be similar.
You cannot use different server names for browsing your mirror. If you use `pythonnest.example.org`
in the configuration, you cannot use its IP address to access the website.

.. code-block:: bash

    sudo apt-get install apache2 libapache2-mod-xsendfile
    sudo a2enmod headers proxy proxy_http
    sudo a2dissite 000-default.conf
    # sudo a2dissite 000-default on Debian7
    SERVICE_NAME=pythonnest.example.org
    cat << EOF | sudo tee /etc/apache2/sites-available/pythonnest.conf
    <VirtualHost *:80>
        ServerName $SERVICE_NAME
        Alias /static/ /var/pythonnest/static/
        ProxyPass /static/ !
        Alias /media/ /var/pythonnest/media/
        ProxyPass /media/ !
        ProxyPass / http://127.0.0.1:9000/
        ProxyPassReverse / http://127.0.0.1:9000/
        DocumentRoot /var/pythonnest/
        ServerSignature off
        XSendFile on
        XSendFilePath /var/pythonnest/storage/
        # in older versions of XSendFile (<= 0.9), use XSendFileAllowAbove On


    </VirtualHost>
    EOF
    sudo mkdir /var/pythonnest/
    sudo chown -R www-data:www-data /var/pythonnest/
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
        Alias /static/ /var/pythonnest/static/
        ProxyPass /static/ !
        Alias /media/ /var/pythonnest/media/
        ProxyPass /media/ !
        ProxyPass / http://127.0.0.1:9000/
        ProxyPassReverse / http://127.0.0.1:9000/
        DocumentRoot /var/pythonnest/
        ServerSignature off
        RequestHeader set X_FORWARDED_PROTO https
        <Location />
            Options +FollowSymLinks +Indexes

        </Location>
        <Location /static/>
            Order deny,allow
            Allow from all
            Satisfy any
        </Location>

        XSendFile on
        XSendFilePath /var/pythonnest/storage/
        # in older versions of XSendFile (<= 0.9), use XSendFileAllowAbove On
    </VirtualHost>
    EOF
    sudo mkdir /var/pythonnest/
    sudo chown -R www-data:www-data /var/pythonnest/
    sudo a2ensite pythonnest.conf
    sudo apachectl -t
    sudo apachectl restart



Application
-----------

Now, it's time to install PythonNest:

.. code-block:: bash

    SERVICE_NAME=pythonnest.example.org
    sudo mkdir -p /var/pythonnest
    sudo adduser --disabled-password pythonnest
    sudo chown pythonnest:www-data /var/pythonnest
    sudo apt-get install virtualenvwrapper python3.5 python3.5-dev build-essential postgresql-client libpq-dev
    # application
    sudo -u pythonnest -i
    SERVICE_NAME=pythonnest.example.org
    mkvirtualenv pythonnest -p `which python3.5`
    workon pythonnest
    pip install setuptools --upgrade
    pip install pip --upgrade
    pip install pythonnest psycopg2
    mkdir -p $VIRTUAL_ENV/etc/pythonnest
    cat << EOF > $VIRTUAL_ENV/etc/pythonnest/settings.ini
    [global]
    server_name = $SERVICE_NAME
    protocol = http
    ; use https if your Apache uses SSL
    bind_address = 127.0.0.1:9000
    data_path = /var/pythonnest
    admin_email = admin@$SERVICE_NAME
    time_zone = Europe/Paris
    language_code = fr-fr
    x_send_file =  true
    x_accel_converter = false
    debug = false
    [database]
    engine = django.db.backends.postgresql_psycopg2
    name = pythonnest
    user = pythonnest
    password = 5trongp4ssw0rd
    host = localhost
    port = 5432
    EOF
    pythonnest-manage migrate
    pythonnest-manage collectstatic --noinput



supervisor
----------

Supervisor is required to automatically launch pythonnest:

.. code-block:: bash

    sudo apt-get install supervisor
    cat << EOF | sudo tee /etc/supervisor/conf.d/pythonnest.conf
    [program:pythonnest_gunicorn]
    command = /home/pythonnest/.virtualenvs/pythonnest/bin/pythonnest-gunicorn
    user = pythonnest
    EOF
    sudo /etc/init.d/supervisor restart

Now, Supervisor should start pythonnest after a reboot.


systemd
-------

You can also use systemd to launch pythonnest:

.. code-block:: bash

    cat << EOF | sudo tee /etc/systemd/system/pythonnest-gunicorn.service
    [Unit]
    Description=PythonNest Gunicorn process
    After=network.target
    [Service]
    User=pythonnest
    Group=pythonnest
    WorkingDirectory=/var/pythonnest/
    ExecStart=/home/pythonnest/.virtualenvs/pythonnest/bin/pythonnest-gunicorn
    ExecReload=/bin/kill -s HUP $MAINPID
    ExecStop=/bin/kill -s TERM $MAINPID
    [Install]
    WantedBy=multi-user.target
    EOF
    systemctl enable pythonnest-gunicorn.service




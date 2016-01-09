Complete configuration
======================

You can look current settings with the following command::

    pythonnest-manage config

Here is the complete list of settings::

    [global]
    server_name = pythonnest.example.org
    protocol = https
    bind_address = 127.0.0.1:8211
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

If you need more complex settings, you can override default values (given in `djangofloor.defaults` and `pythonnest.defaults`) by creating a file named `[prefix]/etc/pythonnest/settings.py`.

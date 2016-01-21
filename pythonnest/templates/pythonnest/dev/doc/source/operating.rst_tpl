Operating the mirror
====================

PythonNest is intended to work as read-only copy of the official Python pypi mirror in a disconnected network.

Dumping an existing mirror
--------------------------

You can populate your mirror by copying an existing mirror such as pypi.python.org:

.. code-block:: bash

  workon $VIRTUALENV
  pythonnest-manage update [--url http://pypi.python.org/pypi] [--init-all] [-h]

The source mirror must implement the XML-RPC API (of course, pypi.python.org does).
You have to download around 10 GB (and to wait several hours) to dump an official Pypi mirror if you restrict yourself to the last version of the
downloaded packages.


Exporting data
--------------

If you want to maintain an offline repository, you need two PythonNest instances, the first one being able to run
the `update` command:

.. code-block:: bash

  workon $VIRTUALENV
  pythonnest-manage export [--path <path_you_want_to_export_data_to>] [--tag <tag_to_identify_this_export>] \
    [--serial <serial>]

All packages imported into PythonNest (through `update` or `import` command, or added by users) are associated to
a unique serial. The export command stores the last exported serial associated to the given tag. By default,
the export starts to export data from the last stored serial.
If you only want to dump an existing mirror and export collected data, you can delete the directory
$ROOT_PATH/media/downloads after the export without breaking the database (you only need to be sure that you wan't
export these files again!).

Importing data
--------------


.. code-block:: bash

  workon $VIRTUALENV
  pythonnest manage import [--path <path_with_exported_data>] [--tag <tag_to_identify_this_import>] [--force]

Import all data previously exported by the other PythonNest instance. The last imported serial is stored into database,
so any missing import can be tracked (and further importations are forbidden, unless you specify the --force option).

The `tag` option allow to export data to/to import from different PythonNest instances.

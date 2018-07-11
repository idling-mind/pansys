.. _installation:

Installing pansys
=================

From GAI
--------

If you are working from GAI, to use pansys, you just need to point your 
``PYTHONPATH`` environment variable to ``/tools/hub/pypackages``. 

To set environment variable:
If you are using c-shell edit your ``~/.cshrc`` and add the following line.

.. code-block:: sh

    setenv PYTHONPATH /tools/hub/pypackages/

If you are using bash, edit your ``~/.bashrc`` and add the following line

.. code-block:: bash

    export PYTHONPATH="/tools/hub/pypackages/"

From GAS
--------

If you are working in GAS, please do check if the folder
``/tools/hub/pypackages/`` is existing for you. If not, it is recommended to wait
until that becomes available. If you would like to try out, you can copy the
module code and use it temporarily. You will not get bug fixes and updates if
you do so. 

You can copy the module from the following path
``\\blrroot\tools\hub\pypackages\pansys``. Paste it into a local disk and add the
root path to your ``PYTHONPATH`` environment variable as explain above.

Coding Environment
-------------------

It is recommended to use the anaconda version of python for all code which uses
pansys module. You can find it under the folder ``/opt/anaconda3/bin/``.

To code, its convenient to use ``jupyter-notebook`` or ``jupyter-console`` (from 
``/opt/anaconda3/bin/``). All the samples given under :ref:`examples` use
``jupyter-notebook`` as the authoring environment.

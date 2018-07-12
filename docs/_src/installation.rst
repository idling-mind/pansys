.. _installation:

Installing pansys
=================

For pansys to work, you need ANSYS installed on a linux machine.

.. code-block:: sh

    pip install pansys


The pansys module relies on a command based interface of ANSYS. By default
pansys assumes that you have a command called ``ansys150`` mapped to the ansys
executable. If that does not work for you, use the ``startcommand`` keyword
argument when initiating :class:`Ansys` object and point it to the ANSYS
executable.

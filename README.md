# pansys

Work interactively with ANSYS mechanical APDL and python.

The pansys module helps you interact with ansys through python. Starting a
panys session is as easy as setting a variable.

.. code-block:: python

    from pansys import Ansys
    ans = Ansys()

Now you're ready to send commands to your newly created ansys session.

.. code-block:: python

    ans.send("/prep7")
    ans.send("""n,,1
        n,,2""")

As you must have guessed, ``ans.send`` command will let you send commands
from python to ansys in string format.

You can get data out of Ansys as well.

.. code-block:: python

    nmax = ans.get("node","","num","max")
    ncount = ans.get("node","","count","")

Using ``get_list()`` function, you can get any ansys list item as well.

.. code-block:: python

    nodes = ans.get_list("nlist")

You can also start an ansys session in a remote machine. You will have to set up your ssh keys for this to work.

.. code-block:: python

    ans = Ansys(host="remotesystem")

Look into the documentation to get to know the API better.
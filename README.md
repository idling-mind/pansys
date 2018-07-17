# pansys

[![Documentation Status](http://readthedocs.org/projects/pansys/badge/?version=latest)](https://pansys.readthedocs.io/en/latest/?badge=latest)

Work interactively with ANSYS mechanical APDL and python.

The pansys module helps you interact with ansys through python. Starting a
panys session is as easy as setting a variable.

```python
    from pansys import Ansys
    ans = Ansys()
```

Now you're ready to send commands to your newly created ansys session.

```python
    ans.send("/prep7")
    ans.send("""n,,1
        n,,2""")
```

As you must have guessed, ``ans.send`` command will let you send commands
from python to ansys in string format.

You can get data out of Ansys as well.

```python
    nmax = ans.get("node","","num","max")
    ncount = ans.get("node","","count","")
```

Using ``get_list()`` function, you can get any ansys list item as well.

```python
    nodes = ans.get_list("nlist")
```

You can also start an ansys session in a remote machine. You will have to set up your ssh keys for this to work.

```python
    ans = Ansys(host="remotesystem")
```

Look into the documentation to get to know the API better.

## Installation

As of now, pansys is supported only on Linux systems. You will also need ANSYS installation on your computer
(or on the remote system, if you are using the ``host`` option when you're starting pansys).

```bash
    pip install pansys
```

The module assumes that you have ANSYS already installed in your machine. Also, the default command that the module is using
is ``ansys150``. You can override it with the ``start_command`` keyword argument.

```python
    a = Ansys(startcommand='my_ansys_command')
```

If you want to change the default start command from ``ansys150``, you can set an environment variable ``PANSYS_STARTCOMMAND``.
The value of this environment variable will be used as the start command. This value will be overridden if you explicitly call
``Ansys`` session with a ``startcommand``.

## Documentation

You can find the documentation at [readthedocs](https://pansys.readthedocs.io/en/latest/index.html)

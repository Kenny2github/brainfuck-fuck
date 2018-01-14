brainfuck-fuck
==============

Just a nice little brainfuck interpreter in Python.

Nope! This is brainfuck-*fuck*. You know there's C, then C+, then C++? Well, there's brainfuck, and now there's brainfuck-fuck.
Brainfuck-fuck is supposedly backwards compatible. So therefore this:

.. code-block:: brainfuck

    +++++++ [ > ++++++++++ < - ] > ++ . [-]<[-] ++++++++++ [ > ++++++++++ < - ] > +++++ .

does exactly the same thing as this:

.. code-block:: brainfuck

    =H.=i.

besides the fact that the first one uses two cells while the second uses one.

A full list of additions:
* The ``=`` command.
  This sets the current cell's value to the ASCII value of the character
  after the ``=``. Therefore ``=H`` sets the cell to 72 (the ASCII value of
  H).
* An if/else statement!
  The syntax is ``? (code) : (code) !``. When a ``?`` is reached, it checks
  the current cell. If the current cell is 0, it skips to the
  corresponding ``:``. Otherwise, it continues on until the ``:``, then skips
  to the ``!``. Thus ``+ ? =Y : =N ! .`` prints out "Y" while ``? =Y : =N ! .``
  prints out "N".
* Functions! To define a function, use
  ``(@ symbol)(single ASCII character)(code)(pipe, |)``,
  e.g. ``@F+++++|`` (which simply adds 5). To call a function, use a caret
  (``^``) and then the ASCII character used to name the function, e.g. ``^F``
  (which calls the previously defined function ``F``, thereby adding 5).

Booleans
--------

In this assignment, booleans can only be produced using comparison
operators, there is no literal to express them. As well, they are
ephemeral: there is no way to store them. They can only exist when
created using one of the comparison operators.

When printed, booleans take on a value of 1 (true) or 0 (false). For
example:

::

     print(1 == 1);
     print(1 == 0);

produces the following output:

::

     1
     0

As well booleans *are* usable in expressions and must be *upcast* to an
integer. This means if a boolean is used in an arithmetic expression it
takes on the integer value described above. For example:

::

     print(1 + (1 == 1));
     print(1 + (1 == 0));

produces the following output:

::

     2
     1


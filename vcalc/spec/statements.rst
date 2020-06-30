Statements
----------

Declaration
~~~~~~~~~~~

*VCalc* adds vectors as an assignable type. To declare a vector
variable, you declare a variable as you would an integer, but replace
``int`` with ``vector``. Vectors may be initialized with any expression
that returns a vector. For example, assigning a range to a vector ``v``:

::

     vector v = 1..10;
     print(v);

prints the following:

::

     [1 2 3 4 5 6 7 8 9 10]

Assignment
~~~~~~~~~~

There are a few new important points when dealing with assignments.

#. The size of a vector may change while the program is executing if a
   vector variable is assigned another value. For instance, the
   following sequence of statements *is* valid:

   ::

            vector v = 1..10;
            v = 1..1000;

   You will have to allocate more memory to store the result of the
   assignment.

#. The type of the expression of the assignment must match the
   destination variable’s type. This is apparent for trying to assign
   vectors to a scalar. In the case of scalars being assigned to
   vectors, one might expect that we can use our extension policy to
   copy our scalar to every index of a newly created vector but the
   question is, how large is the new vector. Because that is
   indeterminable, this is not allowed. For example, the following
   sequence of statements *is not* valid:

   ::

            int i = 1..3;
            vector v = 1;

#. Many languages allow you to assign to vector indices, *VCalc does
   not*. For example, the following sequence of statments *is not*
   valid:

   ::

      ;
            vector v = 1..3;
            v[0] = 99;

Conditional
~~~~~~~~~~~

Conditional conditions must evaluate to booleans, this means that
vectors are not a valid condition. Remember, however, that integers can
be implicitly downcast to booleans.

Loops
~~~~~

Loop conditions must evaluate to booleans, this means that vectors are
not a valid condition. Remember, however, that integers can be
implicitly downcast to booleans.


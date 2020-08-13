Scoping
-------

Loops and conditionals are scoped in *VCalc*, unlike *SCalc*. As well,
generators and filters both have internal scopes for their domain
variable.

A reference to a variable will resolve to the *definition* in the
innermost possible scope. This matches the scoping rules found in *C*.
For example:

::

     int i = 1;
     print(i);

     if (1 == 1)
       int i = 3;
       print(i);

       i = i * 2;
       print(i);
     fi;

     print(i);

     loop (i < 20)
       print(i);
       i = i + 10;
     pool;

     print(i);

prints the following:

::

     1
     3
     6
     1
     1
     11
     21

Generator and filter scopes only exist during the evaluation of the
expression or predicate. The scope will only contain the domain
variable.

Be careful in what order you evaluate things. For example:

::

     int i = 0;
     if (1 == 1)
       int i = i + 1;
       print(i);
     fi;

     vector v = 0..3;
     print([i in i..3 | i]);
     print([v in v & v < 2]);

     int j = 5;
     print([i in v | i * j]);

prints the following:

::

     1
     [0 1 2 3]
     [0 1]
     [0 5 10 15]

If you define a variable in a scope before evaluating the expression,
you may mis-resolve a value. If you enter the new scope in your filter
or generator before resolving the domain, you may mis-resolve the
domain.


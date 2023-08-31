.. _sec:typeChecking:

Vector/Matrix Type Checking
===========================

While the size of vectors and matrices may not always be known at
compile time, there are instances where the compiler can perform length
checks at compile time. For instance:

::

       integer v[3] = 1..10;

In cases like these the compiler is always able to catch the size
mismatch, since the vector ``1..10`` is known at compile time.

Your compiler should handle cases where the initialization
expression consists of an expression with only literal values (thus, it
can be evaluated at compile time). Similarly the size of the declared
vector must either be given with an expression of literal values, or not
be provided. If a size mismatch is detected here the compiler should
throw an error.

The compiler should also handle cases where a type can be propogated
within the local scope:

::

       {
         integer v[3] = 3;
         integer w[2] = v;
       }

The compiler should also be able to detect cases such as:

::

       integer[*] v = 1;

where the length of the vector can not be determined at all.

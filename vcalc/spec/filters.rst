Filters
-------

A filter has similar syntax to a generator, but instead has a ``&``
instead of a ``|`` as shown here:

::

     [<domain variable> in <domain> & <predicate>]

The identifier and vector are still called the domain variable and
domain vector, however, the right-hand-side expression is now called the
*predicate*. The domain variable is an integer typed variable defined
only in the scope of the generator.

As in a generator, the domain may be any vector-valued expression which
includes identifiers (that are vector typed), ranges, generators,
filters, and index expressions with a vector index. The expression must
evaluate to a boolean. This means that if the result of the expression
is an integer it will be implicitly demoted to a boolean, but a vector
result is an *error*.

A filter will create a new vector containing only the elements of the
domain where the predicate evaluates to a true value. The domain values
that satisfy the predicate are appended to the result vector in their
original order. For instance, to select all of values greater than 5 in
a vector you might write:

::

     print([i in 1..10 & 5 < i ]);

prints the following:

::

     [6 7 8 9 10]


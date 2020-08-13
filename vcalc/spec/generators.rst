Generators
----------

A generator is another way to create a vector in *VCalc*. Generators
work the same as they did in the generator assignment and have the
following form:

::

     [<domain variable> in <domain> | <expression>]

The identifier is referred to as the domain variable, the vector is the
domain or domain vector, and the expression is the right-hand-side
expression. The domain variable is an integer typed variable defined
only in the scope of the generator.

The domain may be any vector-valued expression which includes
identifiers (that are vector typed), ranges, generators, filters, and
index expressions with a vector index. The expression must evaluate to
an integer. This means that if the result of the expression is a boolean
it will be implicitly promoted to an integer, but a vector result is an
*error*.

Generators are identical to list comprehensions from other languages.
For instance, to generate a vector of the first 100 perfect squares, one
may write the following generator:

::

     vector sqrs = [i in 1..100 | i * i];

The expression on the right yields the value for a single element of the
generated vector, which corresponds to the element ``i`` of the domain
vector.

The right-hand-side expression does not need to depend upon the domain
variable. For instance:

::

     print([i in 1..10 | 0]);

prints the following:

::

     [0 0 0 0 0 0 0 0 0 0]

As another example, the following generator produces the square value of
all positive, even integers up to 20.

::

     print([i in [ j in 1..10 | j * 2] | i * i]);

prints the following:

::

     [4 16 36 64 100 144 196 256 324 400]


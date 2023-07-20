Vectors
-------

*VCalc* has a new type, ``vector``, that is a vector of integer values.
Vectors are restricted to the length that can be represented by the
*largest possible index*. Indices are integers and integers are signed
32 bit integers. Because the largest possible integer is
:math:`2^{31} - 1` or :math:`2147483647`, a vector can have a length in
the range :math:`[0, 2^{31}]`.

**Assertion:** All vectors will have length :math:`l` such that
:math:`0 \leq l \leq 2^{32}`. (:ref:`vector-length <assert:vector-length>`)

There is no way to specify a vector literal, they must be created
through ranges, generators, filters, or index expressions with a vector
index.

The only way to create an empty vector is through the use of a filter
whose predicate is evaluated to false at each index of the domain or a
range whose first bound is greater than the second bound. Once you have
an empty vector, other operations may also produce empty vectors. That
is, binary operations between an empty vector and another empty vector
or a scalar, indexing by an empty vector, or using an empty vector as a
generator or filter domain will also result in an empty result vector.

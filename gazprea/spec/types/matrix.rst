.. _ssec:matrix:

Matrix
------

*Gazprea* supports two dimensional matrices. A matrix can have all of
the same element types a vector can:

-  ``boolean``

-  ``integer``

-  ``real``

-  ``character``

.. _sssec:matrix_decl:

Declaration
~~~~~~~~~~~

Matrix declarations are similar to vector declarations, the difference
being that matrices have two dimensions instead of one. The following are
valid matrix declarations:

::

   				integer[*, *] A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]];
   				integer[3, 2] B = [[1, 2], [4, 5], [7, 8]];
   				integer[3, *] C = [[1, 2], [4, 5], [7, 8]];
   				integer[*, 2] D = [[1, 2], [4, 5], [7, 8]];
   				integer[*, *] E = [[1, 2], [4, 5], [7, 8]];


.. _sssec:matrix_null:

Null
~~~~

Matrix of ``null`` elements.

.. _sssec:matrix_ident:

Identity
~~~~~~~~

Matrix of ``identity`` elements.

.. _sssec:matrix_constr:

Construction
~~~~~~~~~~~~

To construct a matrix the programmer may use nested vectors. Each vector
element represents a single row of the matrix. All rows with fewer
elements than the row of maximum row length are padded with ``null``
values on the right. Similarly, if the matrix is declared with a column
length larger than the number of rows provided, the bottom rows of the
matrix are ``null``. If the number of rows or columns exceeds the
amounts given in a declaration an error is to be produced.

::

   				integer[*] v = [1, 2, 3];
   				integer[*, *] A = [v, [1, 2]];
   				/* A == [[1, 2, 3], [1, 2, 0]] */


Similarly, we can have:

::

   				integer[*] v = [1, 2, 3];
   				integer[3, 3] A = [v, [1, 2]];
   				/* A == [[1, 2, 3], [1, 2, 0], [0, 0, 0]] */


Also matrices can be initialized with a scalar value, ``null``, or
``identity``. ``null`` and ``identity`` behave as previously described.
Initializing with a scalar value makes every element of the matrix equal
to the scalar.

Gazprea supports empty matrices.

::

   integer[*,*] m = []; /* Should create an empty matrix */

.. _sssec:matrix_ops:

Operations
~~~~~~~~~~

Matrices have binary and unary operations of the element type defined in
the same manner as vectors. Unary operations are applied to every
element of the matrix, and binary operations are applied between
elements with the same position in two matrices.

The operators ==, and != also have the same behaviors that vectors do.
These operations compare whether or not **all** elements of two matrices
are equal.

In addition to this matrices have several special operations defined on
them. If the element type is numeric (supports addition, and
multiplication), then matrix multiplication is supported using the
operator \**. Matrix multiplication is only defined between matrices
with compatible element types, and the dimensions of the matrices must be
valid for performing a matrix multiplication. If this is not the case
then an error should be raised.

All matrices support the built in functions ``rows`` and ``columns``,
which when passed a matrix yields the number of rows and columns in the
matrix respectively. For instance:

::

   				integer[*, *] M = [[1, 1, 1], [1, 1, 1]];

   				integer r = rows(M);  /* This has a value of 2 */
   				integer c = columns(M);  /* This has a value of 3 */


Matrix indexing is done similarly to vector indexing, however, two
indices must be used. These indices are separated using a comma.

::

   				M[i, j] -> std_output;


The first index specifies the row of the matrix, and the second index
specifies the column of the matrix. The result is retrieved from the row
and column. Both the row and column indices must be integers.

::

   				integer[*, *] M = [[11, 12, 13], [21, 22, 23]];

   				/* M[1, 2] == 12 */

As with vectors, out of bounds indexing is an error on Matrices.


Type Casting and Type Promotion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see the types that ``matrix`` may be cast and/or promoted to, see
the sections on :ref:`sec:typeCasting` and :ref:`sec:typePromotion`
respectively.

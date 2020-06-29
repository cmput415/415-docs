.. _ssec:matrix:

Matrix
------

*Gazprea* supports two dimensional matrices. A matrix can have all of
the same base types a vector can:

-  ``boolean``

-  ``integer``

-  ``real``

-  ``character``

.. _sssec:matrix_declr:

Declaration
~~~~~~~~~~~

A matrix is declared using the ``matrix`` keyword. Matrix declarations
are similar to vector declarations, the difference being that matrices
have two dimensions instead of one. The following are valid matrix
declarations:

::

   				integer matrix A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]];
   				integer matrix A[3, 2] = [[1, 2], [4, 5], [7, 8]];
   				integer matrix A[3, *] = [[1, 2], [4, 5], [7, 8]];
   				integer matrix A[*, 2] = [[1, 2], [4, 5], [7, 8]];
   				integer matrix A[*, *] = [[1, 2], [4, 5], [7, 8]];
   			

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

   				integer vector v = [1, 2, 3];
   				integer matrix A = [v, [1, 2]];
   				/* A == [[1, 2, 3], [1, 2, 0]] */
   			

Similarly, we can have:

::

   				integer vector v = [1, 2, 3];
   				integer matrix A[3, 3] = [v, [1, 2]];
   				/* A == [[1, 2, 3], [1, 2, 0], [0, 0, 0]] */
   			

Also matrices can be initialized with a scalar value, ``null``, or
``identity``. ``null`` and ``identity`` behave as previously described.
Initializing with a scalar value makes every element of the matrix equal
to the scalar.

.. _sssec:matrix_ops:

Operations
~~~~~~~~~~

Matrices have binary and unary operations of the base type defined in
the same manner as vectors. Unary operations are applied to every
element of the matrix, and binary operations are applied between
elements with the same position in two matrices.

The operators ==, and != also have the same behaviors that vectors do.
These operations compare whether or not **all** elements of two matrices
are equal.

In addition to this matrices have several special operations defined on
them. If the base type is numeric (supports addition, and
multiplication), then matrix multiplication is supported using the
operator \**. Matrix multiplication is only defined between matrices
with compatible base types, and the dimensions of the matrices must be
valid for performing a matrix multiplication. If this is not the case
then an error should be raised.

All matrices support the built in functions ``rows`` and ``columns``,
which when passed a matrix yields the number of rows and columns in the
matrix respectively. For instance:

::

   				integer matrix M = [[1, 1, 1], [1, 1, 1]];

   				integer r = rows(M);  /* This has a value of 2 */
   				integer c = columns(M);  /* This has a value of 3 */
   			

Matrix indexing is done similarly to vector indexing, however, two
indices must be used. These indices are separated using a comma.

::

   				M[i, j] -> out;
   			

The first index specifies the row of the matrix, and the second index
specifies the column of the matrix. The result is retrieved from the row
and column. Both the row and column indices can be either integers,
integer intervals, or integer vectors. When both indices are scalar
integers the result is the scalar value in the row and column specified.

::

   				integer matrix M = [[11, 12, 13], [21, 22, 23]];

   				/* M[1, 2] == 12 */
   			

If one of the indices is an interval or a vector, and the other index is
a scalar, then the result is a vector. For example:

::

   				integer matrix M = [[11, 12, 13], [21, 22, 23]];

   				/* Select from row 2 */
   				/* M[2, 2..3] == [22, 23] */
   				/* M[2, [3, 2]] == [23, 22] */

   				/* Select from column 1 */
   				/* M[1..2, 1] == [11, 21] */
   				/* M[[2, 1], 1] == [21, 11] */
   			

Finally, both of the indices may be intervals or vectors, in which case
the result is another matrix.

::

   				integer matrix M = [[11, 12, 13], [21, 22, 23]];

   				/* Makes a matrix consisting of [[M[2, 1], M[2, 3]], [M[1, 1], M[1, 3]]] */
   				integer matrix K = M[[2, 1], [1, 3]];
   			

As with vectors, out of bounds indexing is an error on Matrices.


Type Casting and Type Promotion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see the types that ``matrix`` may be cast and/or promoted to, see
the sections on :ref:`sec:typeCasting` and :ref:`sec:typePromotion` 
respectively.
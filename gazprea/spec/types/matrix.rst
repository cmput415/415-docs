.. _ssec:matrix:

Matrices
--------

*Gazprea* arrays generalize to arbitrary rank: a type of the form
``T[n1][n2]...[nk]`` is a rank-``k`` array whose element type ``T`` may be
any :ref:`storable type <ssec:storable_types>`. A *matrix* is the rank-2
case, and this section describes it in full; higher-rank arrays follow the
same construction, indexing, and element-wise operation rules, generalized
to ``k`` index positions. The rank-2 operators discussed below (matrix
multiplication, ``rows``, and ``columns``) are defined on matrices
specifically; their generalization to higher-rank arrays is left to a
future revision of this specification.

.. _sssec:matrix_decl:

Declaration
~~~~~~~~~~~

Matrix declarations are similar to array declarations, the difference
being that matrices have two dimensions instead of one. The following are
valid matrix declarations:

::

           integer[*][*] A = [[1, 2, 3], [4, 5, 6], [7, 8, 9]];
           integer[3][2] B = [[1, 2], [4, 5], [7, 8]];
           integer[3][*] C = [[1, 2], [4, 5], [7, 8]];
           integer[*][2] D = [[1, 2], [4, 5], [7, 8]];
           integer[*][*] E = [[1, 2], [4, 5], [7, 8]];

Both matrix dimensions are :term:`initialization`-time sized: each length is
fixed once when the matrix is :term:`initialized <initialization>` and never
changes thereafter. A ``[*]`` in either position infers that dimension once
from the initializer — exactly as ``[*]`` infers the length of a 1-D array —
after which it too is fixed.

.. _sssec:matrix_constr:

Construction
~~~~~~~~~~~~

A 2D matrix can be viewed as an array of arrays.
The elements in each array form a single row of the matrix.
All rows with fewer elements than the row of maximum row length are padded with
zeros on the right. Similarly, if the matrix is declared with a row
length larger than the number of rows provided, the bottom rows of the
matrix are zero. If the number of rows or columns exceeds the
amounts given in a declaration the compiler must emit a ``SizeError``
(see :ref:`sec:errors`).

::

           integer[*] v = [1, 2, 3];
           integer[*][*] A = [v, [1, 2]];
           /* A == [[1, 2, 3], [1, 2, 0]] */


Similarly, we can have:

::

           integer[*] v = [1, 2, 3];
           integer[3][3] A = [v, [1, 2]];
           /* A == [[1, 2, 3], [1, 2, 0], [0, 0, 0]] */


Also matrices can be initialized with a :term:`scalar <scalar type>` value.
Initializing with a scalar value makes every element of the matrix equal
to the scalar.

Gazprea supports empty matrices.

::

   integer[*][*] m = []; /* Should create an empty matrix */

.. _sssec:matrix_ops:

Operations
~~~~~~~~~~

Multi-dimensional arrays have binary and unary operations of the element type
defined in the same manner as uni-dimensional arrays.
Unary operations are applied to every element of the matrix, and binary
operations are applied between elements with the same position in the arrays.

The operators ==, and != also have the same behavior independent of the
dimensionality of the array.
These operations compare whether or not **all** elements of are equal.

Two dimensional arrays have several special operations defined on them.
If the element type is numeric (supports addition and multiplication),
then matrix multiplication is supported using the operator \**.
Matrix multiplication is only defined between matrices with compatible element
types, and the dimensions of the matrices must be valid for performing matrix
multiplication.
Specifically, the number of columns of the first operand must equal the number
of rows of the second operand, e.g. an :math:`m \times n` matrix multiplied by
an :math:`n \times p` matrix will produce an :math:`m \times p` matrix.
If the dimensions are not correct the compiler must emit a ``SizeError``.

Arrays of any dimension support the built in functions ``rows`` and ``columns``,
which when passed a 2D array yields the number of rows and columns in the
matrix respectively. For instance:

::

           integer[*][*] M = [[1, 1, 1], [1, 1, 1]];

           integer r = rows(M);  /* This has a value of 2 */
           integer c = columns(M);  /* This has a value of 3 */


Matrix indexing is done similarly to array indexing, however, two
indices must be used. Because matrices are arrays of arrays the indexing is
composite:

::

           M[i][j] -> std_output;


The first index specifies the row of the matrix, and the second index
specifies the column of the matrix. The result is retrieved from the row
and column. Both the row and column indices must be integers.

::

           integer[*][*] M = [[11, 12, 13], [21, 22, 23]];

           /* M[1][2] == 12 */

As with arrays, out of bounds indexing on matrices must emit an
``IndexError``.


Type Casting and Implicit Casts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see the types that a matrix may be cast and/or implicitly cast to, see
the sections on :ref:`sec:typeCasting` and :ref:`sec:typePromotion`
respectively.

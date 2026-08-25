.. _ssec:matrix:

Matrices
--------

*Gazprea* arrays generalize to arbitrary rank: a type of the form
``T[n1][n2]...[nk]`` is a rank-``k`` array whose element type ``T`` may be
any :ref:`storable type <ssec:storable_types>`. A *matrix* is the rank-2
case, and this section describes it in full; higher-rank arrays follow the
same construction, indexing, and element-wise operation rules, generalized
to ``k`` index positions. The ``rows`` and ``columns`` built-ins discussed
below are defined on matrices (rank-2 arrays) specifically, and ``length`` on
rank-1 arrays; there is currently **no** size query for arrays of rank 3 or
more, so their extents are not observable at run time. This is a known
limitation: a general ``shape`` built-in reporting the extents of an array of
any rank is planned for a future revision of this specification. Matrix
multiplication (``**``), by contrast, is defined for
arrays of **any** rank, as described in :ref:`sssec:matrix_ops`.

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
the element type's :term:`zero value` on the right. Similarly, if the matrix is
declared with more rows than are provided, the bottom rows hold the element
type's zero value. If the number
of rows or columns exceeds the
amounts given in a declaration the compiler must emit a ``SizeError``
(see :ref:`sec:errors`) at :term:`compile time` or :term:`run time`.

This pad-to-longest-row rule is a property of the nested array literal itself, so
it applies identically whether the literal initializes a matrix, an array
variable, or a :ref:`vector of arrays <ssec:vector>`. Only *incrementally*
growing a vector with ``push``/``append`` behaves differently, fitting each new
element to the size fixed by the first element; :ref:`ssec:vector` walks through
the contrast with worked examples.

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

Gazprea supports empty matrices. A rank-2 array initialized from the empty
literal ``[]`` is the empty rank-2 array, written ``[[]]``:

::

   integer[*][*] m = []; /* m == [[]], an empty rank-2 array */

Like an empty 1-D array, an empty matrix has its (zero) dimensions fixed at
:term:`initialization` and is not growable. Both of its dimensions are zero:
``rows(m)`` and ``columns(m)`` are each ``0`` (a 0x0 matrix, notwithstanding the
``[[]]`` notation).

.. _sssec:matrix_ops:

Operations
~~~~~~~~~~

Multi-dimensional arrays have binary and unary operations of the element type
defined in the same manner as uni-dimensional arrays.
Unary operations are applied to every element of the matrix, and binary
operations are applied between elements with the same position in the arrays.

The operators ==, and != also have the same behavior independent of the
dimensionality of the array.
These operations compare whether or not **all** elements of the two matrices
are equal.

Two dimensional arrays have several special operations defined on them.
If the element type is numeric (supports addition and multiplication),
then matrix multiplication is supported using the operator \**.
Matrix multiplication is only defined between matrices with compatible element
types, and the dimensions of the matrices must be valid for performing matrix
multiplication. When the two operands have differing element types (e.g.
``integer ** real``), each element is implicitly cast to a common type (see
:ref:`sec:implicitCasts`) before multiplication, just as for element-wise
binary operations. Specifically, the number of columns of the first operand must equal the number
of rows of the second operand, e.g. an :math:`m \times n` matrix multiplied by
an :math:`n \times p` matrix will produce an :math:`m \times p` matrix.
If the dimensions are not correct the compiler must emit a ``SizeError``
(see :ref:`sec:errors`).

When one operand of ``**`` is a scalar it can be broadcast to a matrix operand
of matrix multiplication **only if the other operand is a square matrix**: a
scalar ``s`` paired with an :math:`n \times n` matrix is filled into an
:math:`n \times n` matrix whose every element is ``s`` before the
multiplication. If the other operand is not square the scalar cannot be
broadcast and the compiler must emit a ``TypeError`` (see :ref:`sec:errors`).
Scalars broadcast this way only to ``**`` operands whose extents are all equal --
a rank-1 array (trivially, since it has a single extent, so a scalar may be
dotted with a vector; see the :ref:`dot product <sssec:array_ops>`), a square
matrix, or a higher-rank hypercube with equal extents; *Gazprea* does **not**
provide comprehensive broadcasting. See :ref:`sec:implicitCasts`.

More generally, ``**`` is defined for numeric arrays of **any** rank as the
single-axis contraction familiar from linear algebra: the **last** dimension of
the left operand is contracted with the **first** dimension of the right
operand. Writing the left operand as a rank-:math:`a` array ``A`` and the right
operand as a rank-:math:`b` array ``B``, the last extent of ``A`` must equal
the first extent of ``B`` -- otherwise the compiler must emit a ``SizeError``
(see :ref:`sec:errors`) -- and the result ``C`` has rank :math:`a + b - 2`,
given by
:math:`C[i_1 \ldots i_{a-1},\, k_2 \ldots k_b] = \sum_j A[i_1 \ldots i_{a-1},\, j] \cdot B[j,\, k_2 \ldots k_b]`.
The rank-1-with-rank-1 case is therefore the :ref:`dot product
<sssec:array_ops>` (a scalar) and the rank-2-with-rank-2 case is the matrix
multiplication described above; both are instances of the one contraction rule,
which corresponds directly to the contraction operations already available in
*MLIR*.

The number of rows and columns in a matrix is given by the built-in
functions ``rows`` and ``columns``; see :ref:`ssec:builtIn_rows_cols` for
their full definition.


Matrix indexing is done similarly to array indexing. Because a matrix is an
array of arrays, indexing is *composite*: each subscript is applied, left to
right, to the value the subscripts before it produced. The ``[]`` operator is
left-associative, so ``M[i][j]`` groups as ``(M[i])[j]``:

::

           M[i][j] -> std_output;


The first subscript ``M[i]`` selects row ``i`` -- a whole rank-1 array -- and
the second subscript then indexes *that* row, so ``M[i][j]`` selects element
``j`` of row ``i``. When both indices are single integers, as here, the result
is the one element at that row and column:

::

           integer[*][*] M = [[11, 12, 13], [21, 22, 23]];

           /* M[1]    == [11, 12, 13]  (the whole first row) */
           /* M[1][2] == 12            (its second element)  */

As with arrays, out of bounds indexing on matrices must emit an
``IndexError`` (see :ref:`sec:errors`) at :term:`compile time` or
:term:`run time`.

Each index position accepts the same forms as a 1-D array index (see
:ref:`sssec:array_slices`): a single integer selects one element along the
current outermost axis and drops that axis, while a range written directly in an
index position selects a contiguous run along it and keeps it (a slice, with the
same inclusive-left, exclusive-right bounds as for 1-D arrays). Because the
subscripts are applied one after another, each indexes the outermost *remaining*
axis of the value the previous subscripts produced -- a matrix is peeled from
the outside in, exactly as in *C*. So ``M[i]`` selects a whole row (a rank-1
array), ``M[i][j]`` selects one element, ``M[1..3]`` selects a contiguous band
of rows (a rank-2 sub-matrix), and ``M[1..3][2]`` re-indexes that band to select
its second row. Higher-rank arrays generalize this to ``k`` subscripts.

::

           integer[*][*] M = [[11, 12, 13], [21, 22, 23], [31, 32, 33]];

           /* M[2]        == [21, 22, 23]                  (a whole row)         */
           /* M[1..3]     == [[11, 12, 13], [21, 22, 23]]  (rows 1 and 2)        */
           /* M[1..3][2]  == [21, 22, 23]                  (second row of those) */

Operator precedence and associativity are specified once, for all types, in
the :ref:`table of operator precedence <ssec:expressions_toop>`.


Type Casting and Implicit Casts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see the types that a matrix may be cast and/or implicitly cast to, see
the sections on :ref:`sec:typeCasting` and :ref:`sec:implicitCasts`
respectively.

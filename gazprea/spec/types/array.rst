.. _ssec:array:

Arrays
------

Arrays are fixed size collections, where each element of the array has the same
type. An array element may be of any :ref:`storable type
<ssec:storable_types>`: a :term:`primitive type <primitive type>` (``boolean``,
``integer``, ``real``, ``character``), or an 
:term:`aggregate type <aggregate type>` 
such as a ``struct``, ``tuple``, ``vector``, ``string``, or another
array (which yields a higher-rank array; see :ref:`ssec:matrix`).

.. _sssec:array_sizing:

Sizing
~~~~~~

Arrays are **initialization-time sized**: the length of an array variable --
and, for a :ref:`matrix or higher-rank array <ssec:matrix>`, each of its
dimensions -- is settled exactly *once*, at the variable's
:term:`initialization`, and from that point on is fixed for the entire
:term:`lifetime` of the variable. The glossary entry for
:term:`initialization` gives the general rule -- a size is any integer
expression, evaluated a single time at the declaration's program point, and
need not be a :term:`compile time` constant. Concretely:

-  A declaration such as ``integer[n] v;`` evaluates ``n`` once, at
   initialization. Later changes to ``n`` have no effect on the length of
   ``v``.

-  A declaration such as ``integer[*] v = <expr>;`` takes its length from the
   value of ``<expr>`` at initialization. The ``*`` means "infer this length
   once, here"; it does **not** mean the array is resizable.

-  No subsequent operation can change the length of an array variable.
   Assignment, concatenation, and casting all produce array *values*; storing
   such a value into an array variable never resizes that variable. If the
   value's length does not match, it is padded with the element type's
   :term:`zero value`, or the compiler must emit a ``SizeError`` (see
   :ref:`sec:errors`) at :term:`compile time` or :term:`run time`, as
   described below.

If you need a collection whose length changes as the program runs, use a
:ref:`vector <ssec:vector>`, which is runtime sized. See
:ref:`sssec:array_vs_vector`.

.. _sssec:array_decl:

Declaration
~~~~~~~~~~~

Aside from any type specifiers, the element type of the array is the first
portion of the declaration. An array is then declared using square brackets
immediately after the element type.

If possible, initialization expressions may go through an implicit cast. For
instance, when declaring a real array that is initialized with an integer value
the integer will be implicitly cast to a real value, and then used as a scalar
initialization of the array. Be careful about type inference! If the type of
the array is being inferred from the right hand side, the previous example
would create an ``integer`` array instead of a ``real`` array.

#. Explicit Size Declarations

   When an array is declared it may be explicitly given a size. Every array,
   whether explicitly or implicitly sized, has a size that is fixed on the
   first execution of its declaration at :term:`run time` and is
   immutable thereafter; a collection whose size can grow requires a
   :ref:`vector <ssec:vector>`.

   ::

            [<qualifier>] <type>[<int-expr>] <identifier>;
            [<qualifier>] <type>[<int-expr>] <identifier> = <type-expr>;
            [<qualifier>] <type>[<int-expr>] <identifier> = <type-array>;


   The size of the array is given by the integer expression between the
   square brackets.

   If the array is given a scalar value (``type-expr``) of the same element
   type then the scalar value is duplicated for every single element of the
   array.

   An array may also be initialized with another array. Initialization occurs
   element-wise, with the RHS element type's initialization semantics applying
   from left to right. If the LHS array is initialized using a RHS array that
   is too small then the LHS array will be padded with the element type's
   :term:`zero value`. However, if the LHS array is initialized with a RHS
   array that is too large then the compiler must emit a ``SizeError`` (see
   :ref:`sec:errors`) at :term:`compile time` or :term:`run time`.

#. Inferred Size Declarations

   If an array is assigned an initial value when it is declared, then
   its size may be inferred. There is no need to repeat the size in the
   declaration because the size of the array on the right-hand side is
   known.

   ::

            <type>[*] <identifier> = <type-array>;


#. Inferred Type and Size

   It is also possible to declare an array with an implied type and
   length using the var or const keyword. This type of declaration can only be
   used when the variable is initialized in the declaration, otherwise
   the compiler will not be able to infer the type or the size of the
   array.

   ::

      integer[*] v = [1, 2, 3];
      var w = v + 1;


   In this example the compiler can infer both the size and the type of
   ``w`` from ``v``. As with any array, this inferred size is fixed once,
   at :term:`initialization`, and never changes afterwards; a collection
   whose length must *change* after it is created requires a
   :ref:`vector <ssec:vector>`.

.. _sssec:array_constr:

Construction
~~~~~~~~~~~~

An array value in *Gazprea* may be constructed using the following
notation:

::

   [expr1, expr2, ..., exprN]


Each ``expK`` is an expression with a compatible type. In the simplest
cases each expression is of the same type, but it is possible to mix the
types as long as all of the types can be implicitly cast to a common type. For
instance it is possible to mix integers and real numbers.

::

   real[*] v = [1, 3.3, 5 * 3.4];


It is also possible to construct a single-element array using this
method of construction.

::

   real[*] v = [7];


*Gazprea* **DOES** support empty arrays.

::

   real[*] v = []; /* Should create an empty array */

Because the length of an array is fixed at :term:`initialization`, such an
array has a length of zero permanently; it is not an "empty, growable"
array. A :ref:`vector <ssec:vector>` declared without an initializer also
starts empty, but *can* subsequently grow.

.. _sssec:array_vs_vector:

Arrays Versus Vectors
~~~~~~~~~~~~~~~~~~~~~~~

*Gazprea* has two collection types that share the same element-wise
operations but differ in exactly one respect -- when their length is decided:

.. list-table::
   :header-rows: 1
   :widths: 34 33 33

   * -
     - **Array** (``T[N]``, ``T[*]``, and higher-rank arrays / matrices)
     - **Vector** (``vector<T>``, ``string``)
   * - When is the length set?
     - Once, at initialization
     - Continuously, at run time
   * - Can it change afterwards?
     - No
     - Yes
   * - Written in the type?
     - Yes (``[N]``), or inferred once (``[*]``)
     - No
   * - Grows via ``push`` / ``append``?
     - No -- ``TypeError`` (arrays have no methods)
     - Yes
   * - Too-short value stored into it
     - Padded with the element type's :term:`zero value`
     - The vector takes the value's length
   * - Too-long value stored into it
     - ``SizeError``
     - The vector takes the value's length

The two types interoperate, but only through *values*: a vector used in an
array context yields an array value of the vector's current length, and an
array value stored into a vector sets that vector's length. Neither direction
ever makes an array variable resizable. See :ref:`ssec:vector` for the
details of that interoperation.

.. _sssec:array_ops:

Operations
~~~~~~~~~~

#. Array Operations and functions

   a. length

      The number of elements in an array is given by the built-in
      function ``length``; see :ref:`ssec:builtIn_length` for its full
      definition.

   b. Concatenation

      Two arrays with the same element type may be concatenated into a
      single array using the concatenation operator, ``||``. For
      instance:

      ::

         [1, 2, 3] || [4, 5] // produces [1, 2, 3, 4, 5]
         [1, 2] || [] || [3, 4] // produces [1, 2, 3, 4]


      Concatenation is also allowed between arrays of different element
      types, as long as one element type can be implicitly cast to the
      other. For instance:

      ::

         integer[3] v = [1, 2, 3];
         real[3] u = [4.0, 5.0, 6.0];
         real[6] j = v || u;


      would be permitted, and the integer array ``v`` would be implicitly
      cast to a real array before the concatenation.

      Concatenation may also be used with scalar values. In this case
      the scalar values are treated as though they were single element
      arrays.

      ::

         [1, 2, 3] || 4 // produces [1, 2, 3, 4]
         1 || [2, 3, 4] // produces [1, 2, 3, 4]


      At least one operand of ``||`` must be a composite value (an array,
      :ref:`vector <ssec:vector>`, or ``string``). Concatenating two scalars
      is a ``TypeError``; wrap one operand in a one-element array first:

      ::

         integer[3] v = 1 || 2 || 3;   // TypeError: both operands are scalars
         integer[3] w = [1] || 2 || 3; // [1, 2, 3]: left operand is an array


      Remember that arrays have a fixed length, which means you cannot grow an
      array by concatenating elements to the end:

      ::

         var integer[*] growme = [0]; // length is now 1
         var integer i = 1;
         loop while (i < 10) {
             growme = growme || i; // illegal: SizeError
             i = i + 1;
         }


   c. Dot Product

      Two rank-1 arrays with the same size and a numeric element type
      (types with the ``+`` and ``*`` operators) may be used in a dot
      product operation using the ``**`` operator. For rank-2 arrays
      (matrices), ``**`` instead performs matrix multiplication; see
      :ref:`ssec:matrix`. For instance:

      ::

         integer[3] v = [1, 2, 3];
         integer[3] u = [4, 5, 6];

         /* v[1] * u[1] + v[2] * u[2] + v[3] * u[3] */
         /* 1 * 4 + 2 * 5 + 3 * 6 = 32 */
         integer dot = v ** u;  /* Perform a dot product */


   d. Range

      The ``..`` operator creates an integer array holding the specified range
      of integer values.
      This operator must have an expression resulting in an integer on both
      sides of it. These integers mark the *inclusive* upper and lower bounds
      of the range.

      For example:

      ::

         1..10 -> std_output;
         (10-8)..(9+2) -> std_output;

      prints the following:

      ::

         [1 2 3 4 5 6 7 8 9 10]
         [2 3 4 5 6 7 8 9 10 11]

      The number of integers in a range may not be known at :term:`compile time`
      when the integer expressions use variables. In another example, assuming
      at :term:`run time` that ``i`` is computed as -4:

      ::

         i..5 -> std_output;

      prints the following:

      ::

         [-4 -3 -2 -1 0 1 2 3 4 5]

      Therefore, it is *valid* to have bounds that will produce an empty
      array because the difference between them is negative.

   e. Indexing

      An array may be indexed in order to retrieve the values stored in
      the array. An array may be indexed using an integer, in which case
      the index yields a single element, or using range syntax written
      directly at the index position, in which case the index yields a
      slice (see :ref:`sssec:array_slices`). An array *value* — including
      a range bound to a variable — is not a legal index.
      *Gazprea* is 1-indexed, so the first element of an array is at index 1
      (as opposed to index 0 in languages like *C*). For instance:

      ::

         integer[3] v = [4, 5, 6];
         integer x = v[2]; /* x == 5 */
         integer y = [4,5,6][3] /* y == 6 */

      Like Python, *Gazprea* allows negative indices, which are interpreted as
      starting from the *back* of the array instead of the front:

      ::

         integer[3] v = [4, 5, 6];
         integer x = v[-2]; /* x == 5 */
         integer y = [4,5,6][-1] /* y == 6 */

      The compiler must emit an ``IndexError`` (see :ref:`sec:errors`) for
      an out-of-bounds index, at :term:`compile time` or :term:`run time`.

   f. Slices

      A slice is a contiguous subset of array elements. Slice bounds
      and shorthand forms are specified in :ref:`sssec:array_slices`.

#. Operations of the Element Type

   Unary operations that are valid for the element type of an array may be
   applied to the array in order to produce an array whose result is
   the equivalent to applying that unary operation to each element of
   the array. For instance:

   ::

      boolean[*] v = [true, false, true, true];
      boolean[*] nv = not v;


   ``nv`` would have a value of
   ``[not true, not false, not true, not true] = [false, true, false, false]``.

   Similarly, most binary operations that are valid for the element type of an
   array may also be applied to two arrays. When applied to two
   arrays of the same size, the result of the binary operation is an
   array formed by the element-wise application of the binary operation
   to the array operands.

   ::

      [1, 2, 3, 4] + [2, 2, 2, 2] // results in [3, 4, 5, 6]


   The compiler must emit a ``SizeError`` (see :ref:`sec:errors`) when a
   binary operation is performed between two arrays of different sizes, at
   :term:`compile time` or :term:`run time`.

   When one of the operands of a binary operation is an array and the
   other operand is a scalar, the scalar value must first
   be implicitly cast to an array of the same size as the array operand and
   with the value of each element equal to the scalar value. For example:

   ::

      [1, 2, 3, 4] + 2 // results in [3, 4, 5, 6]


   Additionally the element types of arrays may be implicitly cast, for
   instance in this case the integer array must be implicitly cast to a real
   array in order to perform the operation:

   ::

      [1, 2, 3, 4] + 2.3 // results in [3.3, 4.3, 5.3, 6.3]


   The equality operation is the exception to the behavior of the binary
   operations. Instead of producing a boolean array, an equality
   operation checks whether or not all of the elements of two arrays
   are equal, and return a single boolean value reflecting the result of
   this comparison.

   ::

      [1, 2, 3] == [1, 2, 3]


   yields ``true``

   ::

      [1, 1, 3] == [1, 2, 3]


   yields ``false``

   The ``!=`` operation also produces a boolean instead of a boolean array.
   The result is the logical negation of the result of the ``==`` operator.

   Operator precedence and associativity are specified once, for all types,
   in the :ref:`table of operator precedence <ssec:expressions_toop>`.

.. _sssec:array_slices:

Array Slices
~~~~~~~~~~~~

An array slice is a contiguous subset of elements, described by a range.
The left hand bound is *inclusive* and the right hand bound is *exclusive*:
``a[i..j]`` selects the elements from ``i`` up to but not including ``j``.
(This differs from a range *value*, whose bounds are both inclusive:
``0..10`` written as an expression produces the integers 0 through 10, while
the same ``i..j`` syntax written inside an index position selects elements
with a right-exclusive bound.) A slice always selects a contiguous run of
elements.

The following forms are accepted inside an index position, where ``n`` is
the length of the array being sliced and elements are 1-indexed. A negative
right bound ``-i`` counts ``i`` positions back from the end and is likewise
exclusive, so ``..-1`` selects everything up to but not including the final
element:

+-----------+-----------------------------------------+
| Form      | Elements selected                       |
+===========+=========================================+
| ``..``    | all elements, ``1`` through ``n``       |
+-----------+-----------------------------------------+
| ``i..``   | ``i`` through ``n``                     |
+-----------+-----------------------------------------+
| ``..j``   | ``1`` through ``j-1``                   |
+-----------+-----------------------------------------+
| ``..-i``  | ``1`` through ``n-i``                   |
+-----------+-----------------------------------------+
| ``i..j``  | ``i`` through ``j-1``                   |
+-----------+-----------------------------------------+

An array slice is a **view** into the elements of its backing array, not a
copy:

-  As an :term:`lvalue`, a slice writes through to its backing array, and
   so is an lvalue only when that array is mutable (declared ``var``):

   ::

      var integer[3] a = [1, 2, 3];
      a[1..3] = [4, 5];
      a -> std_output; // [4, 5, 3]

   (``a[1..3]`` selects indices 1 and 2.)

-  As an :term:`rvalue`, a slice is a live, read-only view. A ``const``
   slice is such a read-only view and need not be built on a ``const``
   array -- it still reflects later changes to its backing array:

   ::

      var integer[3] a = [1, 2, 3];
      const b = a[1..3];
      b -> std_output; // [1, 2]
      a[2] = 4;
      b -> std_output; // [1, 4]

Further indexing and slicing shorthand forms are shown below.

::

    // 0..10 is a range value, not a slice
    integer[*] a = [0, 2, 4, 6, 8, 10];
    integer[2] x = a[2..4]; /* x == [2, 4] */
    integer y = a[2..4][1]; /* y == 2 */

    integer[*] u = a[..4];  /* u == [0, 2, 4] */
    integer[*] v = a[4..];  /* v == [6, 8, 10] */
    integer[*] w = a[..-1]; /* w == [0, 2, 4, 6, 8] */

    // A slice of the entire array behaves as the array itself, this can be repeated
    integer z1 = a[4];                   /* z1 == 6 */
    integer z2 = a[1..7][1..7][1..7][4]; /* z2 == 6 */


After resolving any negative bound, both ``i`` and ``j`` in ``a[i..j]`` must
lie between ``1`` and ``n + 1`` inclusive (a slice may stop just past the last
element); a bound outside that range is an ``IndexError`` (see
:ref:`sec:errors`), at :term:`compile time` or :term:`run time`, exactly as
for a single-element index.

A slice of a mutable (``var``) array is an :term:`lvalue`; used in a
parameter call or on the left side of an assignment, it allows modification
of the backing array, as in the following example. A slice of a ``const``
array may be used only as an :term:`rvalue`:


::

    procedure sum_arrays(const integer[*] in1, const integer[*] in2, var integer[*] out) {
        /* sum the two inputs and fill the output with the result */
    }

    procedure main() returns integer {

        integer[6] a = [0, 2, 4, 6, 8, 10];
        integer[6] b = [0, 3, 6, 9, 12, 15];
        var integer[6] c;          /* c must be var */

        /* procedure works normally with an array */
        call sum_arrays(a, b, c);
        c -> std_output; /* [0, 5, 10, 15, 20, 25] */

        /* procedure can also modify a slice */
        call sum_arrays(a[1..4], b[1..4], c[4..7]);
        c -> std_output; /* [0, 5, 10, 0, 5, 10] */

        /* slice can be assigned to, modifying c */
        c[3..5] = [415, 429];
        c -> std_output; /* [0, 5, 415, 429, 5, 10] */

        return 0;
    }

Because ``c[4..7]`` and ``c[3..5]`` are views over the mutable array ``c``,
each write passes through to ``c`` itself; no copy of ``c`` is made. A slice
is *always* a view, never a copy: binding one to a new variable (as in the
earlier examples) aliases the backing array's elements rather than copying
them, so a later write through either name is visible through the other. (A
dedicated copy operator is a planned future addition.)


Type Casting and Implicit Casts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see the types that an array may be cast and/or implicitly cast to, see
the sections on :ref:`sec:typeCasting` and :ref:`sec:implicitCasts`
respectively.

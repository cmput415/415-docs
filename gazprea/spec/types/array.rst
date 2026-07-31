.. _ssec:array:

Arrays
-------

Arrays are fixed size collections, where each element of the array has the
same type. The element type of an array may be any of *Gazprea*'s base types
(``boolean``, ``integer``, ``real``, and ``character``), or another array of a
base type, which yields a :ref:`matrix <ssec:matrix>`.

.. _sssec:array_sizing:

Sizing
~~~~~~

Arrays are **elaboration-time sized**. The length of an array variable is
determined exactly *once*, when its declaration is elaborated — that is, on the
first runtime effect of that array's accessor or assignment — and from that
point on the length is frozen for the entire lifetime of the variable.

Elaboration-time is not the same as compile-time. The size of an array may be
given by an arbitrary integer expression, so a length is not required to be a
compile-time constant; it is only required to be *settled* by the time the
array is first accessed or assigned, and to never change afterwards. Concretely:

-  A declaration such as ``integer[n] v;`` evaluates ``n`` once, at
   elaboration. Later changes to ``n`` have no effect on the length of ``v``.

-  A declaration such as ``integer[*] v = <expr>;`` takes its length from the
   value of ``<expr>`` at elaboration. The ``*`` means "infer this length once,
   here"; it does **not** mean the array is resizable.

-  No subsequent operation can change the length of an array variable.
   Assignment, concatenation, and casting all produce array *values*; storing
   such a value into an array variable never resizes that variable. If the
   value's length does not match, it is zero padded or a ``SizeError`` is
   raised, as described in the sections below.

If you need a collection whose length changes as the program runs, use a
:ref:`vector <ssec:vector>`, which is runtime sized. See
:ref:`sssec:array_vs_vector`.

.. _sssec:array_decl:

Declaration
~~~~~~~~~~~

Aside from any type specifiers, the element type of the array is the first
portion of the declaration. An array is then declared using square brackets
immediately after the element type.

If possible, initialization expressions may go through an implicit type
conversion. For instance, when declaring a real array that is
initialized with an integer value the integer will be promoted to a real
value, and then used as a scalar initialization of the array.
Be careful about type inference! If the type of the array is being inferred
from the right had side, the previous example would create an ``integer``
array instead of a ``real`` array.

#. Explicit Size Declarations

   When an array is declared it may be explicitly given a size. This
   size can be given as any integer expression, thus the size of the
   array may not be known until runtime.

   ::

            <type>[<int-expr>] <identifier>;
            <type>[<int-expr>] <identifier> = <type-expr>;
            <type>[<int-expr>] <identifier> = <type-array>;


   The size of the array is given by the integer expression between the
   square brackets. That expression is evaluated exactly once, when the
   declaration is elaborated, and its value becomes the permanent length of
   the array:

   ::

      var integer n = 3;
      var integer[n] v = 0;  /* 'v' has length 3, now and forever */
      n = 100;               /* 'v' still has length 3 */

   If the array is given a scalar value (``type-expr``) of the same element type then the
   scalar value is duplicated for every single element of the array.

   An array may also be initialized with another array. Initialization occurs element-wise,
   with the RHS element type's initialization semantics applying from left to right.
   If the LHS array is initialized using a RHS array that is too small then the LHS array will
   be padded with zeros. However, if the LHS array is initialized with a RHS
   array that is too large then a ``SizeError`` should be thrown at
   compile-time or run-time. Check the :ref:`ssec:errors_sizeErrors` section to know when you
   should throw the error.

   Note that the LHS length wins in both directions: the array is *not*
   shortened to the RHS length when the RHS is smaller, and it is *not* grown
   to the RHS length when the RHS is larger. This is what it means for the
   length to be fixed at elaboration.

#. Inferred Size Declarations

   If an array is assigned an initial value when it is declared, then
   its size may be inferred. There is no need to repeat the size in the
   declaration because the size of the array on the right-hand side is
   known.

   ::

            <type>[*] <identifier> = <type-array>;


   The inferred length is still an elaboration-time length. ``[*]`` only moves
   the choice of length from the declaration to the initializing expression;
   once elaboration has happened the array is as fixed in length as one
   declared with an explicit size:

   ::

      var integer[*] v = [1, 2, 3];  /* 'v' has length 3, now and forever */
      v = [4, 5];                    /* 'v' == [4, 5, 0] -- padded, not shrunk */
      v = [4, 5, 6, 7];              /* SizeError -- 'v' cannot grow */

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
   ``w`` from ``v``. The size may not always be known at compile time, so this
   may need to be handled during runtime; what matters is that the size is
   resolved when the declaration of ``w`` is elaborated and does not change
   thereafter.

.. _sssec:array_constr:

Construction
~~~~~~~~~~~~

An array value in *Gazprea* may be constructed using the following
notation:

::

   [expr1, expr2, ..., exprN]


Each ``expK`` is an expression with a compatible type. In the simplest
cases each expression is of the same type, but it is possible to mix the
types as long as all of the types can be promoted to a common type. For
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

Because the length of an array is fixed at elaboration, such an array has a
length of zero permanently; it is not an "empty, growable" array. A
:ref:`vector <ssec:vector>` declared without an initializer also starts empty,
but *can* subsequently grow.

.. _sssec:array_vs_vector:

Arrays Versus Vectors
~~~~~~~~~~~~~~~~~~~~~

*Gazprea* has two collection types that share the same element-wise operations
but differ in exactly one respect — when their length is decided:

+--------------------------+-------------------------------+-------------------------------+
|                          | **Array** (``T[N]``,          | **Vector** (``vector<T>``,    |
|                          | ``T[*]``)                     | ``string``)                   |
+==========================+===============================+===============================+
| When is the length set?  | Once, at elaboration          | Continuously, at runtime      |
+--------------------------+-------------------------------+-------------------------------+
| Can the length change    | No                            | Yes                           |
| after that?              |                               |                               |
+--------------------------+-------------------------------+-------------------------------+
| Written in the type?     | Yes (``[N]``), or inferred    | No                            |
|                          | once (``[*]``)                |                               |
+--------------------------+-------------------------------+-------------------------------+
| Grows via ``push`` /     | No — ``SizeError``            | Yes                           |
| ``append``?              |                               |                               |
+--------------------------+-------------------------------+-------------------------------+
| Too-short value assigned | Zero padded to the array's    | Vector takes the value's      |
| into it                  | fixed length                  | length                        |
+--------------------------+-------------------------------+-------------------------------+
| Too-long value assigned  | ``SizeError``                 | Vector takes the value's      |
| into it                  |                               | length                        |
+--------------------------+-------------------------------+-------------------------------+

The two types interoperate, but only through *values*: a vector used in an
array context yields an array value of the vector's current length, and an
array value assigned into a vector sets that vector's length. Neither direction
ever makes an array variable resizable. See :ref:`ssec:vector` for the details
of that interoperation.

.. _sssec:array_ops:

Operations
~~~~~~~~~~

#. Array Operations and functions

   a. length

      The number of elements in an array is given by the built-in
      functions ``length``. For instance:

      ::

         integer[*] v = [8, 9, 6];
         integer numElements = length(v);


      In this case ``numElements`` would be 3, since the array ``v``
      contains 3 elements. For an array, ``length`` is invariant after
      elaboration: it will report the same value for every call on the same
      variable. For a :ref:`vector <ssec:vector>` it reports the current
      length, which may differ between calls.

   b. Concatenation

      Two arrays with the same element type may be concatenated into a
      single array using the concatenation operator, ``||``. For
      instance:

      ::

         [1, 2, 3] || [4, 5] // produces [1, 2, 3, 4, 5]
         [1, 2] || [] || [3, 4] // produces [1, 2, 3, 4]


      Concatenation is also allowed between arrays of different element
      types, as long as one element type is coerced automatically to the
      other. For instance:

      ::

         integer[3] v = [1, 2, 3];
         real[3] u = [4.0, 5.0, 6.0];
         real[6] j = v || u;


      would be permitted, and the integer array ``v`` would be promoted to
      a real array before the concatenation.

      Concatenation may also be used with scalar values. In this case
      the scalar values are treated as though they were single element
      arrays.

      ::

         [1, 2, 3] || 4 // produces [1, 2, 3, 4]
         1 || [2, 3, 4] // produces [1, 2, 3, 4]


      An interesting corollary to array-scalar concatenation is that
      two scalars can be concatenated to produce an array:

      ::

         integer[3] v = 1 || 2 || 3; // produces [1, 2, 3]


      Concatenation produces a new array *value* whose length is the sum of
      the lengths of its operands. It does not extend either operand.
      Remember that arrays have a fixed length, which means you cannot grow an
      array by concatenating elements to the end:

      ::

         var integer[*] growme = [0]; // elaborated with length 1; fixed at 1
         var integer i = 1;
         loop while (i < 10) {
             growme = growme || i; // SizeError: a length-2 value into a length-1 array
             i = i + 1;
         }

      Use a :ref:`vector <ssec:vector>` when the collection has to grow:

      ::

         var vector<integer> growme = 0; // [0]
         var integer i = 1;
         loop while (i < 10) {
             growme.push(i); // fine: vectors are runtime sized
             i = i + 1;
         }


   c. Dot Product

      Two arrays with the same size and a numeric element type(types with
      the ``+``, and ``\*`` operator) may be used in a dot product operation.
      For instance:

      ::

         integer[3] v = [1, 2, 3];
         integer[3] u = [4, 5, 6];

         /* v[1] * u[1] + v[2] * u[2] + v[3] * u[3] */
         /* 1 * 4 + 2 * 5 + 3 * 6 &=&  32 */
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

      The number of integers in a range may not be known at compile time when
      the integer expressions use variables. In another example, assuming at
      runtime that ``i`` is computed as -4:

      ::

         i..5 -> std_output;

      prints the following:

      ::

         [-4 -3 -2 -1 0 1 2 3 4 5]

      Therefore, it is *valid* to have bounds that will produce an empty
      array because the difference between them is negative.

      A range yields an array *value*, whose length is settled when the range
      expression is evaluated. Using a range to initialize an array variable
      with an inferred size is therefore one of the ways an array's length
      gets fixed at elaboration:

      ::

         var integer i = 3;
         var integer[*] v = 1..i;  /* 'v' is elaborated with length 3 */
         i = 10;
         v = 1..i;                 /* SizeError: 'v' is still length 3 */

   d. Indexing

      An array may be indexed in order to retrieve the values stored in
      the array. An array may be indexed using integers.
      *Gazprea* is 1-indexed, so the first element of an array is at index 1
      (as opposed to index 0 in languages like *C*). For instance:

      ::

         integer[3] v = [4, 5, 6];
         integer x = v[2]; /* x == 5 */
         integer y = [4,5,6][3] /* y == 6 */

      Like Python, *Gazprea* allows negative indices, which are interpreted as
      starting from the _back_ of the array instead of the front:

      ::

         integer[3] v = [4, 5, 6];
         integer x = v[-2]; /* x == 5 */
         integer y = [4,5,6][-1] /* y == 6 */

      Out of bounds indexing should cause an error.

   e. Stride

      The ``by`` operator is used to specify a step-size greater than 1 when
      indexing across an array. It produces a new array with the values
      indexed by the given stride. For instance:

      ::

         integer[*] v = 1..5 by 1; /* [1, 2, 3, 4, 5] */
         integer[*] u = v by 1; /* [1, 2, 3, 4, 5] */
         integer[*] w = v by 2; /* [1, 3, 5] */
         integer[*] l = v by 3; /* [1, 4] */
         integer[*] s = v by 4; /* [1, 5] */

   d. Slices

      An array may be indexed by a range to create a new array that is a *slice*
      of the original. The left hand index is inclusive, while the right is exclusive.

      ::

         integer[*] a = 0..10 by 2; /* a = [0, 2, 4, 6, 8, 10] */
         integer[2] x = a[2..4]; /* x == [2, 4] */

      Note that for slices only a stride of 1 is allowed.
      For indexing purposes three additions are made to range syntax:

      +---------+---------------------------------+
      | Syntax  | Interpretation                  |
      +=========+=================================+
      | `..`    | all elements                    |
      +---------+---------------------------------+
      | `i..`   | ith to nth elements             |
      +---------+---------------------------------+
      | `..-i`  | first to n-i-1th elements       |
      +---------+---------------------------------+
      | `i..j`  | i to jth elements               |
      +---------+---------------------------------+

      Examples:

      ::

         integer[*] a = 0..10 by 2; /* a = [0, 2, 4, 6, 8, 10] */
         integer[*] x = a[..4]; /* x == [0, 2, 4] */
         integer[*] y = a[4..]; /* y == [6, 8, 10] */
         integer[*] z = a[..-1]; /* z == [0, 2, 4, 6, 8] */

      A slice is an array *value*, not a view that tracks the sliced array.
      Its length is determined when the slice expression is evaluated. Slicing
      a :ref:`vector <ssec:vector>` is the standard way to obtain an array
      value from a runtime-sized collection.

#. Operations of the Element Type

   Unary operations that are valid for the Element type of an array may be
   applied to the array in order to produce an array whose result is
   the equivalent to applying that unary operation to each element of
   the array. For instance:

   ::

      boolean[*] v = [true, false, true, true];
      boolean[*] nv = not v;


   ``nv`` would have a value of
   ``[not true, not false, not true, not true] = [false, true, false, false]``.

   Similarly most binary operations that are valid to the element type of a
   array may be also applied to two arrays. When applied to two
   arrays of the same size, the result of the binary operation is a
   array formed by the element-wise application of the binary operation
   to the array operands.

   ::

      [1, 2, 3, 4] + [2, 2, 2, 2] // results in [3, 4, 5, 6]


   Attempting to perform a binary operation between two arrays of
   different sizes should result in a ``SizeError``.

   When one of the operands of a binary operation is an array and the
   other operand is a scalar, the scalar value must first
   be promoted to an array of the same size as the array operand and
   with the value of each element equal to the scalar value. For example:

   ::

      [1, 2, 3, 4] + 2 // results in [3, 4, 5, 6]


   Additionally the element types of arrays may be promoted, for instance
   in this case the integer array must be promoted to a real array in
   order to perform the operation:

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


Type Casting and Type Promotion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see the types that an array may be cast and/or promoted to, see
the sections on :ref:`sec:typeCasting` and :ref:`sec:typePromotion`
respectively.

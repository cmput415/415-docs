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

Note that the empty array literal ``[]`` carries no element type of its own, so
the element type must come from context (the declared type, as in
``real[*] v = []`` above). A declaration that elides the type and asks the
compiler to infer it from an empty literal -- such as ``var v = [];`` -- is
:term:`ill-formed`, because the element type cannot be deduced; the compiler
must emit a ``TypeError`` (see :ref:`sec:errors`). The same holds anywhere a
bare ``[]`` appears without a type to fix its element type (see also
:ref:`ssec:typeCasting_vtov` and :ref:`ssec:expressions_dom_expr`).

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

         integer[3] v = 1 || 2 || 3;   // TypeError: all operands are scalars
         integer[3] w = [1] || 2 || 3; // [1, 2, 3]: left operand is an array


      Concatenation is right-associative, and its *receiver* -- the rightmost
      operand -- fixes the **kind** of the result. When the receiver is a
      :ref:`vector <ssec:vector>` (a ``vector<T>`` or a ``string``), the whole
      concatenation is a vector of that element type; otherwise -- when the
      receiver is an array or a scalar -- the result is an array, exactly as in
      the examples above. Nothing else about concatenation changes: at least one
      operand must still be composite, and the operands must share a common
      element type through implicit casts. This is what keeps a string
      concatenation such as ``"x = " || format(x)`` a ``string`` (its receiver
      ``format(x)`` is a string), so it renders as text when sent to a stream,
      while a vector result can still be stored into an array through the usual
      :ref:`vector/array interoperability <ssec:implicitCasts_avv>`.


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
      product operation using the ``**`` operator. The two operands must
      have the same size; if they do not, the compiler must emit a
      ``SizeError`` (see :ref:`sec:errors`) at :term:`compile time` or
      :term:`run time`. The dot product is the rank-1 case of a single rule:
      ``**`` is defined for numeric arrays of any rank as the linear-algebra
      contraction of the last dimension of the left operand with the first
      dimension of the right operand, so the rank-2 case is matrix
      multiplication. See :ref:`ssec:matrix` for the general definition and its
      ``SizeError``. For instance:

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
      sides of it. The range is **half-open**: the left bound is *inclusive*
      and the right bound is *exclusive*, so ``i..j`` holds the integers ``i,
      i+1, ..., j-1``. This is the same convention used when a range is written
      inside an index position to form a :ref:`slice <sssec:array_slices>`, so a
      range value and a slice agree on exactly which endpoints they include.

      For example:

      ::

         1..10 -> std_output;
         (10-8)..(9+2) -> std_output;

      prints the following:

      ::

         [1 2 3 4 5 6 7 8 9]
         [2 3 4 5 6 7 8 9 10]

      The number of integers in a range may not be known at :term:`compile time`
      when the integer expressions use variables. In another example, assuming
      at :term:`run time` that ``i`` is computed as -4:

      ::

         i..5 -> std_output;

      prints the following:

      ::

         [-4 -3 -2 -1 0 1 2 3 4]

      Therefore, it is *valid* to have bounds that will produce an empty
      array: because the right bound is *exclusive*, ``i..j`` is empty whenever
      ``i >= j`` (for example ``5..5`` or ``5..2``).

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

   Only ``==`` and ``!=`` collapse to a single boolean in this way. The
   *ordering* comparisons ``<``, ``>``, ``<=``, and ``>=`` follow the ordinary
   element-wise rule: applied between two arrays of the same size they produce
   a ``boolean`` array (a bitmask) of that size, whose element ``k`` is the
   comparison of the two operands' element ``k``. As with any element-wise
   binary operation, a size mismatch is a ``SizeError`` (see :ref:`sec:errors`)
   and a scalar operand is first broadcast to the array's size. For example:

   ::

      [1, 5, 3] < [2, 2, 2] // results in [true, false, false]
      [1, 2, 3] <= 2        // results in [true, true, false]

   Operator precedence and associativity are specified once, for all types,
   in the :ref:`table of operator precedence <ssec:expressions_toop>`.

.. _sssec:array_slices:

Array Slices
~~~~~~~~~~~~

An array slice is a contiguous subset of elements, described by a range.
The left hand bound is *inclusive* and the right hand bound is *exclusive*:
``a[i..j]`` selects the elements from ``i`` up to but not including ``j``. This
is the identical half-open convention used by a range *value* (see the
:ref:`range operator <sssec:array_ops>`), so ``i..j`` picks out the same
endpoints whether it is written as a value or inside an index position. A slice
always selects a contiguous run of elements.

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

Whether a slice copies or writes through depends on where it appears: a slice is
a **copy when read** and a **view when assigned to**.

-  **In value position** (an :term:`rvalue`) -- as an initializer, on the right
   of an assignment, as an argument bound to a ``const`` parameter, or anywhere
   an array value is expected -- a slice produces a **fresh, independent array**
   holding a *copy* of the selected elements. Binding it to a variable creates a
   new array; the copy and the original never observe each other's later writes.
   Because the elements are copied, the source array need not be mutable -- a
   slice of a ``const`` array is perfectly legal here -- and the copy's own
   mutability is decided by the declaration that receives it:

   ::

      integer[3] a = [1, 2, 3];   // a is const (the default)
      var b = a[1..3];            // b is a fresh var integer[2] == [1, 2] (a copy)
      b[1] = 9;                   // b == [9, 2]; a is unchanged, still [1, 2, 3]

   (``a[1..3]`` selects indices 1 and 2.)

-  **In assignment-target position** (an :term:`lvalue`) -- on the *left* of an
   assignment, or bound to a ``var`` reference parameter -- a slice is a **view**
   that writes *through* to its backing array. This is the only situation in
   which a slice aliases storage, and it requires the backing array to be mutable
   (declared ``var``); a slice of a ``const`` array is never an lvalue. The
   assigned value is fitted to the slice's length exactly as for a whole-array
   assignment -- a shorter value is padded with the element type's
   :term:`zero value` and a longer value is a ``SizeError`` (see
   :ref:`sssec:array_sizing`):

   ::

      var integer[3] a = [1, 2, 3];
      a[1..3] = [4, 5];           // writes through: a == [4, 5, 3]
      a -> std_output;            // [4, 5, 3]

This copy-on-read, view-on-assignment split applies unchanged to arrays of any
rank; the higher-rank case is described below and in :ref:`ssec:matrix`.

Slicing shorthand forms are shown below. Each names a slice in value position,
so each is an ordinary array value (a copy):

::

    // 0..10 is a range value, not a slice
    integer[*] a = [0, 2, 4, 6, 8, 10];
    integer[2] x = a[2..4]; /* x == [2, 4] (a fresh copy) */

    integer[*] u = a[..4];  /* u == [0, 2, 4] */
    integer[*] v = a[4..];  /* v == [6, 8, 10] */
    integer[*] w = a[..-1]; /* w == [0, 2, 4, 6, 8] */

To index *into* the array that a slice produces, bind it to a variable (or
parenthesize the slice) and index that value; being a copy, it behaves as any
other array value:

::

    integer[*] a = [0, 2, 4, 6, 8, 10];
    var s = a[2..4];        /* s is a fresh integer[2] copy == [2, 4] */
    integer y = s[1];       /* y == 2 */


After resolving any negative bound, both ``i`` and ``j`` in ``a[i..j]`` must
lie between ``1`` and ``n + 1`` inclusive (a slice may stop just past the last
element); a bound outside that range is an ``IndexError`` (see
:ref:`sec:errors`), at :term:`compile time` or :term:`run time`, exactly as
for a single-element index.

A slice whose (in-bounds) left bound is greater than its right bound, such as
``a[4..2]``, is **not** an error: like a range value with a negative difference
(see :ref:`sssec:array_ops`), it simply selects no elements and yields an empty
array of ``a``'s element type.

Slicing generalizes to arrays of any rank. Indexing is *positional*: in a
subscript chain ``a[s1][s2]...[sk]`` the subscript ``sm`` applies to axis ``m``
of ``a``, and a rank-``k`` array accepts up to ``k`` index positions (see
:ref:`ssec:matrix`). An axis indexed by a single integer is dropped from the
result; an axis indexed by a range is kept, holding the selected run -- so the
rank of the result is the number of index positions that are ranges. The
copy-on-read, view-on-assignment rule carries over per selection: the result is
a copy when read and a write-through view when it is the target of an
assignment.

::

    // a rank-3 array whose 27 elements are 1, 2, 3, ..., 27 in order
    var integer[3][3][3] a = ...;

    // axis 1 by an integer (dropped); axes 2 and 3 by ranges (kept):
    var b = a[1][1..3][1..3];   // a fresh integer[2][2] copy == [[1, 2], [4, 5]]

    // the same positional selection as an lvalue writes through to a:
    a[2][1..3][1..3] = [[28, 29], [30, 31]];  // updates those four elements of a

Because a subscript chain names successive axes rather than re-indexing an
intermediate result, writing more index positions than the array has axes is
*not* how one indexes into a slice's result; for that, bind the slice to a
variable (or parenthesize it) and index the resulting value, as shown above.

A slice may also be handed to a :ref:`function <sec:function>` or
:ref:`procedure <sec:procedure>`. In an argument position it follows the same
copy-or-view rule as everywhere else, decided by the *parameter* it binds to:

-  A slice bound to a ``const`` parameter is passed **by value** -- the callee
   receives a copy of the selected elements and cannot reach the caller's array
   through it. Every :ref:`function <sec:function>` parameter is ``const``
   (functions are pure), so a slice passed to a function is always such a copy.

-  A slice bound to a ``var`` parameter -- available only for
   :ref:`procedures <ssec:procedure_vec_mat>`, whose parameters may be ``var`` --
   is passed **by reference**: it is a view that writes *through* to the backing
   array, exactly as an lvalue slice does, so the callee's writes are visible to
   the caller once the call returns. This requires the backing array to be
   ``var``.

An implementation may still pass a ``const`` slice by reference for efficiency:
because the callee only reads it, the choice is unobservable, and *Gazprea*'s
value semantics -- realized directly by *MLIR* -- make the copy and the shared
reference indistinguishable in that case.

::

    procedure sum_arrays(const integer[*] in1, const integer[*] in2, var integer[*] out) {
        /* sum the two inputs and fill the output with the result */
    }

    procedure main() returns integer {

        integer[6] a = [0, 2, 4, 6, 8, 10];   /* a and b are const */
        integer[6] b = [0, 3, 6, 9, 12, 15];
        var integer[6] c;                      /* c must be var */

        /* procedure works normally with whole arrays */
        call sum_arrays(a, b, c);
        c -> std_output; /* [0, 5, 10, 15, 20, 25] */

        /* a[1..4] and b[1..4] are copied into the const parameters;
           c[4..7] is a var slice, so writes pass through to c */
        call sum_arrays(a[1..4], b[1..4], c[4..7]);
        c -> std_output; /* [0, 5, 10, 0, 5, 10] */

        /* a slice on the left of an assignment writes through to c */
        c[3..5] = [415, 429];
        c -> std_output; /* [0, 5, 415, 429, 5, 10] */

        return 0;
    }

Here ``c[4..7]`` and ``c[3..5]`` are lvalue slices of the mutable array ``c``,
so each write passes through to ``c`` itself; ``a[1..4]`` and ``b[1..4]``, bound
to ``const`` parameters, are copied and leave ``a`` and ``b`` untouched.


Type Casting and Implicit Casts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see the types that an array may be cast and/or implicitly cast to, see
the sections on :ref:`sec:typeCasting` and :ref:`sec:implicitCasts`
respectively.

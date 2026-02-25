.. _ssec:array:

Arrays
------

Arrays are ordered, homogeneous collections of elements. *Gazprea*'s array
system offers a unified syntax for
statically-sized, dynamically-sized, and multi-dimensional arrays.

An array's elements can be of any single type, including base types (
``boolean``,
``integer``, ``real``), compound types (``tuple``), and other arrays.

.. _sssec:array_lrvalue:

L-values and R-values
~~~~~~~~~~~~~~~~~~~~~

Every expression in *Gazprea* has a **value category**: either an *lvalue*
or an *rvalue*, which governs the role the expression may take and
how the result of the expression is stored. A full
discussion of value categories, including their relationship to the richer
C++ taxonomy (glvalue, xvalue, prvalue), is given in
:ref:`sec:value_categories`.

For arrays the key consequence is that **slice expressions are rvalues**.
A slice such as ``v[2..5]`` produces, semantically, a new, independent
deep copy of the
selected elements. Because it is an rvalue, a slice:

- cannot appear on the left-hand side of an assignment, and
- cannot be passed as a ``var`` (mutable) parameter to a procedure.

Attempting either is a compile-time error. Because slices semantically produce
deep copies
and carry no persistent address, they do not participate in aliasing analysis
(see :ref:`ssec:procedure_alias`).

.. _sssec:array_decl:

Declaration
~~~~~~~~~~~

An array type is specified by providing a shape in
square brackets (``[]``) to a type.

#. Static vs. Dynamic Sizing

   *Gazprea* distinguishes between arrays whose size is fixed at compile time
   (static) and arrays that can change size at runtime (dynamic).

   -  A **static dimension** is declared using an integer literal or a
      :ref:`constant expression <sec:constexpr>`.
   -  A **dynamic dimension** is declared using an asterisk (``*``).

   ::

        // A statically-sized array of 10 integers.
        //  initialized to 0 elementwise
        var integer[10] a;

        // A dynamically-sized array of integers.
        //  initialized to integer[0], with shape() = [0]
        var integer[*] b;

   .. note::

      The ``*`` token is a syntactic marker meaning "size not declared here",
      but it is **not** the sole property that makes an array dynamic. An array
      is dynamic when its size cannot be determined at compile time:

      -  ``integer[x]`` is dynamic whenever ``x`` is not a
         :ref:`constant expression <sec:constexpr>`, no ``*`` is required.
      -  ``integer[*] a = [1, 2, 3]`` may be treated as **static** by the
         compiler because the initialiser literal has a known length of 3.
         A conforming implementation is free to allocate ``a`` on the stack
         just like ``integer[3] a = [1, 2, 3]``.

      The distinction matters for implementations: only arrays whose size is
      genuinely unknown at compile time require dynamic memory management
      (heap allocation, runtime resize, etc.). Arrays whose size is
      determinable from their initialiser, regardless of whether the
      declaration uses a literal or ``*``, may be stack-allocated like any
      fixed-size value.

#. N-Dimensional Arrays

   Multi-dimensional arrays are declared by providing a comma-separated list of
   dimension specifiers (the shape). There are some restrictions on which 
   dimension can be static or dynamic: i) There may only be one (1) dynamic
   dimension per n-d array, ii) the last dimension of an n-d array with n > 1
   cannot be dynamic. This prevents the creation of jagged arrays, however
   arrays can hold tuples and vice-versa which provides an avenue for emulating
   jagged arrays.

   ::

        // A 3x4 2d-array of real numbers.
        var real[3, 4] matrix;

        // A dynamic list of static 3-element integer vectors.
        var integer[*, 3] vectors;

        // a jagged array definition
        var integer[3, *] jagged; // illegal, compile time error
        var tuple(integer[*], integer[*], integer[*]) jagged; //equivalent


#. Inferred Type and Size

   When initializing a variable with an array literal, its type and size can
   be inferred by the compiler using ``var``. The resulting array is always
   statically-sized unless _any_ initializer contains a dynamic dimension
   or is a dynamically-sized array.

   ::

      // v is inferred as type integer[3].
      var v = [1, 2, 3];

      // w is inferred as type real[2, 2].
      var w = [[1.0, 2.0], [3.0, 4.0]];

      // x is inferred as type integer[5].
      var integer[*] dyn = [1, 2, 3, 4, 5];
      var x = [...dyn];

.. _sssec:array_constr:

Construction
~~~~~~~~~~~~

An array value is constructed using a comma-separated list of expressions
within square brackets. All elements must share a common promotable type.
The element type of an unspecified array is the top-most type in the type
hierarchy that elements can be _implicitly_ promoted to. Any other unpromotable
types will result in a compile-time type error.

::

   [1, 2, 3]                     // An integer array
   [1, 2.5, 3]                   // A real array (integer 1 is promoted)
   [(1, true), (2, false)]       // An array of tuples
   [1, [2, 3], [4, 5, 6]]        // A ragged integer array integer[3,*]

*Gazprea* supports empty array literals (``[]``). The literal has no inherent
type and acquires its element type from the declared variable type.

A dynamic array (``integer[*]``) initialised with ``[]`` starts as an empty,
growable array. A static array of size zero (``integer[0]``) is also legal,
though of limited practical use. Any other static size is a compile-time
``SizeError``.

Because ``[]`` carries no element type, **type inference cannot be used with
an empty array literal.** A declaration of the form ``var x = []`` is a
compile-time ``TypeError`` since the compiler has no information from which to
derive the element type of ``x``.

::

    var integer[*] a = []; // Legal: dynamic empty array
    integer[0] b = [];     // Legal: static array of size zero (not very useful)
    var integer[5] c = []; // Illegal: size mismatch, static array needs 5 elements
    var d = [];            // Illegal: element type cannot be inferred from []

.. _sssec:array_spread:

Spread Operator
~~~~~~~~~~~~~~~

The spread operator (``...``) provides a concise, declarative way to construct
a new array by unpacking elements from existing arrays. It can be used multiple
times within an array literal and can be combined with other elements.

The spread operator is a syntactic feature **exclusive** to array literals.
It is
evaluated left-to-right.

::

   var integer[2] a = [1, 2];
   var integer[3] b = [3, 4, 5];

   // c becomes [0, 1, 2, 3, 4, 5, 6]
   var integer[7] c = [0, ...a, ...b, 6];

When constructing a static array, the compiler must be able to verify the final
size at compile time. Spreading a dynamic array into a static array is a
compile-time size error. See :ref:`sec:constexpr` for more details.

.. _sssec:array_ops:

Operations
~~~~~~~~~~

#. Indexing and Slicing

   -  **Indexing:** Elements of an N-dimensional array are accessed using a
      comma-separated list of 1-based integer indices. Negative indices count
      from the end of a dimension.
   -  **Slicing (Deep Copy):** A slice expression creates a **new, independent
      array** by performing a **deep copy** of a segment of an existing array.
      The resulting array has its own memory, and modifications to it will
      never affect the original array. This behavior is consistent with
      *Gazprea*'s rule that all assignments are deep copies.

      A slice expression is an **r-value**, meaning it produces a value and
      cannot be the target of an assignment. For N-D arrays, slicing is only
      permitted on the last dimension.

      .. note::

         Implementations are **not** required to perform an eager copy when a
         slice is passed to a function or procedure. A lazy strategy such as
         Copy-On-Write is permitted because slices are always passed as
         ``const`` parameters and therefore cannot be mutated by the callee.
         See :ref:`sec:impl_slice_passing` for guidance.

   ::

        var integer[5] a = [10, 20, 30, 40, 50];

        // Legal: Create a new array 'b' from a slice of 'a'.
        var integer[3] b = a[2..5]; // b is [20, 30, 40]

        // 'b' is independent of 'a'.
        b[1] = 99; // 'a' remains [10, 20, 30, 40, 50]

        // Illegal: A slice is not an l-value and cannot be assigned to.
        a[1..3] = [1, 2]; // COMPILE-TIME ERROR

#. shape

   The built-in function ``shape`` returns the shape of an array as a
   dynamically-sized integer array (``integer[*]``).

   For n-d arrays, ``shape`` returns the shape of the array using -1
   as a marker value for dynamic dimensions.

   ::

      var integer[10] a;
      shape(a) // returns [10]

      var real[3, 4] b;
      shape(b) // returns [3, 4]

      var character[5, *, 4] c;
      shape(c) // returns [5, -1, 4]

#. Concatenation (``||``)

   The ``||`` operator concatenates two arrays. This operation is primarily
   useful for **dynamically-sized arrays**.

   ::

      var integer[*] a = [1, 2];
      a = a || [3, 4]; // a is now [1, 2, 3, 4]

      var integer[*, 4] b; // integer[0, 4], growable
      b = b || [1, 2, 3, 4]; // integer[1, 4]

      var integer[1, *, 2] c; // integer[1, 0, 2] = [[]];
      c = c || [[[1, 2]]]; // c = [[[1, 2]]]

   The :ref:`spread operator <sssec:array_spread>` is the preferred method for
   composition of arrays. Note that working with a dynamically-sized array 
   implies that
   the size check must be performed at runtime, however some arrays will have
   constant size obtainable at compile time.

#. Element-wise Operations and Broadcasting

   Unary and binary operations (e.g., ``not``, ``+``, ``-``, ``*``) can be applied
   element-wise to arrays.

   -  For operations between two arrays, their dimensions must be compatible.
   -  For operations between an array and a scalar, the scalar is **broadcast**
      across the array.

   *Gazprea* follows a simple "trailing dimensions" rule for broadcasting: an
   array ``A`` can be broadcast over array ``B`` if ``A``'s dimensions are a suffix
   of ``B``'s dimensions.

   ::

      var integer[3, 4] m = ...;
      var integer[4] n = [1, 2, 3, 4];
      var s = 10;

      var r1 = m + s; // Legal: scalar broadcast
      var r2 = m + v; // Legal: [4] is a suffix of [3, 4]. v is added to each row.

      var integer[3] v2;
      var r3 = m + v2; // Illegal: [3] is not a suffix of [3, 4].

   The equality operators ``==`` and ``!=`` are an exception. They perform a
   deep, element-wise comparison and return a single ``boolean`` value.

   These element-wise operations are fully supported for dynamic arrays where the
   shape is regular (e.g., ``integer[*]``, ``integer[*, 5]``). Compatibility
   checks can be performed either at runtime or compile time, and a ``SizeError``
   will be thrown if
   the shapes are incompatible.

.. _sssec:array_taxonomy:

Array Type Summary
~~~~~~~~~~~~~~~~~~

The following table summarises the different array forms in *Gazprea*, their
declaration syntax, the meaning of each wildcard (``*``) position, and the
key restrictions that apply.

+------------------------+-------------------+----------------------------------------------+------------------------------------+
| **Form**               | **Declaration**   | **Description**                              | **Element-wise ops allowed?**      |
+========================+===================+==============================================+====================================+
| Static                 | ``T[N]``          | Size fixed at compile time. ``N`` must be a  | Yes: size known at compile time.  |
|                        |                   | literal or :ref:`constexpr <sec:constexpr>`. |                                    |
+------------------------+-------------------+----------------------------------------------+------------------------------------+
| Static N-D             | ``T[N, M]``       | All dimensions fixed at compile time.        | Yes: checked at compile time.     |
+------------------------+-------------------+----------------------------------------------+------------------------------------+
| Dynamic 1-D            | ``T[*]``          | Size unknown at compile time; grows          | Yes: shape checked at runtime.    |
|                        |                   | or shrinks at runtime.                       |                                    |
+------------------------+-------------------+----------------------------------------------+------------------------------------+
| Regular dynamic N-D    | ``T[*, N]``       | Leading dimension(s) dynamic; final          | Yes: shape checked at runtime.    |
|                        |                   | dimension(s) static. All rows have the       |                                    |
|                        |                   | same fixed inner length.                     |                                    |
+------------------------+-------------------+----------------------------------------------+------------------------------------+


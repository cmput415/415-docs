.. _ssec:vector:

Vectors
-------

Vectors are arrays that can contain any of the following base types:

-  ``boolean``

-  ``integer``

-  ``real``

-  ``character``

In *Gazprea* the number of elements in the vector also determine its
type. A 3 element vector of any base type is always considered a different
type from a 2 element vector.

.. _sssec:vector_decl:

Declaration
~~~~~~~~~~~

Aside from any type specifiers, the element type of the vector is the first
portion of the declaration. A vector is then declared using square brackets 
immediately after the element type.

If possible, initialization expressions may go through an implicit type
conversion. For instance, when declaring a real vector if it is
initialized with an integer value the integer will be promoted to a real
value, and then used as a scalar initialization of the vector.

#. Explicit Size Declarations

   When a vector is declared it may be explicitly given a size. This
   size can be given as any integer expression, thus the size of the
   vector may not be known until runtime.

   ::

            <type>[<int-expr>] <identifier>;
            <type>[<int-expr>] <identifier> = <type-expr>;
            <type>[<int-expr>] <identifier> = <type-vector>;
      					

   The size of the vector is given by the integer expression between the
   square brackets.

   If the vector is given a scalar value of the same element type then the
   scalar value is duplicated for every single element of the vector.

   A vector may also be initialized with another vector. If the vector
   is initialized using a vector that is too small then the vector will
   be null padded. However, if the vector is initialized with a vector
   that is too large then a type error will occur.

#. Inferred Size Declarations

   If a vector is assigned an initial value when it is declared, then
   its size may be inferred. There is no need to repeat the size in the
   declaration because the size of the vector on the right-hand side is
   known.

   ::

            <type>[*] <identifier> = <type-vector>;
      					

#. Inferred Type and Size

   It is also possible to declare a vector with an implied type and
   length using the var keyword. This type of declaration can only be
   used when the variable is initialized in the declaration, otherwise
   the compiler will not be able to infer the type or the size of the
   vector.

   ::

      						integer[*] v = [1, 2, 3];
      						var w = v + 1;
      					

   In this example the compiler can infer both the size and the type of
   w from v. The size may not always be known at compile time, so this
   may need to be handled during runtime.

.. _sssec:vector_null:

Null
~~~~

Vector of ``null`` elements.

When initializing a vector to a value of ``null`` an explicit size must
be given. Such initialization is equivalent to promoting a ``null``
value of the element type to the vector.

.. _sssec:vector_ident:

Identity
~~~~~~~~

Vector of ``identity`` elements.

When initializing a vector to a value of ``identity`` an explicit size
must be given. Such initialization is equivalent to promoting a
``identity`` value of the element type to the vector.

.. _sssec:vector_constr:

Construction
~~~~~~~~~~~~

A vector value in *Gazprea* may be constructed using the following
notation:

::

   				[expr1, expr2, ..., exprN]
   			

Each ``expK`` is an expression with a compatible type. In the simplest
cases each expression is of the same type, but it is possible to mix the
types as long as all of the types can be promoted to a common type. For
instance it is possible to mix integers and real numbers.

::

   				real[*] v = [1, 3.3, 5 * 3.4];
   			

It is also possible to construct a single-element vector using this
method of construction.

::

   				real[*] v = [7];
   			

*Gazprea* **DOES** support empty vectors.

::

   				real[*] v = []; /* Should create an empty vector */
   			

.. _sssec:vector_ops:

Operations
~~~~~~~~~~

#. Vector Operations and functions

   a. length 
      
      The number of elements in a vector is given by the built-in
      functions ``length``. For instance:

      ::

         								integer[*] v = [8, 9, 6];
         								integer numElements = length(v);
         							

      In this case ``numElements`` would be 3, since the vector v
      contains 3 elements.

   b. Concatenation

      Two vectors with the same element type may be concatenated into a
      single vector using the concatenation operator, ``||``. For
      instance:

      ::

         								[1, 2, 3] || [4, 5] // produces [1, 2, 3, 4, 5]
         								[1, 2] || [] || [3, 4] // produces [1, 2, 3, 4]
         							

      Concatenation is also allowed between vectors of different element
      types, as long as one element type is coerced automatically to the
      other. For instance:

      ::

         								integer[3] v = [1, 2, 3];
         								real[3] u = [4.0, 5.0, 6.0];
         								real[6] j = v || u;
         							

      would be permitted, and the integer vector v would be promoted to
      a real vector before the concatenation.

      Concatenation may also be used with scalar values. In this case
      the scalar values are treated as though they were single element
      vectors.

      ::

         								[1, 2, 3] || 4 // produces [1, 2, 3, 4]
         								1 || [2, 3, 4] // produces [1, 2, 3, 4]
         							

   c. Dot Product

      Two vectors with the same size and a numeric element type(types with
      the +, and \* operator) may be used in a dot product operation.
      For instance:

      ::

         								integer[3] v = [1, 2, 3];
         								integer[3] u = [4, 5, 6];

         								/* v[1] * u[1] + v[2] * u[2] + v[3] * u[3] */
         								/* 1 * 4 + 2 * 5 + 3 * 6 &=&  32 */
         								integer dot = v ** u;  /* Perform a dot product */
         							

   d. Indexing

      A vector may be indexed in order to retrieve the values stored in
      the vector. A vector may be indexed using integers, integer
      vectors, and integer intervals. *Gazprea* is 1-indexed, so the
      first element of a vector is at index 1 (as opposed to index 0 in
      languages like *C*). For instance:

      ::

         								intger vector v[3] = [4, 5, 6];

         								integer x = v[2]; /* x == 5 */
         								integer[*] y = v[2..3]; /* y == [5, 6] */
         								integer[*] z = v[[3, 1, 2]]; /* z == [6, 4, 5] */
         							

      When indexed with a scalar integer the result is a scalar value,
      but when indexed with an interval or a vector the result is
      another vector.

      Out of bounds indexing should cause an error.

   e. by

      The by operator is also defined for vectors of any element type. It
      produces a vector with every value with the given offset. For
      instance:

      ::

         								integer[*] v = 1..5 by 1; /* [1, 2, 3, 4, 5] */
         								integer[*] u = v by 1; /* [1, 2, 3, 4, 5] */
         								integer[*] w = v by 2; /* [1, 3, 5] */
         								integer[*] l = v by 3; /* [1, 4] */
         							

#. Operations of the Element Type

   Unary operations that are valid for the Element type of a vector may be
   applied to the vector in order to produce a vector whose result is
   the equivalent to applying that unary operation to each element of
   the vector. For instance:

   ::

      						boolean[*] v = [true, false, true, true];
      						boolean[*] nv = not v;
      					

   ``nv`` would have a value of
   ``[not true, not false, not true, not true] = [false, true, false, false]``.

   Similarly most binary operations that are valid to the element type of a
   vector may be also applied to two vectors. When applied to two
   vectors of the same size, the result of the binary operation is a
   vector formed by the element-wise application of the binary operation
   to the vector operands.

   ::

      						[1, 2, 3, 4] + [2, 2, 2, 2] // results in [3, 4, 5, 6]
      					

   Attempting to perform a binary operation between two vectors of
   different sizes should result in a type error.

   When one of the operands of a binary operation is a vector and the
   other operand this a scalar value, then the scalar value must first
   be promoted with a vector of the same size as the vector operand and
   with the value of each element equal the scalar value. For example:

   ::

      						[1, 2, 3, 4] + 2 // results in [3, 4, 5, 6]
      					

   Additionally the element types of vectors may be promoted, for instance
   in this case the integer vector must be promoted to a real vector in
   order to perform the operation:

   ::

      						[1, 2, 3, 4] + 2.3 // results in [3.3, 4.3, 5.3, 6.3]
      					

   The equality operation is the exception to the behavior of the binary
   operations. Instead of producing a boolean vector, an equality
   operation checks whether or not all of the elements of two vectors
   are equal, and return a single boolean value reflecting the result of
   this comparison.

   ::

      						[1, 2, 3] == [1, 2, 3]
      					

   yields ``true``

   ::

      						[1, 1, 3] == [1, 2, 3]
      					

   yields ``false``

   The != operation also produces a boolean instead of a boolean vector.
   The result is the logical negation of the result of the == operator.


Type Casting and Type Promotion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see the types that ``vector`` may be cast and/or promoted to, see
the sections on :ref:`sec:typeCasting` and :ref:`sec:typePromotion` 
respectively.
Vectors
-------

Vectors are language supported dynamically sized objects

-  Current vectors will be renamed to arrays (note vector is not a keyword)

-  New keyword Vector will be introduced

-  Vectors can only be created from literals:

   ::
        Vector<character> vec = ["a", "b", "c"];
        Vector<integer> ivec = [];
        Vector<real[*]> ragged_right = [[1.0], [2.0, 2.0]];

-  Gazprea supports some methods on Vector objects

   - push() - pushes a new element to the back
   - len() - number of elements in vector
   - to_c()
   - concat/append - add another vector
   - other operations? pop? sort? get?

- Operations on ``Vectors`` are identical syntactically and semantically to operations on arrays. In particular lengths must match.

- Vectors passed as arguments to functions are slices. This should also work for arrays

- Should we allow type inference for Vectors?       

   ::
        Vector<character> vec = ["a", "b", "c"];
        var cpy = vec;
        Vector vv;  // Is it better with or without the <>?
        vv.push(vec);
        vv.push(cpy);

Strings
-------

Gazprea ``string`` will be renamed to String and follow Vector rules/semantics

- Declaration does not need type because it is always character
      ::
        String str = "hello";
        String angular = "is this better?";

- Should we attempt to supprt unicode?

Structs
-------

Current tuple declaration:

::

     (integer, real, integer[10]) t1, t3;
     tuple(integer, real, integer[10]) t4 = ;
     var tuple(character mode, real, string[256] id, real) t4 = ("m", 1.0, "hello");
     typedef tuple(integer)  foo;

     
-  Should structs define a type?

::

     var integer foo;
     foo = 4;
     struct S (integer i, real r, integer[10] iv);
     struct T (integer i, real r, integer[10] iv) t3;
     struct stype (character mode, real float, String id);
     stype stype_var = ("c", 1.0, "id");
     stype alt_init = (mode = "c", id = "id", float = 0.0);

- can we require field names for structs and disallow field names for tuples?

- should structs use ``{}`` instead of ``()``?

- what is the difference between structs and tuples in Rust? I noticed that tuples and arrays are introduced together, but Objects and structs are introduced later.
  

        

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


      In this case ``numElements`` would be 3, since the vector ``v``
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


      would be permitted, and the integer vector ``v`` would be promoted to
      a real vector before the concatenation.

      Concatenation may also be used with scalar values. In this case
      the scalar values are treated as though they were single element
      vectors.

      ::

         [1, 2, 3] || 4 // produces [1, 2, 3, 4]
         1 || [2, 3, 4] // produces [1, 2, 3, 4]


      An interesting corollary to vector-scalar concatenation is that
      two scalars can be concatenated to produce a vector:

      ::

         integer[3] v = 1 || 2 || 3; // produces [1, 2, 3]


   c. Dot Product

      Two vectors with the same size and a numeric element type(types with
      the ``+``, and ``\*`` operator) may be used in a dot product operation.
      For instance:

      ::

         integer[3] v = [1, 2, 3];
         integer[3] u = [4, 5, 6];

         /* v[1] * u[1] + v[2] * u[2] + v[3] * u[3] */
         /* 1 * 4 + 2 * 5 + 3 * 6 &=&  32 */
         integer dot = v ** u;  /* Perform a dot product */


   d. Range

      The ``..`` operator creates an integer vector holding the specified range
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
      vector because the difference between them is negative.

   d. Indexing

      A vector may be indexed in order to retrieve the values stored in
      the vector. A vector may be indexed using integers.
      *Gazprea* is 1-indexed, so the first element of a vector is at index 1
      (as opposed to index 0 in languages like *C*). For instance:

      ::

         integer[3] v = [4, 5, 6];
         integer x = v[2]; /* x == 5 */
         integer y = [4,5,6][3] /* y == 6 */

      Out of bounds indexing should cause an error.

   e. Stride

      The ``by`` operator is used to specify a step-size greater than 1 when
      indexing across a vector. It produces a new vector with the values
      indexed by the given stride. For instance:

      ::

         integer[*] v = 1..5 by 1; /* [1, 2, 3, 4, 5] */
         integer[*] u = v by 1; /* [1, 2, 3, 4, 5] */
         integer[*] w = v by 2; /* [1, 3, 5] */
         integer[*] l = v by 3; /* [1, 4] */
         integer[*] s = v by 4; /* [1, 5] */
         integer[*] t = v by 5; /* [1] */

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
   different sizes should result in a ``SizeError``.

   When one of the operands of a binary operation is a vector and the
   other operand is a scalar, the scalar value must first
   be promoted to a vector of the same size as the vector operand and
   with the value of each element equal to the scalar value. For example:

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

   The ``!=`` operation also produces a boolean instead of a boolean vector.
   The result is the logical negation of the result of the ``==`` operator.


Type Casting and Type Promotion
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To see the types that a vector may be cast and/or promoted to, see
the sections on :ref:`sec:typeCasting` and :ref:`sec:typePromotion`
respectively.
=======
   

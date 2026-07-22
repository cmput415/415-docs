.. _ssec:vector:

Vectors
-------

Vectors are language supported objects that allow for dynamically sized arrays.
Once created, ``vectors`` in *Gazprea* interoperate freely with arrays: they
can be intermixed with arrays in expressions; they can be used on the RHS of
array declarations and initializations; and they can be passed as array
arguments to functions and procedures. Vectors are nevertheless a distinct
type, and the differences are normative: vectors have methods where arrays
have none, binary operations involving a vector produce *array* results,
and a vector of inferred-size arrays pads to the size of its *first*
element (see below), whereas a matrix literal pads to its longest row
(see :ref:`sssec:matrix_constr`).

.. _sssec:vec_decl:

Declaration
~~~~~~~~~~~

Vectors are declared and (optionally) initialized as follows.
(Note that we have replaced ``<>`` with ``|`` in the notation below since
the literals ``<`` and ``>`` are used in the declaration)

   ::

            [<qualifier>] vector<|type|> |identifier|;
            [<qualifier>] vector<|type|> |identifier| = |type-expr|;
            [<qualifier>] vector<|type|> |identifier| = |type-array|;


Unlike the array type, *Gazprea* vectors do not have an explicit size
specifier, often called *capacity* in other languages.

The element type ``T`` of a ``vector<T>`` may be any base type
(``boolean``, ``integer``, ``real``, ``character``) or a one-dimensional
array of a base type. Vectors of vectors, tuples, structs, strings, and
streams are not permitted. Below are some examples of
``vector`` declarations.
   
    ::

        const vector<integer[2]> v1 = 3;       // [[3, 3]]
        const vector<integer[2]> v2 = [4, 5];  // [[4, 5]]
        const vector<integer> v3 = 42;         // [42]
        var vector<integer> v4 = 42;           // [42], mutable
        vector<integer> v4 = 42;               // [42], implied const
        const vector<real> v5 = 1;             // [1.0]


Vectors of inferred sized arrays assume the size of the *first* array in the vector.
Subsequent array elements of less than the inferred size are padded.
Those greater raise a :term:`run time` ``SizeError``. (Contrast with
:ref:`matrix construction <sssec:matrix_constr>`, where rows pad to the
*longest* row: the same nested literal can be legal as a matrix and a
``SizeError`` as a vector of arrays.)

   ::

        const vector<character> vec = ['a', 'b', 'c'];
        const vector<real[*]> ragged_right = [[1.0], [2.0, 2.0]]; // SizeError
        const vector<real[*]> padded_right = [[1.0, 2.0], [1.0]]; // Pads second element
        const vector<character> const_vec = vec;


Operations
~~~~~~~~~~~

Operations on vectors are identical syntactically and semantically to
operations on arrays. In particular, operand lengths must match for binary
expressions and dot product. All binary operations between vector and arrays produce array results.

As a language supported object, *Gazprea* provides several methods for ``vector``:

- ``push(T)`` - pushes a new element to the back of the vector, where ``T`` is the element type of the vector

- ``len()`` - number of elements in the vector

- ``append(T[*])`` - append another array to the vector where ``T[*]`` is the type of the original vector or a type that can be implicitly cast to it.

   ::

        var vector<integer> v1;        // v1 == []
        v1.len() -> std_output;        // 0

        v1.push(1);                    // v1 == [1]
        v1.len() -> std_output;        // 1

        v1.push(2);                    // v1 == [1, 2]
        v1.len() -> std_output;        // 2

        v1.append([3, 4, 5])           // v1 == [1, 2, 3, 4, 5]
        v1.len() -> std_output;        // 5

        var vector<real[2]> v2;        // v2 == []
        const x = 1..10; 
        
        // `1` is promoted to `[1.0, 1.0]` before appending
        v2.append(1);                  // v2 == [[1.0, 1.0]]

        // length 1 array padded to length 2
        v2.append([3.0]);              // v2 == [[1.0, 1.0], [3.0, 0.0]]               
        
        // slices
        v2.append(x[5..7]);            // v2 == [[1.0, 1.0], [3.0, 0.0], [5.0, 6.0]]

        v2.len() -> std_output         // 3

        v2.len();                      // Does nothing

        (v1 + v2).push(3);             // Effectively does nothing, reference to the sum is dropped after the statement

Slicing a vector produces an array slice (there are no "vector slices").

   ::

        // Slicing a vector produces an array slice
        vec[2..5].append(x[5..7])      // TypeError; cannot do `append` on an array slice

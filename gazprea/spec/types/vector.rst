.. _ssec:vector:

Vectors
-------

Vectors are language supported objects that allow for dynamically sized arrays.
Once created, ``vectors`` in *Gazprea* behave exactly like arrays: they can be
intermixed with arrays in expressions; they can be used on the RHS of array
declarations and initializations; and they can be passed as array arguments to
subroutines and functions.

.. _sssec:vec_decl:

Declaration
~~~~~~~~~~~

Vectors are declared and (optionally) initialized as follows.
(Note that we have replaced ``<>`` with ``|`` in the notation below since
the literals ``<`` and ``>`` are used in the declaration)

   ::

            vector<|type|> |identifier|;
            vector<|type|> |identifier| = |type-expr|;
            vector<|type|> |identifier| = |type-array|;


Unlike the array type, *Gazprea* vectors do not have an explicit size
specifier, often called *capacity* in other languages. Below are some examples of 
`vector` declarations.
   
    ::

        const vector<integer[2]> v1 = 3;       // [[3, 3]]
        const vector<integer[2]> v2 = [4, 5];  // [[4, 5]]
        const vector<integer> v3 = 42;         // [42]
        const vector<real> v4 = 1;             // [1.0]


Vectors of inferred sized arrays assume the size of the *first* array in the vector.
Subsequent array elements of less than the inferred size are padded.
Those greater raise a runtime ``SizeError``.

   ::

        const vector<character> vec = ['a', 'b', 'c'];
        const vector<real[*]> ragged_right = [[1.0], [2.0, 2.0]]; // SizeError
        const vector<real[*]> padded_right = [[1.0, 2.0], [1.0]]; // Pads second element
        const vector<character> const_vec = vec;


Operations
~~~~~~~~~~~

Operations on vectors are identical syntactically and semantically to
operations on arrays. In particular, operand lengths must match for binary
expressions and dot product.

Slicing a vector produces an array slice (there are no "vector slices").

   ::

        // Slicing a vector produces an array slice
        vec[2..5].append(x[5..7])      // TypeError; vec[2..5] is an array slice

As a language supported object, *Gazprea* provides several methods for ``vector``:

- ``push()`` - pushes a new element to the back of the vector

- ``len()`` - number of elements in the vector

- ``append(T[*])`` - append another array to the vector where `T` is the type of the original vector or a type that can be implicitly cast to it. The following example tracks the elements inside `vec` through various appends.

   ::

        const x = 1..10; 
        var vector<real[2]> vec;       // []
        
        // scalar to array promotion
        vec.append(1);                 // [[1.0, 1.0]]

        // array padding
        vec.append(3..3);              // [[1.0, 1.0], [3.0, 0.0]]               
        
        // slices
        vec.append(x[5..7]);           // [[1.0, 1.0], [3.0, 0.0], [5.0, 6.0]]

        vec[tvec.len()] -> std_output; // prints 3



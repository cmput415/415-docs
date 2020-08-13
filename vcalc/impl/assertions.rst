Assertions
==========

**ALL** input test cases will be valid. It can be a good idea to do
error checking for your own testing and debugging, but it is *not
necessary*. If you encounter what you think is undefined behaviour or
think something is ambiguous then *do* make a forum post about it to
clarify.

What does it mean to be valid input? The input must adhere to the
specification. The rules below give more in-depth explanation of
specification particulars.

#. 

   .. _assert:vector-length:

   .. container::
      :name: vector-length

      **vector-length**:

   All vectors will have length :math:`l` such that
   :math:`0 \leq l \leq 2^{32}`. Trying to create an index greater than
   :math:`2^{32} - 1` will cause overflow and result in a negative
   number. Indexing with a negative number returns :math:`0`. Therefore,
   vector locations greater than :math:`2^{32} - 1` would be
   inaccessible. For example, the following tests would be considered
   invalid:

   ::

            print((0-1)..2147483647);

   But the following test is valid because the vector length is still
   within range:

   ::

            print((0-2)..2147483645);


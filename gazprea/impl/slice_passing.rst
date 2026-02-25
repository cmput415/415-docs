.. _sec:impl_slice_passing:

Slice Passing — Eager Copy vs. Copy-On-Write
============================================

The *Gazprea* specification defines slice expressions as rvalues that produce a
**deep copy** of the selected elements (see :ref:`sssec:array_ops`). This is a
*semantic* guarantee: from the programmer's perspective, a slice always behaves
as an independent value with no aliasing relationship to the source array.

However, the specification does **not** require an *eager* copy to be made at
the point of the slice expression. An implementation is free to use a lazy
strategy such as **Copy-On-Write (COW)**.

Copy-On-Write Strategy
----------------------

Under COW, passing a slice to a function or procedure does not immediately
duplicate the underlying storage. Instead, the implementation shares the same
backing memory and only performs the physical copy when — and if — either the
source array or the slice view is mutated. If no mutation occurs, the copy is
avoided entirely.

This is safe because:

1. Slices can only be passed as ``const`` (by-value) parameters. A callee that
   receives a slice argument cannot mutate it through that parameter.
2. The source array variable is not accessible from inside the called
   function/procedure (functions are pure; procedures have no aliasing with
   ``const`` parameters).

Therefore, a COW implementation is observationally equivalent to an eager deep
copy for all legal *Gazprea* programs.

Example
-------

::

    function sum(integer[*] v) returns integer { ... }

    procedure main() returns integer {
        var integer[10] a = 1..10;

        // The slice a[2..6] is an rvalue. An eager-copy implementation
        // allocates a new 4-element array here.  A COW implementation may
        // instead pass a lightweight view into a's storage, deferring the
        // copy until (if ever) a mutation would make it necessary.
        integer total = sum(a[2..6]);
        return total;
    }

Implementation Note
-------------------

Choosing an eager-copy or COW strategy is an internal quality-of-implementation
decision and does not affect language semantics. Implementations that wish to
avoid the overhead of copying large slices are encouraged to consider COW or
similar lazy strategies.

.. _ssec:ext_borrow_checking:

Ownership and Borrowing System
==============================

One of the most powerful but complex extensions would be to replace *Gazprea*'s
default "deep copy" memory model with an ownership and borrowing system, similar
to the one pioneered by the Rust programming language.

**High-Level Goal**
-------------------

The goal of this system is to guarantee memory safety (no dangling pointers, no
data races) at compile time **without** requiring a garbage collector. This would
allow for highly performant code with C-like speed while providing strong safety
guarantees. It would enable powerful features like zero-cost mutable "views"
into arrays, solving the problem discussed in the main specification.

A new keyword, such as ``ref``, could be introduced to create borrowed
references to data.

::

    // Hypothetical Gazprea with borrowing
    procedure sort_portion(ref arr: integer[*]) {
        // ... sort the slice in-place ...
    }

    var my_data: integer[100] = ...;
    call sort_portion(ref my_data[10..20]); // Pass a mutable view

Major Architectural Changes Required
------------------------------------

Implementing a borrow checker is not a small feature; it is a fundamental change
to the entire compiler architecture. It would require:

1.  **A Lifetime-Aware Type System:** The type checker would need to be
    fundamentally altered to understand lifetimes. A type like ``ref integer``
    is incomplete; the full type is ``ref<'a> integer``, where ``'a`` is a
    lifetime parameter that the compiler must track and validate. This involves
    complex inference and subtyping rules.

2.  **Control-Flow-Sensitive Static Analysis:** The compiler would need a new,
    major analysis pass that runs after initial type checking. This pass must:
    a. Build a Control-Flow Graph (CFG) for every function.
    b. Track the state of every variable (owned, immutably borrowed, mutably
       borrowed, or moved) along every possible execution path.
    c. This analysis, often called "borrow checking," is a non-trivial data-flow
       analysis problem.

3.  **Sophisticated Error Reporting:** The compiler must be able to generate
    human-understandable error messages for complex borrow-checking failures,
    such as "cannot borrow `x` as mutable because it is also borrowed as
    immutable in function `f`."

Documentation and Further Reading
---------------------------------

**Community and Engineering Focused:**

*   **The Rust Programming Language (Book):** The official book provides the most
    accessible introduction to the concepts of ownership, borrowing, and
    lifetimes. Chapters 4, 10, and 15 are particularly relevant.
    *   *Link:* `https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html <https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html>`_
*   **Rustonomicon:** For a deep dive into the memory model and the unsafe code
    that a borrow checker allows you to avoid.
    *   *Link:* `https://doc.rust-lang.org/nomicon/ <https://doc.rust-lang.org/nomicon/>`_
*   **Niko Matsakis's Blog:** A series of blog posts from a lead Rust developer
    detailing the implementation and evolution of the borrow checker. Essential
    for understanding the practical engineering challenges.
    *   *Link:* `https://smallcultfollowing.com/babysteps/ <https://smallcultfollowing.com/babysteps/>`_

**Academic and Theory Focused:**

*   **"Region-based memory management"** and **"Affine types"** are the core
    computer science concepts behind borrow checking. Academic papers on these
    topics provide the theoretical foundation.
*   **RustBelt: Securing the Foundations of the Rust Programming Language (PLDI 2018):**
    A key academic paper that formally models and proves the safety of Rust's
    type system.
    *   *Link:* `https://dl.acm.org/doi/10.1145/3296979.3192384 <https://dl.acm.org/doi/10.1145/3296979.3192384>`_

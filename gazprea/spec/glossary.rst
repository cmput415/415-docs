.. _sec:glossary:

Glossary
========

This page collects the technical terminology used throughout the *Gazprea*
specification.  Its purpose is threefold: to fix the meaning of the words we
use so that the specification is self-consistent, to point the reader at the
authoritative literature behind each term, and to give students a
jumping-off point when they need or want to specify a language or compiler task
of their own.

Most entries below have a **primary citation** to an authoritative source:
an ISO/IEC or IEEE standard, the documentation of an ongoing industrial
open-source project (LLVM, GCC, GNU Binutils), or a peer-reviewed
publication in a respected venue.  The *Gazprea*-specific normative entries
(for example :term:`zero value` and :term:`value type`) instead cite the
specification chapter that states the rule in full.
Where a term has a widely-used *effective*
reference (e.g. cppreference for the C++ value categories), that reference
appears alongside the authoritative citation and is explicitly labeled as
non-normative.

.. note::

   Most entries here are *definitions of terminology*.  Where *Gazprea*
   re-uses a word from another language (for instance ``type qualifier``,
   which C reserves for ``const``/``volatile``/``restrict``/``_Atomic`` but
   *Gazprea* uses for the mutability distinction ``const``/``var``), the
   glossary explains the source of the word and points to the *Gazprea*
   chapter that gives its language-specific meaning.

   A few entries, however, *do* state normative *Gazprea* rules -- notably
   :term:`zero value`, :term:`initialization`, :term:`re-initialization`,
   :term:`domain`, and :term:`value type`.  These definitions are
   normative wherever it appears, and each is cross-referenced to
   the chapter that states it in full.

.. contents:: On this page
   :local:
   :depth: 2

.. _ssec:glossary_terms:

Terms
-----

.. glossary::
   :sorted:

   initialization
      The :term:`run time` instant at which a variable's declaration first
      executes.  A declaration is surrounded by two *program points* such that
      any control path reaching the first point (preceding the declaration)
      *must* pass through the second point [#dragon]_;
      at run time
      control reaches the point preceding the declaration
      along some *control-flow path*, and may reach
      it more than once. For example, a declaration in a loop body,
      or one on a branch of
      a conditional, is reached once per time control flows through it.

      A
      variable is *initialized* on the first transit of control through the path
      between the two points enclosing the declaration.
      Each subsequent execution of the same
      declaration begins a fresh :term:`lifetime` rather than mutating the
      previous one (see :term:`re-initialization`).

      A variable's array and
      matrix dimensions are settled *exactly once*, at initialization, and are
      then fixed for the remainder of that variable's lifetime: an array is
      sized once and can never be resized.  A size may be any integer
      expression. It need not be a :term:`compile time` constant, but it is
      evaluated a single time, at the first execution of the declaration,
      and later changes to that
      expression's inputs do not affect the array. (Ada draws a similar
      once-only distinction termed *elaboration*; *Gazprea*
      keeps a single definition of a variable's size and calls the instant it
      happens *initialization*.)

   zero value
      The value a variable of a given type holds when it is declared
      without an :term:`initializer`.  It is ``0`` for ``integer``,
      ``0.0`` for ``real``, ``false`` for ``boolean``, and ``'\0'`` (the
      null character) for ``character``.  For a fixed-size array or
      matrix it is that shape filled with the element type's zero value;
      for a ``tuple`` or ``struct``, each member set to its own zero
      value; for a ``vector`` or ``string``, the empty collection.  A
      ``const`` variable declared without an initializer keeps its zero
      value for its entire lifetime; a shorter array value stored into a
      longer array is padded with the element type's zero value.  This rule
      is stated normatively, in the context of *Gazprea*'s RAII-style
      initialization, in :ref:`sec:declaration`.

   aggregate type
      A type composed of subordinate members of possibly-different types.
      In ISO C the term denotes array and structure types collectively
      [#iso-c11]_.  In *Gazprea* the aggregate types are arrays, matrices,
      vectors, tuples, and structs; see :ref:`sec:types`.

      *Terminology note.*  Ada calls this umbrella category *composite
      type* rather than *aggregate type* [#ada-rm]_.  ISO C
      also defines *composite type* but with an unrelated meaning:
      the merged type produced from two compatible declarations of
      the same entity, not a category of types [#iso-c11]_.  Because
      "composite" is a false friend between the two standards, *Gazprea*
      follows the C/C++ convention and uses *aggregate type* as the
      umbrella term.

   assembler
      A program that translates assembly language into relocatable
      machine code [#dragon]_.  In the LLVM toolchain the assembler role
      is played by the MC layer and the ``llvm-mc`` driver [#llvm-mc]_.

   compile time
      The interval during which the source program is being translated
      by the :term:`compiler`, before program execution begins.  The
      contrast with :term:`run time` matters for sizing in *Gazprea*: an
      array's size need not be fixed at compile time, only at
      :term:`initialization`, which is a run-time instant.  The C
      standard specifies the phases of translation in ISO/IEC 9899
      §5.1.1.2 [#iso-c11]_.

   compiler
      A program that reads a source program in one language and
      produces an equivalent program in a target language [#dragon]_.
      GCC and LLVM/Clang are two production compilers whose internal
      architectures follow the classical front-end / middle-end /
      back-end division [#gcc-int]_ [#llvm-langref]_.

      *Compiler subtypes.*  The default definition of a compiler is one thats
      target is machine code executable by a CPU.
      Two marked variants are
      recognized:

      *  A :term:`source-to-source translator` compiles from one
         high-level language to another high-level language [#dragon]_.
         The informal term *transpiler* is sometimes used for the same
         concept. The first attempt at a
         peer-reviewed generic definition appears in a 2023 mapping
         review [#meza-transpilers-2023]_.  Prefer *source-to-source
         translator*.
      *  A :term:`cross-compiler` runs on one host platform and emits
         code for a different target platform (CPU or operating system)
         [#clang-cross]_ [#gcc-cross]_.  Cross-compilation is
         orthogonal to whether the target language is machine code or
         another high-level language.

   cross-compiler
      A :term:`compiler` that runs on one host platform (CPU + operating
      system) and produces code for a different target platform.  Clang
      is designed as a native cross-compiler in which one binary can
      target every supported architecture via a ``-target`` flag
      [#clang-cross]_; GCC by contrast requires a separately-built
      host/target binary pair [#gcc-cross]_.

   source-to-source translator
      A :term:`compiler` that translates from one high-level language
      into another high-level language rather than into machine code
      [#dragon]_.  The informal industry term *transpiler* denotes the
      same concept; see the note in :term:`compiler`.

   constant expression
      An expression that a conforming implementation is required to be
      able to evaluate during translation.  In C++, "expressions that
      satisfy these requirements ... are called constant expressions"
      [#cpp-draft]_.  See :ref:`sec:constexpr` for *Gazprea*'s
      specific rules; note that in *Gazprea* the noun is often
      abbreviated ``constexpr``, which is *not* a keyword.

   declaration
      A construct that specifies the interpretation and attributes of a
      set of identifiers [#iso-c11]_.  A declaration in *Gazprea* has
      the form defined in :ref:`sec:declaration`.

   definition
      A declaration that additionally causes storage to be reserved for
      an object, or that supplies the body of a function or procedure
      [#iso-c11]_.  The C++ grammar production and definitional
      requirements are given in [basic.def] [#cpp-draft]_; *Gazprea*
      does not adopt C++'s one-definition rule, so the citation is
      informational only.

   dynamic
      Determined or known at :term:`run time`.  Used as the antonym of
      :term:`static`.  ISO/IEC 9899 §6.2.4 uses "dynamic" implicitly by
      contrasting *static* storage duration with *automatic* and
      *allocated* storage durations whose extents are established during
      execution [#iso-c11]_.

   expression
      "A sequence of operators and operands that specifies a
      computation.  An expression can result in a value and can cause
      side effects" [#cpp-draft]_.  The syntactic shape of
      expressions in *Gazprea* is defined in :ref:`sec:expressions`.
      Note that in gazprea an expression is functionally pure.

   domain
      In a *Gazprea* :ref:`iterator loop <sssec:statements_iter_loop>`
      or :term:`domain expression`, the array-typed operand to the
      right of ``in``.  The domain is evaluated exactly once, at
      :term:`initialization`; the resulting value is captured
      for the lifetime of the loop, and subsequent modifications to
      any variable that appeared in the domain expression do not
      affect the domain variable.
      In general PL usage the analogous notion is the
      *range* of a range-based loop (C++ ``for (x : R)``
      [#cpp-draft]_), archaically called the *iteration scheme* of an Ada
      ``for`` loop [#ada-rm]_.

   domain expression
      The whole *Gazprea* construct ``x in E`` used inside an
      :ref:`iterator loop <sssec:statements_iter_loop>` or generator:
      the :term:`iterator variable` ``x`` bound over the :term:`domain`
      ``E``.  Domain expressions can only appear inside iterator loops
      and generators.

   iterator
      A cursor that yields the elements of a collection one at a time,
      in a defined order.  The concept is standard across modern
      language families: Python defines it operationally through the
      iterator protocol (``__iter__`` / ``__next__``) [#pep-234]_;
      C++ defines *iterators* as generalized pointers into a range,
      with the requirements collected in [iterator.requirements]
      [#cpp-draft]_.  In *Gazprea* the word is used
      informally for the mechanism that a
      :ref:`iterator loop <sssec:statements_iter_loop>` uses to walk
      its :term:`domain`; the visible binding is the
      :term:`iterator variable`.

   iterator variable
      In a *Gazprea* :ref:`iterator loop <sssec:statements_iter_loop>`
      or :term:`domain expression`, the identifier to the left of
      ``in``.  A fresh binding is introduced at the start of every
      iteration (see :term:`re-initialization`) and destroyed at the
      end of that iteration.  In other languages the equivalent
      binding is Ada's *loop parameter* [#ada-rm]_ and C++'s
      *for-range-declaration* [#cpp-draft]_.

   re-declaration
      A second (or nth) :term:`declaration` of the same
      :term:`identifier` within a given :term:`scope`.  In *Gazprea*
      a re-declaration always introduces a fresh binding that
      *shadows* the enclosing binding for the remainder of the scope;
      it does not modify the original.  The general PL concept is
      *scope shadowing* [#pierce-tapl]_.

      Re-declarations arise in every scope, not only iterator loops.
      The specific case where a re-declaration inside an
      :ref:`iterator loop <sssec:statements_iter_loop>` body shadows
      the :term:`iterator variable` is called out under
      :term:`re-initialization`: the shadow lives for one iteration
      only, and the next iteration re-initializes the iterator
      variable normally.

   re-initialization
      In a *Gazprea*
      :ref:`iterator loop <sssec:statements_iter_loop>`, the binding,
      performed at the start of every iteration, of the
      :term:`iterator variable` to the next element of the captured
      :term:`domain`.  Because re-initialization introduces a fresh
      binding from the captured domain, neither reassignment of the
      loop domain expression nor mutation of the iterator variable
      inside the body carries information into the next iteration.

   functional purity
      An informal property of a language, expression, or function: the
      absence of observable :term:`side effects <side effect>`.  There
      is no ISO definition; the standard academic reference is
      Strachey's characterization of :term:`referential transparency`
      [#strachey-2000]_.  *Gazprea* invokes functional purity as the
      motivation for forbidding mutable :ref:`globals <sec:global>` and
      for the input-only nature of function arguments.

      Once again, consult with a Haskell programmer.

   glvalue
      A "generalized" lvalue: "an expression whose evaluation
      determines the identity of an object, function, non-static data
      member, or a direct base class relationship" [#cpp-draft]_.
      One of the three C++11 :term:`value categories <value category>`
      (together with :term:`prvalue` and :term:`xvalue`).  See the
      non-normative summary at [#cppref-value-cat]_ for an accessible
      introduction. Note that gazprea does not contain glvalues, this is
      for extended reading.

   identifier
      "A sequence of nondigit characters ... and digits, which
      designates one or more entities" [#iso-c11]_.  *Gazprea*'s lexical
      rules for identifiers are in :ref:`sec:identifiers`.

   ill-formed
      A program is *ill-formed* if it is not :term:`well-formed`
      [#cpp-defns]_.  A conforming implementation is required to
      issue a diagnostic for at least one violation of a diagnosable
      rule in an ill-formed program.

   implementation-defined behavior
      "Unspecified behavior where each implementation documents how the
      choice is made" [#iso-c11]_.  Distinct from
      :term:`unspecified behavior` (no documentation obligation) and
      :term:`undefined behavior` (no requirements at all).

      *Gazprea policy.*  A conforming *Gazprea* implementation must
      not have any user-distinguishable implementation-defined
      behavior or unspecified behavior, and has **no undefined
      behavior** at all.  Every program is either :term:`well-formed`
      and produces the output required by this specification, or it is
      :term:`ill-formed` and the implementation emits an error.

   implicit cast
      A conversion the compiler performs automatically, with no syntax
      in the program text.  In *Gazprea*, "cast" is the umbrella term
      for both implicit casts and the *explicit casts* written
      ``as<toType>(value)``; an implicit cast is simply the automatic
      counterpart (e.g. ``integer`` -> ``real`` when arithmetic mixes
      them).  The mechanism is specified in
      :ref:`sec:implicitCasts`.  Most implicit casts can also be written
      explicitly as an ``as<>`` cast; a scalar-to-array explicit cast must
      then state the destination size (see :ref:`ssec:typeCasting_stovm`).

   explicit cast
      A conversion the programmer writes out explicitly in the program
      text with the ``as<toType>(value)`` syntax, as opposed to an
      :term:`implicit cast`, which the compiler inserts automatically.
      Both are *casts*; the explicit form is specified in
      :ref:`sec:typeCasting`.

   value type
      A type whose values are stored inline, by value, rather than
      through indirection.  In *Gazprea* every :term:`aggregate type`
      except ``vector`` behaves as though it is a value type. Due to value-type
      behaviour requiring a value to be
      :term:`materializable <materialization>`,
      nesting of aggregate type definitions must be acyclic through
      value types, so a ``struct`` or ``tuple`` may refer to its own type
      only through a ``vector`` (see :ref:`ssec:storable_types`).

    materialization
      "Materialization is the blanket term for any actions that are required
      [...] to generate a symbol definition that is safe to call or access."
      [#llvm-orcjit]_ .

   implicit conversion
      An automatic conversion inserted by the language, without a cast,
      to make an operand's type match a required target type.  ISO C
      collects the rules under §6.3 "Conversions" [#iso-c11]_.

      *Gazprea* uses this general term only in the glossary.  In the
      *Gazprea* specification proper the analogous mechanism is called
      an :term:`implicit cast`, described in
      :ref:`sec:implicitCasts`.

   initializer
      The syntactic element that supplies an initial value to a newly
      declared object.  In C++ the grammar is given in
      ``[dcl.init.general]`` [#cpp-draft]_.  *Gazprea*'s
      initializer positions and rules are covered in
      :ref:`sec:declaration`.

   interpreter
      A program that does not produce a target program, but "appears to
      directly execute the operations specified in the source program on
      inputs supplied by the user" [#dragon]_.  Contrast with
      :term:`compiler` and :term:`translator`.

   lifetime
      "The portion of program execution during which storage is
      guaranteed to be reserved" for an :term:`object`.  "An object
      exists, has a constant address, and retains its last-stored value
      throughout its lifetime" [#iso-c11]_.

      Rust makes *lifetime* a first-class object of the type system
      such that every reference carries a compile-time lifetime parameter
      that the borrow-checker uses to prove memory safety without a
      garbage collector.  The Rust Reference chapter on lifetimes
      [#rust-ref-lifetimes]_ and the Rustonomicon chapter on
      references [#rustonomicon-lifetimes]_ together give the most
      operationally-precise treatment of the concept in a
      production language.

   linker
      A program that combines separately-translated
      :term:`translation units <translation unit>` into a single
      executable, resolving external references between them.  The GNU
      ``ld`` documentation gives the canonical operational description
      [#binutils-ld]_.  See also :term:`link time`.

   link time
      The interval during which the :term:`linker` runs, after
      :term:`translation` of each translation unit and before program
      execution.  ISO C describes this as translation phase 8
      [#iso-c11]_.  Link-time optimization (LTO), performed at this
      point, is documented for the LLVM toolchain in [#llvm-lto]_.

   literal
      A token whose value is the token itself: integer, floating-point,
      character, string, boolean, and (in C++) pointer literals
      [#cpp-draft]_.  Contrast a literal with a
      :term:`constant expression`, which may be composed of literals
      and other operators.

   lvalue
      "An expression (with an object type other than void) that
      potentially designates an object" [#iso-c11]_.  C++ defines an
      lvalue as "a :term:`glvalue` that is not an :term:`xvalue`"
      [#cpp-draft]_.  The historical origin of the "l-value" and
      "r-value" terminology is Strachey's 1967 lectures, published as
      [#strachey-2000]_.  See the non-normative summary
      [#cppref-value-cat]_ for a modern taxonomy.

   name binding
      The association of an :term:`identifier` with an entity (an
      object, function, type, etc.) within a scope.  ISO C uses the
      operational phrase "the declaration ... is visible at the point
      the identifier occurs" [#iso-c11]_ rather than the term "binding".
      The academic origin of "binding" as the association of names with
      denotable values in an environment is Strachey
      [#strachey-2000]_.

   object
      "A region of data storage in the execution environment, the
      contents of which can represent values" [#iso-c11]_.  In this
      glossary the word always refers to the *run-time* storage-region
      entity, in the ISO C sense.

      *Gazprea note.*  *Gazprea* is not an object-oriented language.
      It has no user-defined classes, no inheritance, and no virtual
      dispatch.  *Gazprea* uses object oriented terminology to describe
      :term:`aggregates <aggregate type>`, particularly the
      :ref:`vector <ssec:vector>` type, which exposes methods
      (``push``, ``len``, ``append``) via dot syntax.  Those are
      built-in operations on the vector's storage-region object, not
      a user-facing object-model feature; when a *Gazprea* sentence
      says "object" it always means the storage region, never a
      vector-as-instance-of-a-class.

   primitive type
      A type provided directly by the language and not composed of
      other types.  The LLVM Language Reference distinguishes
      *primitive* types (``i32``, floating-point types, ``void``, etc.)
      from *derived* and *aggregate* types [#llvm-langref]_.  In
      *Gazprea* the primitive types are ``boolean``, ``integer``,
      ``real``, and ``character``.  See also :term:`scalar type`,
      ISO C's term for the same four *Gazprea* types.

   prvalue
      A "pure r-value": "an expression whose evaluation initializes an
      object or computes the value of an operand of an operator ... or
      an expression that has type cv void" [#cpp-draft]_.  One of
      the three C++11 :term:`value categories <value category>`.  See
      the non-normative summary at [#cppref-value-cat]_ for an
      accessible introduction.

   pure function
      See :term:`functional purity`.

   referential transparency
      The property that an expression's value depends only on the
      values of its subexpressions, so that any subexpression may be
      replaced by an equal-valued subexpression without changing the
      whole [#strachey-2000]_.  The term is due to Quine
      [#quine-1960]_.

      *Gazprea* guarantees referential transparency only for
      :term:`pure functions <functional purity>` (see
      :ref:`sec:function`) and for :term:`expressions <expression>`
      built exclusively out of them.  It is *not* guaranteed for
      :ref:`procedures <sec:procedure>`, which may have
      :term:`side effects <side effect>` and whose return value can
      therefore change between calls with the same arguments; nor for
      any expression that transitively depends on a procedure call.
      This is why *Gazprea* forbids calling procedures inside
      functions (aside from a mutating ``vector``/``string`` method such as
      ``push``/``append`` on a function-local variable; see
      :ref:`sec:function`), forbids mutable globals, and restricts the operators
      that may combine a procedure call's return value (see
      :ref:`sec:procedure`).

   run time
      The interval during which the program is executing, after
      :term:`translation` and :term:`link time` are complete.  Ada
      defines the corresponding process, *execution*, as "the process
      by which a construct achieves its run-time effect"
      [#ada-rm]_.

   rvalue
      C++ defines an rvalue as "a :term:`prvalue` or an :term:`xvalue`"
      [#cpp-draft]_.  In C the term is used informally as the
      complement of :term:`lvalue`.  Historical origin: Strachey
      [#strachey-2000]_.  See the non-normative summary at
      [#cppref-value-cat]_ for the modern C++ taxonomy.

   scalar type
      A type whose values are atomic in the sense that they are not
      composed of sub-elements.  ISO C: "Arithmetic types and pointer
      types are collectively called scalar types" [#iso-c11]_.  Ada
      groups enumeration, integer, and real types as scalar
      [#ada-rm]_.  In *Gazprea* the scalar types are ``boolean``,
      ``integer``, ``real``, and ``character``.  See also
      :term:`primitive type`, the LLVM-derived term for the same four
      *Gazprea* types.

   scope
      "The region of program text within which [an] identifier is
      visible" [#iso-c11]_.  ISO C distinguishes four kinds of scope:
      function, file, block, and function prototype.  *Gazprea*'s scope
      rules are described in :ref:`sec:declaration` and
      :ref:`sec:namespaces`.

   sequenced before
      "An asymmetric, transitive, pair-wise relation between
      evaluations executed by a single thread ...  if A is sequenced
      before B (or, equivalently, B is sequenced after A), then the
      execution of A shall precede the execution of B"
      [#cpp-draft]_.  The relation supplants the older ISO C
      *sequence point* model for describing the ordering of
      :term:`side effects <side effect>`.

   side effect
      "Reading an object designated by a volatile glvalue, modifying an
      object, ... calling a library I/O function, or calling a function
      that does any of those operations" -- any "change in the state of
      the execution or translation environment" [#cpp-draft]_.
      ISO C gives an equivalent enumeration [#iso-c11]_.

   statement
      A syntactic construct whose primary role is to be executed for
      its effect rather than to compute a value.  The C++ grammar
      enumerates the kinds of statement in ``[stmt.pre]``
      [#cpp-draft]_.  *Gazprea*'s statements are covered in
      :ref:`sec:statements`.

   static
      Determined or known at :term:`compile time`.  Ada gives a nice
      definition: "Static means determinable at compile
      time, using the declared properties or values of the program
      entities" [#ada-rm]_.  Contrast with :term:`dynamic`.

   storage duration
      The property of an :term:`object` that determines its
      :term:`lifetime`.  ISO C defines four storage durations: static,
      thread, automatic, and allocated [#iso-c11]_.

   translation
      The act of processing a source program to produce a target
      program.  ISO C notes that "translation units may be separately
      translated and then later linked to produce an executable
      program" [#iso-c11]_.  Distinct from :term:`compile time`, which
      refers to *when* translation happens.

   translation unit
      "The unit of program text after preprocessing ... consist[ing] of
      a sequence of external declarations" [#iso-c11]_.  In *Gazprea*
      each ``.gaz`` source file corresponds to one translation unit.

   translator
      A generic term for a program that reads a source program and
      writes an equivalent program in a different language; a
      :term:`compiler`, :term:`assembler`, and source-to-source
      converter are all translators [#dragon]_.

   type
      A characterization of a set of values together with a set of
      operations on those values [#ada-rm]_ [#pierce-tapl]_.
      *Gazprea*'s types are enumerated in :ref:`sec:types`.

   type casting
      Explicit conversion of a value from one type to another, invoked
      by an explicit syntactic form.  ISO C's cast operator is defined
      in §6.5.4 [#iso-c11]_.  *Gazprea*'s casting rules are covered in
      :ref:`sec:typeCasting`.

   type inference
      The compile-time reconstruction of a type that has been omitted
      from a program.  Milner's polymorphic type inference (algorithm
      W), and the accompanying soundness result, is the foundational
      academic reference [#milner-1978]_.  *Gazprea*'s type inference
      is described in :ref:`sec:typeInference`.

   type qualifier
      In ISO C the term refers to the *cv*-qualifiers ``const``,
      ``restrict``, ``volatile``, and ``_Atomic``, defined in §6.7.3
      [#iso-c11]_.  *Gazprea* re-uses the phrase for the mutability
      qualifiers ``const`` and ``var`` (see :ref:`sec:typeQualifiers`).

   type system
      A tractable syntactic method for classifying phrases of a
      language by the kinds of values they compute
      [#pierce-tapl]_.  Type systems are traditionally divided into
      *static* systems (checking performed before execution) and
      *dynamic* systems (checking performed during execution); see
      Pierce, Chapter 1 [#pierce-tapl]_.

      *Further reading (for the curious student).*  The deep
      connection between type systems and formal logic is the *Curry-Howard
      correspondence*.  Wadler's ACM lecture "Propositions as Types"
      [#wadler-2015]_ is a short, entry-level survey; Sørensen and
      Urzyczyn's book-length *Lectures on the Curry-Howard
      Isomorphism* [#sorensen-urzyczyn-2006]_ is the standard
      textbook.  These are not required reading for *Gazprea*, but
      students designing their own type systems in future courses may
      encounter them.

   undefined behavior
      "Behavior ... for which this document imposes no requirements"
      [#iso-c11]_.  A program exhibiting undefined behavior at run time
      is not obliged to signal an error, terminate, or produce any
      particular output.  Contrast :term:`unspecified behavior` and
      :term:`implementation-defined behavior`.  *Gazprea* has no
      undefined behavior at all: every program is either
      :term:`well-formed` and produces the specified output, or it is
      :term:`ill-formed` and the implementation emits an error.

   unspecified behavior
      "Use of an unspecified value, or other behavior where this
      document provides two or more possibilities and imposes no
      further requirements on which is chosen in any instance"
      [#iso-c11]_. *Gazprea* should not have _any_ unspecified behaviour.
      If you find any unspecified behaviour, please open an issue on the public
      github, as this is a specification error.

   value category
      "Every expression belongs to exactly one of the fundamental
      categories in [the C++] taxonomy: lvalue, xvalue, or prvalue.
      This property of an expression is called its value category"
      [#cpp-draft]_.  A non-normative overview lives at
      [#cppref-value-cat]_.

   well-formed
      "C++ program constructed according to the syntax rules,
      diagnosable semantic rules, and the one-definition rule"
      [#cpp-defns]_.  *Gazprea* uses "well-formed" throughout in
      this generalized sense: a *Gazprea* program is well-formed if it
      satisfies every diagnosable rule stated in this specification.

   xvalue
      An "expiring" value: "a :term:`glvalue` that denotes an object
      whose resources can be reused (usually because it is near the end
      of its lifetime)" [#cpp-draft]_.  One of the three C++11
      :term:`value categories <value category>`.  See the non-normative
      summary at [#cppref-value-cat]_ for an accessible introduction.


.. _ssec:glossary_authoritative:

Authoritative sources
---------------------

The primary citations for the entries above are listed here.

.. rubric:: Standards

.. [#ada-rm] ISO/IEC 8652:2012, *Information technology -- Programming
   languages -- Ada* (the Ada 2012 Reference Manual).  Ada-Auth
   reference manual mirror, one page per clause under
   http://www.ada-auth.org/standards/12rm/html/.  Year: 2012.  Clauses
   cited from this glossary and where each is used:

   *  3.1 (Declarations), paragraphs 11-12 -- entries
      :term:`compile time`, :term:`declaration`.
   *  3.2 (Types and Subtypes), paragraph 1 -- entries :term:`type`,
      :term:`aggregate type`.
   *  3.2 (Types and Subtypes), paragraphs 2/2 and 4/2 -- entry
      :term:`aggregate type` (terminology note about "composite type").
   *  3.5 (Scalar Types), paragraph 1 -- entry :term:`scalar type`.
   *  4.9 (Static Expressions and Static Subtypes), paragraph 1 --
      entry :term:`static`.
   *  5.5 (Loop Statements), paragraphs 6-9 -- entries
      :term:`iterator variable`, :term:`domain`; defines the *loop
      parameter* of a ``for`` loop and its iteration scheme.
   *  Annex N (Glossary of Terms), entry "Execution" -- entry
      :term:`run time`.

.. [#iso-c11] ISO/IEC 9899:2011 (C11), WG14 Committee Draft N1570.
   https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf.  Year:
   2011.  N1570 is functionally identical to the published standard for
   the clauses cited here (§3.4.x, §3.15, §5.1.1.2, §6.2.1, §6.2.4,
   §6.2.5, §6.3, §6.5.4, §6.7, §6.7.3, §6.9, §6.4.2.1).  The C17
   revision (WG14 N2310) retains the same wording; the C23 revision
   (WG14 N3220) renumbers some clauses. When a *Gazprea* rule depends
   on a specific revision, we cite the revision year explicitly.

.. [#cpp-draft] ISO/IEC 14882 (C++23) working draft N4950, live-tracked
   mirror at https://eel.is/c++draft/, PDF at
   https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/n4950.pdf.
   Year: 2023.  Clauses cited from this glossary and where each is
   used:

   *  [expr.const.general] §7.7.1 -- entry :term:`constant expression`.
   *  [intro.execution] §6.10.1 -- entries :term:`sequenced before`,
      :term:`side effect`.
   *  [expr.pre] §7.1 -- entry :term:`expression`.
   *  [dcl.init.general] §9.5.1 -- entry :term:`initializer`.
   *  [lex.literal.kinds] §5.13.1 -- entry :term:`literal`.
   *  [basic.lval] §7.2.1 -- entries :term:`glvalue`, :term:`lvalue`,
      :term:`prvalue`, :term:`rvalue`, :term:`value category`,
      :term:`xvalue`.
   *  [basic.def.odr] §6.3 -- entry :term:`definition`.
   *  [stmt.pre] §8.1 -- entry :term:`statement`.
   *  [stmt.ranged] §8.6.5 -- entry :term:`iterator variable`;
      defines the range-based ``for`` statement's
      *for-range-declaration* and *for-range-initializer*.
   *  [iterator.requirements] §25.3 -- entry :term:`iterator`; defines
      iterators as generalized pointers into a range and enumerates
      the iterator category requirements.

.. [#cpp-defns] ISO/IEC 14882:2020 (C++20), the "defns" definitions
   section.  Draft mirror: https://timsong-cpp.github.io/cppwp/n4868/.
   Year: 2020.  Definitions cited from this glossary:

   *  [defns.well.formed] -- entry :term:`well-formed` (canonical
      wording: "C++ program constructed according to the syntax rules,
      diagnosable semantic rules, and the one-definition rule").
   *  [defns.ill.formed] -- entry :term:`ill-formed` ("program that is
      not well-formed").

.. rubric:: Industrial and open-source documentation

.. [#binutils-ld] GNU Binutils, ``ld`` manual, "Overview".
   https://sourceware.org/binutils/docs/ld/Overview.html.  Accessed
   2026-08-01.

.. [#gcc-int] *GNU Compiler Collection (GCC) Internals*, chapter
   "Passes and Files of the Compiler".
   https://gcc.gnu.org/onlinedocs/gccint/.  Accessed 2026-08-01.

.. [#llvm-langref] *LLVM Language Reference Manual*, "Type System".
   https://llvm.org/docs/LangRef.html#type-system.  For a stable
   snapshot cite a tagged release, e.g.
   https://releases.llvm.org/18.1.8/docs/LangRef.html.  Accessed
   2026-08-01.

.. [#llvm-orcjit] *LLVM Orc JIT v2 Documentation*,
   "ORC Design and Implementation".
   https://llvm.org/docs/ORCv2.html#design-overview. Accessed 2026-08-28

.. [#llvm-lto] *LLVM Link Time Optimization: Design and Implementation*.
   https://llvm.org/docs/LinkTimeOptimization.html.  Accessed
   2026-08-01.

.. [#llvm-mc] LLVM Machine Code (MC) toolkit, ``llvm-mc`` command guide.
   https://llvm.org/docs/CommandGuide/llvm-mc.html.  Accessed
   2026-08-01.

.. [#clang-cross] *Clang: Cross-compilation using Clang*.
   https://clang.llvm.org/docs/CrossCompilation.html.  Accessed
   2026-08-02.  "Clang/LLVM is natively a cross-compiler, meaning that
   one set of programs can compile to all targets by setting the
   ``-target`` option."

.. [#gcc-cross] *Using and Porting the GNU Compiler Collection (GCC):
   Cross-Compiler*.
   https://gcc.gnu.org/onlinedocs/gcc-3.0.4/gcc/Cross-Compiler.html.
   The host/target distinction and the requirement for a separate
   cross-assembler and cross-linker are described operationally here;
   the same model is retained in current GCC releases.

.. [#rust-ref-lifetimes] *The Rust Reference*, chapter "Lifetime
   elision" (types.html#r-type.lifetime.elision) and section
   "Generic parameters and where clauses" (items/generics.html).
   https://doc.rust-lang.org/reference/types.html and
   https://doc.rust-lang.org/reference/items/generics.html.
   Accessed 2026-08-03.  Normative reference for how the Rust
   type system encodes lifetimes.

.. [#rustonomicon-lifetimes] *The Rustonomicon*, chapter "References
   and Borrowing" (subsections on lifetimes and lifetime elision).
   https://doc.rust-lang.org/nomicon/lifetimes.html.  Accessed
   2026-08-03.  Effective (non-normative) tutorial-depth companion
   to the Rust Reference for readers new to borrow-checker
   reasoning.

.. rubric:: Peer-reviewed and textbook literature

.. [#dragon] Aho, A. V., Lam, M. S., Sethi, R., and Ullman, J. D.
   (2006). *Compilers: Principles, Techniques, and Tools* (2nd ed.).
   Addison-Wesley.  ISBN 0-321-48681-1.  Chapter 1, "Introduction",
   pp. 1-3.

.. [#milner-1978] Milner, R. (1978). "A Theory of Type Polymorphism in
   Programming."  *Journal of Computer and System Sciences*, 17(3),
   348-375.  DOI: https://doi.org/10.1016/0022-0000(78)90014-4.

.. [#pierce-tapl] Pierce, B. C. (2002). *Types and Programming
   Languages*.  MIT Press.  ISBN 0-262-16209-1.  Chapter 1
   ("Introduction"), for the definition of a type system and the
   static-versus-dynamic distinction.

.. [#quine-1960] Quine, W. V. O. (1960). *Word and Object*.  MIT Press.
   ISBN 0-262-67001-1.  Chapter 4, "Vagaries of Reference", §30-31
   ("Referential Opacity"), for the origin of *referential
   transparency*.

.. [#pep-234] van Rossum, G. and Yee, K.-P. (2001).  *PEP 234 --
   Iterators*.  Python Enhancement Proposal defining the Python
   iterator protocol (``__iter__``, ``__next__``).
   https://peps.python.org/pep-0234/.  Year: 2001.

.. [#meza-transpilers-2023] Meza Hormaza, J. (2023).  "Transpilers: A
   Systematic Mapping Review of Their Usage in Research and Industry."
   *Applied Sciences*, 13(6), 3667.  DOI:
   https://doi.org/10.3390/app13063667.  Note: the paper explicitly
   proposes a generic definition of *transpiler*, framed as filling a
   pre-existing terminological gap in the field; treat as evidence
   that *transpiler* lacks a prior standards-track definition rather
   than as the standard itself.

.. [#strachey-2000] Strachey, C. (2000).  "Fundamental Concepts in
   Programming Languages."  *Higher-Order and Symbolic Computation*,
   13(1-2), 11-49.  DOI: https://doi.org/10.1023/A:1010000313106.
   (Copenhagen lecture notes, originally delivered 1967.)  Historical
   origin of the L-value / R-value terminology and of the notion of
   referential transparency as applied to programming languages.

.. [#wadler-2015] Wadler, P. (2015).  "Propositions as Types."
   *Communications of the ACM*, 58(12), 75-84.  DOI:
   https://doi.org/10.1145/2699407.  Accessible entry-level survey of
   the Curry-Howard correspondence between logic and computation.

.. [#sorensen-urzyczyn-2006] Sørensen, M. H. and Urzyczyn, P. (2006).
   *Lectures on the Curry-Howard Isomorphism* (Studies in Logic and
   the Foundations of Mathematics, Vol. 149).  Elsevier.  ISBN
   0-444-52077-5.  Standard textbook treatment of the correspondence
   between typed lambda-calculi and natural deduction.

.. rubric:: Effective (non-normative) references

.. [#cppref-value-cat] *cppreference.com*, "Value categories".
   https://en.cppreference.com/w/cpp/language/value_category.  This is
   an accessible community-maintained summary of the C++ value-category
   taxonomy.  It is included here as an *effective* companion to the
   normative [#cpp-draft]_ citation, not as an authoritative
   source in its own right.

.. _ssec:glossary_doc_quality:

On writing glossaries
---------------------

The structure of this page follows established documentation practice.
The Diataxis framework classifies a glossary as *reference*
documentation, whose job is to describe -- accurately, austerely, and
without narrative -- the technical vocabulary of a system
[#diataxis]_.  The Write the Docs community guide reiterates the
constraint that reference material should be optimized for lookup
rather than for narrative reading [#wtd-reference]_.  Guidance on the
craft of glossary-writing itself is summarized by Lester at The
Word Factory [#wordfactory-glossary]_.  ISO/IEC/IEEE 26514:2022
gives the formal standards-track requirements for user documentation,
including terminology sections [#iso-26514]_.

.. [#diataxis] Procida, D. *Diataxis: A Systematic Framework for
   Technical Documentation Authoring*.  https://diataxis.fr/reference/.
   Accessed 2026-08-01.

.. [#wtd-reference] Write the Docs community, *Software documentation
   principles*.  https://www.writethedocs.org/guide/writing/docs-principles/.
   Accessed 2026-08-03.  Their "Meet users where they are" and
   "consistent" principles imply the same lookup-first constraint on
   reference material; the community's Diataxis-derived
   reference-docs page cited in earlier drafts of this glossary is no
   longer live.

.. [#wordfactory-glossary] Lester, M. "How to make a good glossary",
   The Word Factory.
   https://thewordfactory.com/how-to-make-a-good-glossary/.  Accessed
   2026-08-01.  A trade publication rather than an academic source;
   included as an effective reference on the craft of glossary
   compilation.

.. [#iso-26514] ISO/IEC/IEEE 26514:2022, *Systems and software
   engineering -- Design and development of information for users*.
   https://www.iso.org/standard/77451.html (also
   https://standards.ieee.org/ieee/26514/7467/).  Year: 2022.  The
   current revision of the standard covering the design and
   development of user documentation, including guidance on
   terminology and glossary sections; the front matter is available
   free, the full text is paywalled.

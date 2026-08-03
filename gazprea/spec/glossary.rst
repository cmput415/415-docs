.. _sec:glossary:

Glossary
========

This page collects the technical terminology used throughout the *Gazprea*
specification.  Its purpose is threefold: to fix the meaning of the words we
use so that the specification is self-consistent, to point the reader at the
authoritative literature behind each term, and to give students a
jumping-off point when they need to specify a language or compiler task
of their own.

Every entry below has a **primary citation** to an authoritative source:
an ISO/IEC or IEEE standard, the documentation of an ongoing industrial
open-source project (LLVM, GCC, GNU Binutils), or a peer-reviewed
publication in a respected venue.  Where a term has a widely-used *effective*
reference (e.g. cppreference for the C++ value categories), that reference
appears alongside the authoritative citation and is explicitly labelled as
non-normative.  Rejected sources -- those we considered and did not adopt
-- are listed in the :ref:`ssec:glossary_rejected` appendix so that a
reviewer can audit our choices.

Every glossary entry is a Sphinx ``:term:`` target and can be
cross-referenced from anywhere in the specification.  For example, a
sentence in another chapter can read
"``the size is fixed at`` :term:`elaboration <elaboration>` ``time``\ ".

.. note::

   The entries here are *definitions of terminology*, not statements of
   *Gazprea* semantics.  Where *Gazprea* re-uses a word from another
   language (for instance ``type qualifier``, which C reserves for
   ``const``/``volatile``/``restrict``/``_Atomic`` but *Gazprea* uses for
   the mutability distinction ``const``/``var``), the glossary explains
   the source of the word and points to the *Gazprea* chapter that gives
   its language-specific meaning.

.. contents:: On this page
   :local:
   :depth: 2

.. _ssec:glossary_terms:

Terms
-----

.. glossary::
   :sorted:

   aggregate type
      A type composed of subordinate members of possibly-different types.
      In ISO C the term denotes array and structure types collectively
      [#iso-c11]_.  In *Gazprea* the aggregate types are arrays, vectors,
      tuples, strings, and structs; see :ref:`sec:types`.

      *Terminology note.*  Ada calls this umbrella category *composite
      type* rather than *aggregate type* [#ada-rm-3-2-composite]_.  ISO C
      also defines *composite type* but with an unrelated meaning -- it
      is the merged type produced from two compatible declarations of
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
      by the :term:`compiler`, before program execution begins.  Ada
      states the contrast explicitly: "At compile time, the declaration
      of an entity declares the entity.  At run time, the elaboration of
      the declaration creates the entity" [#ada-rm-3-1]_.  The C
      standard specifies the phases of translation in ISO/IEC 9899
      §5.1.1.2 [#iso-c11]_.

   compiler
      A program that reads a source program in one language and
      produces an equivalent program in a target language [#dragon]_.
      GCC and LLVM/Clang are two production compilers whose internal
      architectures follow the classical front-end / middle-end /
      back-end division [#gcc-int]_ [#llvm-langref]_.

      *Compiler subtypes.*  The unmarked base case -- a compiler whose
      target is machine code executable by a CPU -- has no distinct
      term of art; it is simply *compiler*.  Two marked variants are
      recognised:

      *  A :term:`source-to-source translator` compiles from one
         high-level language to another high-level language [#dragon]_.
         The informal term *transpiler* is sometimes used for the same
         concept; it is not defined in any ISO/IEC standard, LLVM
         document, or GCC document, and the first attempt at a
         peer-reviewed generic definition appears in a 2023 mapping
         review [#meza-transpilers-2023]_.  Prefer *source-to-source
         translator* in the formal register.
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
      [#cpp-draft-const]_.  See :ref:`sec:constexpr` for *Gazprea*'s
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
      requirements are given in [basic.def] [#cpp-draft-odr]_; *Gazprea*
      does not adopt C++'s one-definition rule, so the citation is
      informational only.

   dynamic
      Determined or known at :term:`run time`.  Used as the antonym of
      :term:`static`.  ISO/IEC 9899 §6.2.4 uses "dynamic" implicitly by
      contrasting *static* storage duration with *automatic* and
      *allocated* storage durations whose extents are established during
      execution [#iso-c11]_.

   elaboration
      The process by which a declaration achieves its effect --
      allocating storage, computing size expressions, resolving
      instantiations, or otherwise binding the declaration to a
      concrete entity -- during a phase separate from ordinary
      expression evaluation.  The term is standard across several
      language families:

      *  Ada RM Annex N: "The process by which a declaration achieves
         its run-time effect is called elaboration.  Elaboration is one
         of the forms of execution" [#ada-rm-annex-n]_.
      *  IEEE 1076 (VHDL) §14.1: "The process by which a declaration
         achieves its effect is called the elaboration of the
         declaration.  After its elaboration, a declaration is said to
         be elaborated." [#ieee-1076]_
      *  IEEE 1800 (SystemVerilog) §3.12: "Elaboration is the process
         of binding together the components that make up a design ...
         Elaboration occurs after parsing the source code and before
         simulation" [#ieee-1800]_.
      *  Milner, Tofte, Harper and MacQueen, *The Definition of
         Standard ML (Revised)*, §1: "In the execution of a declaration
         there are three phases: parsing, elaboration, and evaluation
         ... Elaboration, the static phase, determines whether it is
         well-typed and well-formed in other ways, and records relevant
         type or form information in the basis" [#sml-defn]_.

      When the size of a *Gazprea* array is fixed at the first
      evaluation of its declaration rather than at :term:`compile time`,
      we say the size is fixed at *elaboration time*, in the same sense
      as Ada and VHDL.  Note that SML uses "elaboration" for a static
      (compile-time) phase; *Gazprea*'s usage follows the Ada/VHDL
      dynamic sense.

   expression
      "A sequence of operators and operands that specifies a
      computation.  An expression can result in a value and can cause
      side effects" [#cpp-draft-expr]_.  The syntactic shape of
      expressions in *Gazprea* is defined in :ref:`sec:expressions`.

   functional purity
      An informal property of a language, expression, or function: the
      absence of observable :term:`side effects <side effect>`.  There
      is no ISO definition; the standard academic reference is
      Strachey's characterisation of :term:`referential transparency`
      [#strachey-2000]_.  *Gazprea* invokes functional purity as the
      motivation for forbidding mutable :ref:`globals <sec:global>` and
      for the input-only nature of function arguments.

   glvalue
      A "generalized" lvalue: "an expression whose evaluation
      determines the identity of an object, function, non-static data
      member, or a direct base class relationship" [#cpp-draft-lval]_.
      One of the three C++11 :term:`value categories <value category>`
      (together with :term:`prvalue` and :term:`xvalue`).  See the
      non-normative summary at [#cppref-value-cat]_ for an accessible
      introduction.

   identifier
      "A sequence of nondigit characters ... and digits, which
      designates one or more entities" [#iso-c11]_.  *Gazprea*'s lexical
      rules for identifiers are in :ref:`sec:identifiers`.

   ill-formed
      A program is *ill-formed* if it is not :term:`well-formed`
      [#cpp-defns-ill]_.  A conforming implementation is required to
      issue a diagnostic for at least one violation of a diagnosable
      rule in an ill-formed program.

   implementation-defined behavior
      "Unspecified behavior where each implementation documents how the
      choice is made" [#iso-c11]_.  Distinct from
      :term:`unspecified behavior` (no documentation obligation) and
      :term:`undefined behavior` (no requirements at all).

   implicit conversion
      An automatic conversion inserted by the language, without a cast,
      to make an operand's type match a required target type.  ISO C
      collects the rules under §6.3 "Conversions" [#iso-c11]_.

      *Gazprea* uses this general term only in the glossary.  In the
      *Gazprea* specification proper the analogous mechanism is called
      :ref:`type promotion <sec:typePromotion>`, and it is
      deliberately distinct from :term:`type casting`: type promotion
      is the *implicit* mechanism (e.g. ``integer`` -> ``real`` when
      arithmetic mixes them), while type casting is the *explicit*
      mechanism invoked via ``as<toType>(value)``.  The two are not
      interchangeable in *Gazprea*: some casts have no corresponding
      implicit promotion.

   initializer
      The syntactic element that supplies an initial value to a newly
      declared object.  In C++ the grammar is given in
      ``[dcl.init.general]`` [#cpp-draft-init]_.  *Gazprea*'s
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
      [#iso-c11]_.  Link-time optimisation (LTO), performed at this
      point, is documented for the LLVM toolchain in [#llvm-lto]_.

   literal
      A token whose value is the token itself: integer, floating-point,
      character, string, boolean, and (in C++) pointer literals
      [#cpp-draft-literal]_.  Contrast a literal with a
      :term:`constant expression`, which may be composed of literals
      and other operators.

   lvalue
      "An expression (with an object type other than void) that
      potentially designates an object" [#iso-c11]_.  C++ defines an
      lvalue as "a :term:`glvalue` that is not an :term:`xvalue`"
      [#cpp-draft-lval]_.  The historical origin of the "l-value" and
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
      glossary the word always refers to the *run-time* entity, never
      to an object in the sense of object-oriented programming.

   primitive type
      A type provided directly by the language and not composed of
      other types.  The LLVM Language Reference distinguishes
      *primitive* types (``i32``, floating-point types, ``void``, etc.)
      from *derived* and *aggregate* types [#llvm-langref]_.  In
      *Gazprea* the primitive types are ``boolean``, ``integer``,
      ``real``, and ``character``.

   prvalue
      A "pure r-value": "an expression whose evaluation initializes an
      object or computes the value of an operand of an operator ... or
      an expression that has type cv void" [#cpp-draft-lval]_.  One of
      the three C++11 :term:`value categories <value category>`.

   pure function
      See :term:`functional purity`.

   referential transparency
      The property that an expression's value depends only on the
      values of its subexpressions, so that any subexpression may be
      replaced by an equal-valued subexpression without changing the
      whole [#strachey-2000]_.  The term is due to Quine
      [#quine-1960]_.  *Gazprea* invokes referential transparency
      implicitly through its ban on mutable globals in function bodies.

   run time
      The interval during which the program is executing, after
      :term:`translation` and :term:`link time` are complete.  Ada
      defines the corresponding process, *execution*, as "the process
      by which a construct achieves its run-time effect"
      [#ada-rm-annex-n]_.

   rvalue
      C++ defines an rvalue as "a :term:`prvalue` or an :term:`xvalue`"
      [#cpp-draft-lval]_.  In C the term is used informally as the
      complement of :term:`lvalue`.  Historical origin: Strachey
      [#strachey-2000]_.

   scalar type
      A type whose values are atomic in the sense that they are not
      composed of sub-elements.  ISO C: "Arithmetic types and pointer
      types are collectively called scalar types" [#iso-c11]_.  Ada
      groups enumeration, integer, and real types as scalar
      [#ada-rm-3-5]_.  In *Gazprea* the scalar types are ``boolean``,
      ``integer``, ``real``, and ``character``.

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
      [#cpp-draft-exec]_.  The relation supplants the older ISO C
      *sequence point* model for describing the ordering of
      :term:`side effects <side effect>`.

   side effect
      "Reading an object designated by a volatile glvalue, modifying an
      object, ... calling a library I/O function, or calling a function
      that does any of those operations" -- any "change in the state of
      the execution or translation environment" [#cpp-draft-exec]_.
      ISO C gives an equivalent enumeration [#iso-c11]_.

   statement
      A syntactic construct whose primary role is to be executed for
      its effect rather than to compute a value.  The C++ grammar
      enumerates the kinds of statement in ``[stmt.pre]``
      [#cpp-draft-stmt]_.  *Gazprea*'s statements are covered in
      :ref:`sec:statements`.

   static
      Determined or known at :term:`compile time`.  Ada gives the
      cleanest formal definition: "Static means determinable at compile
      time, using the declared properties or values of the program
      entities" [#ada-rm-4-9]_.  Contrast with :term:`dynamic`.

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
      A characterisation of a set of values together with a set of
      operations on those values [#ada-rm-3-2]_ [#pierce-tapl]_.
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

   type promotion
      In general PL usage, an :term:`implicit conversion` in which an
      operand of one type is converted to a "wider" or "richer" type
      before an operation; ISO C specifies *integer promotions*
      (§6.3.1.1) and the *usual arithmetic conversions* (§6.3.1.8)
      [#iso-c11]_.

      In *Gazprea*, *type promotion* is the specific implicit-conversion
      mechanism defined in :ref:`sec:typePromotion` (integer to real,
      scalar to array, tuple to tuple, string to character-vector and
      back).  It is deliberately separate from :term:`type casting`,
      which is the explicit mechanism invoked via ``as<toType>(value)``.
      Every promotion is available as an explicit cast, but not every
      cast is available as an implicit promotion.

   type qualifier
      In ISO C the term refers to the *cv*-qualifiers ``const``,
      ``restrict``, ``volatile``, and ``_Atomic``, defined in §6.7.3
      [#iso-c11]_.  *Gazprea* re-uses the phrase for the mutability
      qualifiers ``const`` and ``var`` (see :ref:`sec:typeQualifiers`);
      this is a *terminological convention*, not an assertion that
      *Gazprea*'s qualifiers behave like C's.

   type system
      A tractable syntactic method for classifying phrases of a
      language by the kinds of values they compute
      [#pierce-tapl]_.  Type systems are traditionally divided into
      *static* systems (checking performed before execution) and
      *dynamic* systems (checking performed during execution); see
      Pierce, Chapter 1 [#pierce-tapl]_.

   undefined behavior
      "Behavior ... for which this document imposes no requirements"
      [#iso-c11]_.  A program exhibiting undefined behavior at run time
      is not obliged to signal an error, terminate, or produce any
      particular output.  Contrast :term:`unspecified behavior` and
      :term:`implementation-defined behavior`.

   unspecified behavior
      "Use of an unspecified value, or other behavior where this
      document provides two or more possibilities and imposes no
      further requirements on which is chosen in any instance"
      [#iso-c11]_.

   value category
      "Every expression belongs to exactly one of the fundamental
      categories in [the C++] taxonomy: lvalue, xvalue, or prvalue.
      This property of an expression is called its value category"
      [#cpp-draft-lval]_.  A non-normative overview lives at
      [#cppref-value-cat]_.

   well-formed
      "C++ program constructed according to the syntax rules,
      diagnosable semantic rules, and the one-definition rule"
      [#cpp-defns-well]_.  *Gazprea* uses "well-formed" throughout in
      this generalised sense: a *Gazprea* program is well-formed if it
      satisfies every diagnosable rule stated in this specification.

   xvalue
      An "expiring" value: "a :term:`glvalue` that denotes an object
      whose resources can be reused (usually because it is near the end
      of its lifetime)" [#cpp-draft-lval]_.  One of the three C++11
      :term:`value categories <value category>`.


.. _ssec:glossary_authoritative:

Authoritative sources
---------------------

The primary citations for the entries above are listed here.  All URLs
were captured for later ``archive.org`` snapshotting.

.. rubric:: Standards

.. [#ada-rm-3-1] ISO/IEC 8652:2012, *Information technology --
   Programming languages -- Ada*, clause 3.1 (Declarations), paragraph
   11-12.  Ada-Auth reference manual mirror:
   http://www.ada-auth.org/standards/12rm/html/RM-3-1.html.  Year:
   2012.

.. [#ada-rm-3-2] ISO/IEC 8652:2012, clause 3.2 (Types and Subtypes),
   paragraph 1.  http://www.ada-auth.org/standards/12rm/html/RM-3-2.html.
   Year: 2012.

.. [#ada-rm-3-2-composite] ISO/IEC 8652:2012, clause 3.2 (Types and
   Subtypes), paragraph 2/2: "Elementary types are those whose values
   are logically indivisible; composite types are those whose values are
   composed of component values", and paragraph 4/2: "The composite
   types are the record types, record extensions, array types, interface
   types, task types, and protected types."
   http://www.ada-auth.org/standards/12rm/html/RM-3-2.html.  Year: 2012.

.. [#ada-rm-3-5] ISO/IEC 8652:2012, clause 3.5 (Scalar Types), paragraph
   1.  http://www.ada-auth.org/standards/12rm/html/RM-3-5.html.  Year:
   2012.

.. [#ada-rm-4-9] ISO/IEC 8652:2012, clause 4.9 (Static Expressions and
   Static Subtypes), paragraph 1.
   http://www.ada-auth.org/standards/12rm/html/RM-4-9.html.  Year: 2012.

.. [#ada-rm-annex-n] ISO/IEC 8652:2012, Annex N (Glossary of Terms),
   entries "Elaboration" and "Execution".
   http://www.ada-auth.org/standards/12rm/html/RM-N.html.  Year: 2012.

.. [#ieee-1076] IEEE Std 1076-2008, *IEEE Standard VHDL Language
   Reference Manual*, clause 14 (Elaboration and execution), §14.1
   (General).  https://ieeexplore.ieee.org/document/4772740/.  Year:
   2009.  The 2019 revision (IEEE Std 1076-2019) retains the same
   clause structure.

.. [#ieee-1800] IEEE Std 1800-2017, *IEEE Standard for SystemVerilog --
   Unified Hardware Design, Specification, and Verification Language*,
   clause 3.12 (Compilation and elaboration) and clause 23.10.4
   (Elaboration).  https://ieeexplore.ieee.org/document/8299595/.
   Year: 2017.  The 2012 revision (IEEE Std 1800-2012) uses the same
   clause numbering.

.. [#sml-defn] Milner, R., Tofte, M., Harper, R., and MacQueen, D.
   (1997).  *The Definition of Standard ML (Revised)*.  MIT Press.
   ISBN 0-262-63181-4.  §1 (Introduction).  Publicly-available copy at
   https://smlfamily.github.io/sml97-defn.pdf.  Notes that "elaboration"
   in SML is the static (compile-time) type-checking phase, distinct
   from the dynamic sense used by Ada and VHDL.

.. [#iso-c11] ISO/IEC 9899:2011 (C11), WG14 Committee Draft N1570.
   https://www.open-std.org/jtc1/sc22/wg14/www/docs/n1570.pdf.  Year:
   2011.  N1570 is functionally identical to the published standard for
   the clauses cited here (§3.4.x, §3.15, §5.1.1.2, §6.2.1, §6.2.4,
   §6.2.5, §6.3, §6.5.4, §6.7, §6.7.3, §6.9, §6.4.2.1).  The C17
   revision (WG14 N2310) retains the same wording; the C23 revision
   (WG14 N3220) renumbers some clauses -- when a *Gazprea* rule depends
   on a specific revision, cite the revision year explicitly.

.. [#cpp-draft-const] ISO/IEC 14882 (C++23) working draft N4950,
   [expr.const.general] §7.7.1, paragraph 1.
   https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/n4950.pdf.
   Year: 2023.  Live-tracked draft mirror: https://eel.is/c++draft/expr.const.

.. [#cpp-draft-exec] ISO/IEC 14882 working draft N4950,
   [intro.execution] §6.10.1, paragraphs 7-10.
   https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/n4950.pdf.
   Live-tracked mirror: https://eel.is/c++draft/intro.execution.  Year: 2023.

.. [#cpp-draft-expr] ISO/IEC 14882 working draft N4950, [expr.pre]
   §7.1, paragraph 1.
   https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/n4950.pdf.
   Live-tracked mirror: https://eel.is/c++draft/expr.pre.  Year: 2023.

.. [#cpp-draft-init] ISO/IEC 14882 working draft N4950,
   [dcl.init.general] §9.5.1, paragraph 1.
   https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/n4950.pdf.
   Live-tracked mirror: https://eel.is/c++draft/dcl.init.general.  Year:
   2023.

.. [#cpp-draft-literal] ISO/IEC 14882 working draft N4950,
   [lex.literal.kinds] §5.13.1.
   https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/n4950.pdf.
   Live-tracked mirror: https://eel.is/c++draft/lex.literal.kinds.  Year:
   2023.

.. [#cpp-draft-lval] ISO/IEC 14882 working draft N4950, [basic.lval]
   §7.2.1, paragraphs 1-2.
   https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/n4950.pdf.
   Live-tracked mirror: https://eel.is/c++draft/basic.lval.  Year: 2023.

.. [#cpp-draft-odr] ISO/IEC 14882 working draft N4950, [basic.def.odr]
   §6.3, paragraph 2.
   https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/n4950.pdf.
   Live-tracked mirror: https://eel.is/c++draft/basic.def.odr.  Year:
   2023.

.. [#cpp-draft-stmt] ISO/IEC 14882 working draft N4950, [stmt.pre]
   §8.1.
   https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2023/n4950.pdf.
   Live-tracked mirror: https://eel.is/c++draft/stmt.pre.  Year: 2023.

.. [#cpp-defns-well] ISO/IEC 14882:2020, definition
   [defns.well.formed]: "C++ program constructed according to the
   syntax rules, diagnosable semantic rules, and the one-definition
   rule".  Draft mirror:
   https://timsong-cpp.github.io/cppwp/n4868/defns.well.formed.  Year:
   2020.

.. [#cpp-defns-ill] ISO/IEC 14882:2020, definition [defns.ill.formed]:
   "program that is not well-formed".  Draft mirror:
   https://timsong-cpp.github.io/cppwp/n4868/defns.ill.formed.  Year:
   2020.

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

.. rubric:: Effective (non-normative) references

.. [#cppref-value-cat] *cppreference.com*, "Value categories".
   https://en.cppreference.com/w/cpp/language/value_category.  This is
   an accessible community-maintained summary of the C++ value-category
   taxonomy.  It is included here as an *effective* companion to the
   normative [#cpp-draft-lval]_ citation, not as an authoritative
   source in its own right.

.. _ssec:glossary_rejected:

Rejected sources
----------------

The following sources were considered during the drafting of this
glossary and rejected.  They are recorded here so that a reviewer can
audit our source-selection decisions.

*Community-maintained encyclopedias and tutorials.*  Wikipedia articles
on "Value categories", "Sequence point", "Name binding", the various
ISO C revisions, GeeksforGeeks, W3Schools, TutorialsPoint,
learncpp.com, and Microsoft Learn "previous-versions" pages were not
adopted as primary citations.  They are useful for triage and
navigation but are tertiary summaries rather than normative sources.

*Vendor product pages.*  Microsoft Learn's own "Lvalues and Rvalues
(C++)" page is vendor documentation of a specific implementation, not
a standard, and was rejected in favour of the ISO/IEC 14882 draft.

*Community coding-standard wikis.*  The SEI CERT C Coding Standard
wiki was consulted to cross-check clause numbering but is a coding
standard atop the language standard rather than a language standard
itself.

*Q&A and forum threads.*  Stack Overflow, Reddit, and mailing-list
threads were not cited as primary sources for any term, in accordance
with the source-preference policy given at the top of this page.

*Paywalled front-matter.*  ISO/IEC 2382:2015 (*Information technology
-- Vocabulary*) would in principle be authoritative but is paywalled
with only its scope and foreword available for public inspection; no
clause text could be verified, so it was not cited.

.. _ssec:glossary_doc_quality:

On writing glossaries
---------------------

The structure of this page follows established documentation practice.
The Diataxis framework classifies a glossary as *reference*
documentation, whose job is to describe -- accurately, austerely, and
without narrative -- the technical vocabulary of a system
[#diataxis]_.  The Write the Docs community guide reiterates the
constraint that reference material should be optimised for lookup
rather than for narrative reading [#wtd-reference]_.  Guidance on the
craft of glossary-writing itself -- one entry per concept, plain
language, definitions that do not re-use the word being defined, and
concrete examples where possible -- is summarised by Lester at The
Word Factory [#wordfactory-glossary]_.  ISO/IEC/IEEE 26514:2022
gives the formal standards-track requirements for user documentation,
including terminology sections [#iso-26514]_.

.. [#diataxis] Procida, D. *Diataxis: A Systematic Framework for
   Technical Documentation Authoring*.  https://diataxis.fr/reference/.
   Accessed 2026-08-01.

.. [#wtd-reference] Write the Docs community, *Documentation Guide*,
   "Reference".  https://www.writethedocs.org/guide/writing/reference-docs/.
   Accessed 2026-08-01.

.. [#wordfactory-glossary] Lester, M. "How to make a good glossary",
   The Word Factory.
   https://thewordfactory.com/how-to-make-a-good-glossary/.  Accessed
   2026-08-01.  A trade publication rather than an academic source;
   included as an effective reference on the craft of glossary
   compilation.

.. [#iso-26514] ISO/IEC/IEEE 26514:2022, *Systems and software
   engineering -- Design and development of information for users*.
   https://www.iso.org/standard/81352.html.  Year: 2022.  The current
   revision of the standard covering the design and development of
   user documentation, including guidance on terminology and glossary
   sections; the front matter is available free, the full text is
   paywalled.

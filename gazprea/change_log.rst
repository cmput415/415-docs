.. _sec:changelog:

Change log
==========

- **2020/10/22 4:20**

  - Cleaned up latex artifacts messing up a code block.
    (:ref:`ssec:statements_return`, :numref:`ssec:statements_return`)
  - Changed ``pythag`` function so that the exponent is a real.
    (:ref:`ssec:function_syntax`, :numref:`ssec:function_syntax`)
  - Fixed latex artifact where ``character`` literal for ``'`` was ``\’``
    not ``\'``. (:ref:`sssec:character_lit`, :numref:`sssec:character_lit`)
  - Removed usages of ``std_output`` as an assignable value.
    (:ref:`ssec:procedure_main`, :numref:`ssec:procedure_main`;
    :ref:`ssec:typePromotion_ttot`, :numref:`ssec:typePromotion_ttot`;
    :ref:`sssec:string_ops`, :numref:`sssec:string_ops`;
    :ref:`ssec:typePromotion_stov`, :numref:`ssec:typePromotion_stov`)
  - Remove mention of ``matrix`` keyword that no longer exists.
    (:ref:`sssec:matrix_decl`, :numref:`sssec:matrix_decl`)
  - Clarify lack of ``= <stmt>;`` format for procedures.
    (:ref:`ssec:procedure_syntax`, :numref:`ssec:procedure_syntax`)
  - Fix usage of ``if ... fi`` that is not used in *Gazprea*.
    (:ref:`sssec:tuple_ops`, :numref:`sssec:tuple_ops`).
  - Remove usage of ``0.0f`` which is C syntax. (:ref:`ssec:statements_assign`,
    :numref:`ssec:statements_assign`)
  - Fix malformed types for vectors and matrices where the size was not
    attached to the type. (:ref:`sssec:vector_ops`, :numref:`sssec:vector_ops`;
    :ref:`sssec:matrix_decl`, :numref:`sssec:matrix_decl`)
  - Clarified format of ``real`` literals without scientific notation.
    (:ref:`sssec:real_lit`, :numref:`sssec:real_lit`)
  - Clarified format of ``real`` literals with scientific notation.
    (:ref:`sssec:real_lit`, :numref:`sssec:real_lit`)

-  **2020/09/01 3:00**

   -  Initial release for Fall 2020

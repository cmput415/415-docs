.. _sec:changelog:

Change log
==========

- **2020/11/18 19:00**

  - Clarified when memory should be freed. (:ref:`ssec:backend_memory`)
  - Clarified that typedef type symbol names do not conflict with variable or
    subroutine symbol names. (:ref:`sec:typedef`, :numref:`sec:typedef`)
  - Clarified that ``null`` and ``identity`` cannot be cast.
    (:ref:`ssec:typeCasting_nai`, :numref:`ssec:typeCasting_nai`)
  - Clarified that "two sided" promotion may occur with tuples.
    (:ref:`ssec:typePromotion_ttot`, :numref:`ssec:typePromotion_ttot`)
  - Clarified that ``return`` statements must have values compatible with the
    type in the ``returns`` clause. (:ref:`ssec:statements_return`,
    :numref:`ssec:statements_return`)
  - Clarified that procedures without ``returns`` clauses do not require explicit
    ``return`` statements. (:ref:`ssec:statements_return`,
    :numref:`ssec:statements_return`)
  - Clarified that scalar ``character`` values can still take part in the
    concatenation (``||``) operation with a ``string`` or vector with type
    ``character``. (:ref:`sssec:character_ops`, :numref:`sssec:character_ops`)
  - Rewrote several sections of ``string``:

    - Clarified differences in type description. (:ref:`ssec:string`,
      :numref:`ssec:string`)
    - Clarified declaration methods. (:ref:`sssec:string_decl`,
      :numref:`sssec:string_decl`)
    - Clarified concatentation of characters onto strings.
      (:ref:`sssec:string_ops`, :numref:`sssec:string_ops`)

  - Clarified that whitespace cannot be in a real literal when in the input
    stream. (:ref:`sssec:input_format`, :numref:`sssec:input_format`)
  - Fixed example of misreading a ``boolean`` from the ``std_input``.
    (:ref:`sssec:input_format`, :numref:`sssec:input_format`).
  - Added restrictions on input stream rewinding.
    (:ref:`ssec:builtIn_stream_state`, :numref:`ssec:builtIn_stream_state`;
    :ref:`sssec:stream_error`, :numref:`sssec:stream_error`)
  - Moved and expanded description of stream rewinding.
    (:ref:`ssec:builtIn_stream_state`, :numref:`ssec:builtIn_stream_state`;
    :ref:`sssec:stream_error`, :numref:`sssec:stream_error`)
  - Removed "and subsequent reads" due to ever-expanding nature of
    ``std_input``. (:ref:`sssec:stream_error`, :numref:`sssec:stream_error`)
  - Trimmed information in description of ``stream_state`` which was duplicating
    the description of streams. (:ref:`ssec:builtIn_stream_state`,
    :numref:`ssec:builtIn_stream_state`)

- **2020/10/22 16:20**

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

-  **2020/09/01 15:00**

   -  Initial release for Fall 2020

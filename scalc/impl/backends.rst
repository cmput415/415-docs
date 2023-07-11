Backends
========

*SCalc*. This compiler will directly generate code for the following
three backends:

-  :ref:`ssec:backend_x86` assembly

-  :ref:`ssec:backend_risc` assembly

-  :ref:`ssec:backend_arm` assembly

You must also create an :ref:`ssec:backend_interp` for *SCalc*

.. _ssec:backend_risc:

RISC-V
------

We recommend that you implement variables in the ``.data`` segment of
your assembly code using ``.word`` entries. The general syntax for RISC-V
assembly is as follows:

::

     .data
     _newline: .asciz "\n"
     var1: .word 0
     var2: .word 0
     ...

     .text
     main:
        <your generated code goes here>
        li   a7, 10
        ecall

This reference is the `RISC-V Assembler and Runtime Simulator (RARS) <https://github.com/TheThirdOne/rars>`, which includes a list of available syscalls.
To print integers you should use the print int ecall (``1``). To print
strings, you should use the print string ecall (``4``) in combination
with the address of a string you’ve defined in the ``.data`` section
containing only a new line character (see above).

If you save the *RISC-V* output as ``program.s`` then you can run it with
the command:

::

     java -jar .../rars1_6.jar program.s

If you wish to debug you may also launch RARS with the command:

::

     java -jar .../rars1_6.jar

which opens a graphical IDE that you can load your assembler code into.


.. _ssec:backend_x86:

x86
---

You should use the Intel syntax for *x86*, and your compiler’s output
must work with the nasm assembler. Your *x86* output should look
something like this:

::

     global main
     extern printf

     section .data
     var1: DD 0
     var2: DD 0
     ...

     section .text
       main:
         <your generated code goes here>
         mov eax, 0 ; Set return value
         ret        ; Return

Print will use ``printf``, which we will link in later to make it easier
to implement the ``print`` statement. Printing consists of three steps:

#. Push the arguments onto the stack in reverse order.

#. Call ``printf``.

#. Clean up the stack.

For instance, the following segment of code contains a call to
``printf``:

::

     global main
     extern printf
     section .data
     _format_string: DB "Hello! Here is a number: %d",0xA,0x0

     section .text
       main:
         push dword 7        ; Second argument
         push _format_string ; First argument (remember stacks are FILO)
         call printf         ; Make the call to printf
         add esp, 8          ; Pop the stack, we are done!

         mov eax, 0
         ret

``_format_string`` deserves a quick explanation. The ``DB`` declares a
datatype of bytes, which is appropriate for characters. The string is
converted to its character components and placed at the label. The
values in commas after it are appended to the array. ``0xA`` is the
`ASCII value of a newline in
hexadecimal <http://www.asciitable.com/>`__. The ``0x0`` is the `null
terminator <https://en.wikipedia.org/wiki/Null-terminated_string>`__ for
the string.

You won’t need to know more of the *x86* calling conventions than what
was demonstrated above.

If you save the *x86* output as ``program.s`` you can assemble an
executable and run it by executing the following commands:

::

     nasm -felf -o program.o program.s
     gcc -m32 -o program program.o
     ./program

Try this on the ``printf`` example and make sure that it works!

.. _ssec:backend_arm:

ARM
---

The *ARM* assembly output should look something like this:

::

     .arch armv7-a
     .data
     _format_string: .asciz "%d\n"
     var1: .word 0
     var2: .word 0
     ...

     .text
     .globl main
     main:
       push {ip, lr}      // Save link and scratch registers.

       <your generated code goes here>

       pop  {ip, lr}      // Load link and scratch registers.
       mov  r0, #0        // Set return value.
       bx   lr            // Return.

We will also be using ``printf`` with *ARM*. The *ARM* calling
convention is different from *x86*: the first argument is passed in r0,
and the second argument is passed in r1. The following code demonstrates
a call to ``printf`` in *ARM* assembly:

::

     .arch armv7-a
     .data
     _format_string: .asciz "Hello! Here is a number: %d\n"

     .text
     .globl main
     main:
       push {ip, lr}      // Save link and scratch registers.

       ldr r0, =_format_string // Load the address of the format string into the first argument.
       mov r1, #7         // Place the literal 7 into the second argument.
       bl printf          // Call printf.

       pop  {ip, lr}      // Load link and scratch registers.
       mov  r0, #0        // Set return value.
       bx   lr            // Return.

Aside from the difference in calling convention, this code is very
similar to the *x86* example. As well, declaring the ``_format_string``
is a lot easier because it has a null-terminated string directive and
can parse ``\n`` like *RISC-V*.

*ARMv7-A* lacks a division instruction. Therefore, we have to call the
subroutine ``__aeabi_idiv`` to perform integer division. The following
code demonstrates a call to ``__aeabi_idiv`` in *ARM* assembly:

::

     .arch armv7-a
     .data

     .text
     .globl main
     main:
       push {ip, lr}      // Save link and scratch registers.

       mov r0, #5         // Move the literal 5 into the first argument (the dividend).
       mov r1, #3         // Move the literal 3 into the second argument (the divisor).
       bl __aeabi_idiv(PLT) // Divide 5 by 3, return the result in r0.

       pop  {ip, lr}      // Load link and scratch registers.
       mov  r0, #0        // Set return value.
       bx   lr            // Return.

In order to assemble and run an executable you may run the following
commands:

::

     arm-none-eabi-as -o program.o program.s
     arm-none-eabi-gcc -specs=rdimon.specs -o program program.o
     qemu-arm ./program

Try this on the ``printf`` example and make sure that it works!

.. _ssec:backend_interp:

Interpreter
-----------

You should be able to execute a program without compiling by
implementing an interpreter. This should work similarly to the generator
assignment.


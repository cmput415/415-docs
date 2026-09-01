dragon-runner
=============

``dragon-runner`` is the test harness for every language project in the course. It feeds each test file through a *toolchain* — your compiler, then whatever it takes to run the result — and diffs what comes out against the expected output written inside the test file. The same tool produces your grade, so a test that passes locally is a test that passes for the grader.

Installation instructions are on the `setup pages <https://cmput415.github.io/415-docs/setup/>`_. The source lives at `cmput415/Dragon-Runner <https://github.com/cmput415/Dragon-Runner>`_.

Running the tester
------------------

.. code-block:: console

 $ dragon-runner [mode] <config>.json [options]

The mode defaults to ``regular``; the other modes (``tournament``, ``perf``, ``memcheck``) are what the graders run. ``dragon-runner --help`` lists every option — the four worth knowing up front are:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Option
     - Effect
   * - ``-v``
     - Print expected and generated output for each failure. Without it a failure is a bare ``[FAIL]`` line.
   * - ``-p PATTERN``
     - Only run packages whose path matches the glob, e.g. ``-p '*arrays*'``.
   * - ``--debug-package PATH``
     - Run a single package by path. Faster than ``-p`` when you already know where the test is.
   * - ``--timeout SECONDS``
     - Per-test timeout. The default is 2 seconds, which a debug build can exceed on a heavy test.

Every path inside the config is resolved relative to the config file, so the command works from any directory:

.. code-block:: console

 $ dragon-runner tests/littleCConfig.json -v --timeout 10

Reading the results
-------------------

.. list-table::
   :header-rows: 1
   :widths: 20 80

   * - Marker
     - Meaning
   * - ``[PASS]``
     - Every step exited cleanly and the final stdout matched the expected output exactly.
   * - ``[FAIL]``
     - Every step exited cleanly but the output did not match.
   * - ``[E-PASS]``
     - A step exited non-zero, and its stderr matched the error named in the expected output.
   * - ``[E-FAIL]``
     - A step exited non-zero and its stderr did not match what the test expected.
   * - ``[TIMEOUT]``
     - A step ran past ``--timeout``.

A step is only allowed to exit non-zero if its config entry sets ``allowError``; otherwise the failure aborts the toolchain. When a test is an error test, the diff is lenient: dragon-runner looks for an error name such as ``SizeError`` or ``IndexError`` in both the expected and generated text rather than demanding a byte-for-byte match.

Output with ``-v``:

.. code-block:: text

 Running executable: solution
   Running Toolchain: littlec
    Entering package solution
     Entering subpackage 01-basics
      [PASS] assign_01.test
      [FAIL] division_truncates_01.test
        ==> Expected Out (2 bytes):
         b'-3'
        ==> Generated Out (2 bytes):
         b'-4'
     Subpackage Passed:  1 / 2

Writing a test
--------------

A test file is a complete program in the language, followed by directives in comments that declare the program's stdin and its expected stdout. Directives use the language's line-comment syntax (``//``) and may appear anywhere in the file.

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Directive
     - Meaning
   * - ``//CHECK:<text>``
     - One line of expected stdout.
   * - ``//INPUT:<text>``
     - One line fed to the program's stdin.
   * - ``//CHECK_FILE:<path>``
     - Read the expected stdout from a file beside the test.
   * - ``//INPUT_FILE:<path>``
     - Read stdin from a file beside the test.

Repeat ``CHECK:`` and ``INPUT:`` for further lines; dragon-runner joins them with newlines. Neither directive appends a trailing newline, so a program whose last statement prints a newline needs an empty ``//CHECK:`` at the end. The inline and file forms of a directive cannot both appear in one test.

``tests/testfiles/solution/littlec/01-basics/assign_01.test``:

.. code-block:: c

 int x = 1;
 x = 42;
 print(x);
 //CHECK:42
 //CHECK:

In a language whose programs read stdin, ``INPUT:`` supplies it. Here two lines are read and echoed back:

.. code-block:: c

 //INPUT:a
 //INPUT:b
 #include <stdio.h>

 int main() {
   char x, y, nl;
   scanf("%c", &x);
   scanf("%c", &nl);
   scanf("%c", &y);
   printf("%c\n%c\n", x, y);
   return 0;
 }
 //CHECK:a
 //CHECK:b
 //CHECK:

Files ending in ``.out`` and ``.ins`` are reserved for ``CHECK_FILE``/``INPUT_FILE`` payloads, and dot-files are skipped. Everything else in a test directory is treated as a test, whatever its extension.

Directory structure
-------------------

Each top-level directory under ``testDir`` is a *package*; every directory beneath a package that contains at least one test is a *subpackage*. Nesting deeper than one level is fine. Packages are the unit of submission — yours must be named after your team ID or SID — and subpackages are how you group tests by feature.

::

 tests
 ├── littleCConfig.json
 └── testfiles
     └── solution              <- package
         └── littlec
             ├── 01-basics     <- subpackage
             │   ├── assign_01.test
             │   └── decl_init_01.test
             ├── 02-expressions
             │   ├── precedence_mul_over_add_01.test
             │   └── unary_minus_01.test
             └── 03-control-flow
                 └── else_binds_to_nearest_if_01.test

The config
----------

``tests/littleCConfig.json`` from the littleC solution builds an LLVM IR file with the compiler under test, then interprets it with ``lli``:

.. code-block:: json

 {
   "testDir": "testfiles",
   "testedExecutablePaths": {
     "solution": "../bin/littlec"
   },
   "toolchains": {
     "littlec": [
       {
         "stepName": "littlec",
         "executablePath": "$EXE",
         "arguments": ["$INPUT", "$OUTPUT"],
         "output": "littlec.ll",
         "allowError": true
       },
       {
         "stepName": "lli",
         "executablePath": "$MLIR_INS/bin/lli",
         "arguments": ["$INPUT"],
         "usesInStr": true,
         "allowError": true
       }
     ]
   }
 }

Three top-level keys are required. ``testDir`` is the directory holding the packages. ``testedExecutablePaths`` maps a label to a binary; the label is what prints in the ``Running executable:`` header, and several may be listed to run the suite against more than one compiler. ``toolchains`` maps a name to the list of steps a test passes through.

Within a step:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Key
     - Meaning
   * - ``stepName``
     - Name shown when the step is the one that failed.
   * - ``executablePath``
     - Program to run. ``$EXE`` is the binary under test; ``$INPUT`` runs the previous step's output as a program.
   * - ``arguments``
     - Argument list. ``$INPUT`` is the test file for the first step and the previous step's output afterwards; ``$OUTPUT`` is the file named by this step's ``output``.
   * - ``output``
     - File this step writes, which becomes the next step's ``$INPUT``. Omit it and the step's stdout is piped through a temporary file instead.
   * - ``allowError``
     - Let this step exit non-zero without aborting the toolchain. Required for any suite containing error tests.
   * - ``usesInStr``
     - Feed the test's ``INPUT:`` text to this step's stdin. Set it on the step that runs the compiled program.

Environment variables are expanded from your shell, which is how ``$MLIR_INS/bin/lli`` above finds the LLVM installation. Paths are relative to the config file, so ``../bin/littlec`` refers to the project's ``bin`` directory rather than to wherever you happened to run the command.

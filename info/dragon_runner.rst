dragon-runner
=============

``dragon-runner`` is the test harness for every language project in the course. It feeds each test file through a *toolchain*: your compiler, then whatever runs the result. The final stdout is diffed against the expected output written inside the test file. Grading runs the same tool over the same configs.

Installation instructions are on the `setup pages <https://cmput415.github.io/415-docs/setup/>`_. The source lives at `cmput415/Dragon-Runner <https://github.com/cmput415/Dragon-Runner>`_.

Running the tester
------------------

.. code-block:: console

 $ dragon-runner [mode] <config>.json [options]

The mode defaults to ``regular``; the graders use the others (``tournament``, ``perf``, ``memcheck``). ``dragon-runner --help`` lists every option; these four cover ordinary use:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Option
     - Effect
   * - ``-v``
     - Print expected and generated output for each failure. Without it a failure is a bare ``[FAIL]`` line.
   * - ``-p PATTERN``
     - Run only the packages whose path matches the glob, e.g. ``-p '*arrays*'``.
   * - ``--debug-package PATH``
     - Run one package, named by its path.
   * - ``--timeout SECONDS``
     - Per-test timeout. The default is 2 seconds, which a debug build can exceed on a heavy test.

Paths inside the config resolve against the config file, so the command works from any directory:

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

A step may exit non-zero only if its config entry sets ``allowError``; otherwise the failure aborts the toolchain. The diff for an error test is lenient: dragon-runner matches on an error name such as ``SizeError`` or ``IndexError`` appearing in both the expected and the generated text.

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

``INPUT:`` supplies stdin. This C test reads two characters and echoes them:

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

Files ending in ``.out`` and ``.ins`` hold ``CHECK_FILE``/``INPUT_FILE`` payloads, and dot-files are skipped. dragon-runner treats every other file in a test directory as a test, whatever its extension.

Directory structure
-------------------

Each top-level directory under ``testDir`` is a *package*; every directory beneath a package holding at least one test is a *subpackage*, at any depth. A package is the unit of submission, and takes its name from your team ID or SID; subpackages group tests by feature.

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

``tests/littleCConfig.json`` from the littleC solution defines a two-step toolchain: the compiler under test emits an LLVM IR file, then ``lli`` interprets it.

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

Three top-level keys are required. ``testDir`` is the directory holding the packages. ``testedExecutablePaths`` maps a label to a binary; the label prints in the ``Running executable:`` header, and listing several runs the suite against each in turn. ``toolchains`` maps a name to the list of steps a test passes through.

Within a step:

.. list-table::
   :header-rows: 1
   :widths: 25 75

   * - Key
     - Meaning
   * - ``stepName``
     - Name printed when this step is the one that fails.
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

Environment variables come from your shell, which is how ``$MLIR_INS/bin/lli`` above finds the LLVM installation. The config sits in ``tests/``, so its relative paths resolve from there: ``../bin/littlec`` is the project's ``bin`` directory and ``testfiles`` is ``tests/testfiles``.

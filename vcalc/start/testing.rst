Testing
=======

.. _testing_tool:

Testing Tool
------------

Inside the ``tests`` directory, a testing configuration file,
``VCalcConfig.json``, is provided. You need to edit
``inDir`` with the absolute path of ``…/tests/input``, ``outDir`` with
the absolute path of ``…/tests/output``, ``testedExecutablePaths`` with 
your ccid and the absolute path of ``…/bin/vcalc``, and finally ``runtimes``
with your ccid and the absolute path of ``…/bin/libvcalcrt.so``

Running the tester should now run your tests with your solution. Note
that the output files will not be cleaned up so it might be wise run
your tests in a directory that is not your repository. If you would
still like to run them in the same directory, just know that the output
files do not need to be tracked by git and can be safely deleted.

::

     tester <path_to_config>

For more information about the testing tool and how it works, see the
`Tester
README <https://github.com/cmput415/Tester/blob/master/README.md>`__.


Generating Test Cases
---------------------

.. todo:: Put Fuzzer onto cmput415 GitHub.

A `Python script <https://github.com/Icohedron/VCalcFuzzer-release>`__ ``fuzzer.py`` is 
available for automatic generation of random test cases.

More information is available in the README file included with the script,
but an example usage of the script is as follows:

::

     python fuzzer.py config.json test

The above command will generate two files: ``test.in`` and ``test.out``, where
``test.in`` contains the VCalc source code of the test case and ``test.out``
contains the expected output. These files can be placed in your ``tests`` 
directory for use with the :ref:`testing_tool`.

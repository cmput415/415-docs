Testing
=======

.. _testing_tool:

Testing Tool
------------

Inside the ``tests`` directory, a testing configuration file,
``SCalcConfigInterpreterOnly.json``, is provided. You need to edit
``inDir`` with the absolute path of ``…/tests/input``, ``outDir`` with
the absolute path of ``…/tests/output``, and finally
``testedExecutablePaths`` with your ccid and the absolute path of
``…/bin/scalc``.

This configuration will run *only your interpreter* and can be run on
your local machine.

Another configuration is provided in ``SCalcConfigCS.json``. This is for
use on the machines in CSC either by being physically logged on or via
ssh. Again, you need to edit ``inDir`` with the absolute path of
``…/tests/input``, ``outDir`` with the absolute path of
``…/tests/output``, and finally ``testedExecutablePaths`` with your ccid
and the absolute path of ``…/bin/scalc``.

This configuration will run the *RISC-V, x86, ARM, and interpreter*
configurations of your compiler against all of your tests.

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

If you feel like running the full configuration (or a larger partial
configuration) you’ll first need to install the extra tools yourself and
then understand how to pull the relevant parts out of the full
configuration (binary path changes may be needed, arguments should be
the same).


Generating Test Cases
---------------------

A `Python script <../_static/SCalcFuzzer.tar.gz>`__ ``fuzzer.py`` is 
available for automatic generation of random test cases.

More information is available in the README file included with the script,
but an example usage of the script is as follows:

::

     python fuzzer.py config.json test

The above command will generate two files: ``test.in`` and ``test.out``, where
``test.in`` contains the SCalc source code of the test case and ``test.out``
contains the expected output. These files can be placed in your ``tests`` 
directory for use with the :ref:`testing_tool`.

On the CSC Lab Computers, the fuzzer is located in the directory 
``/cshome/cmput415/415-resources/fuzzers/SCalc``. Be sure to use ``python3``
when running fuzzers on the CSC Lab Computers.

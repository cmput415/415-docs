Testing
================

Local Testing
----------------
In each base repository there exists a `test` directory which contains a default JSON config and a `testfiles`
directory to put your tests. The default executable paths in the config should be updated to your local environment.
For more information on the 415 tester see `here <https://github.com/cmput415/Dragon-Runner>`_.

Test Submission Guidelines 
---------------------------

* A minimum of five tests must be used for submission. If less than five are submitted, empty tests will inserted in
  their absence.

* It is good practice to make *feature tests* -- tests for a specific feature of the language being implemented, and 
  name each test accordingly.

* Tests which attempt to cause failure through brute force (excessive loop bounds, memory allocation etc) are discouraged.
  During grading a timeout will be used. Exceeding this timeout creates the risk of failing your own tests. Instead, focus on tricky language constructs, interactions and edge cases that others are less likely to notice. 

* Procedurally generated tests, including fuzzer tests, are not allowed for submission. Competitive tests should be hand written.

*  The structure shuold look like the following. Anything below the ``<TEAM-ID/SID>`` directory will be included. ::

    └── tests
        └── testfiles
            └── <TEAM-ID/SID>
                ├── test1.in
                ├── test1.out
                    ...
                |
                ├── package-1
                    ... 
                └── package-N

* Example: In VCalc, if your repository is called ``vcalc-my-cool-team``, then your tests should be in ``tests/testfiles/my-cool-team``.

* Example: In Generator if your SID is 1660000, then a directory named ``tests/testfiles/160000`` should be present. Following this convention
  is important for the grader to be able to match your tests to your executable.
  
* Other tests which break these guidelines don't need to be thrown away! Simply keep them in another test package adjacent to your
  submitted package. There they can be used as local regression tests. For example, it's common to keep a corpus of difficult fuzzer tests
  and simpler tests that are not expected to yield high competative scores.

Competitive Testing
------------------------------
* Each submission should include a test-suite. To reiterate the submission guidelines above:

  * Your submitted tests should be feature-tests.
  * You should submit a minimum of 5 tests in your test-suite. 
  * You should name all of your tests according to the feature they test.
  * You should not submit multiple tests that test the same feature.
  * You should not submit tests created by a fuzzer.

* Your competitive testing grade will be determined by a tournament.

  * In this tournament, submissions earn points based on the performance of their submitted compiler and
    test-suite. Each submitted compiler will be run on each submitted test-suite. Consider two distinct
    submissions, submission-A and submission-B. submission-A earns points as follows:

    * **Coherence Points:** if compiler-A passes every test in test-suite-A, submission-A earns 1 point.
    * **Defensive Points:** if compiler-A passes N test in test-suite-B of size M, submission-A earns N/M points.
    * **Offensive Points:** if compiler-B fails N tests in tests-A, submission-A earns N / (number of
      tests in test-suite-A) points.

  * Your competitive testing grade is computed by dividing your submission's tournament score by the
    highest tournament score earned by a submission for that assignment in this term. For example, if your
    submission earned 30.0 tournament points and the other submissions in the class earned 24.3, 40.0, and
    15.9 tournament points, you will receive a competitive testing grade of 75%.

* In the past, there was a minor penalty for submitting tests that did not adhere to the unit-testing
  practice. So, clever students submitted test-suites with a few large test cases each including many
  features thus making it more likely that a compiler would fail the test cases. Their intent was to
  offset the penalty with the offensive points they earn and the defensive points they prevent other
  students from receiving. To prevent this from happening again and to incentivize students to practice
  writing good unit-tests, the TA can exclude tests that they think are not good unit-tests. If the TA
  excludes several tests from a submission and believes that the students intentionally created bad
  unit-tests to abuse competitive testing, they may receive a competitive testing grade of 0%.

Performance Testing
------------------------------

* Your performance testing grade will be determined by the speed of your produced binaries over a set of
  pre-selected Gazprea programs. Specifically, the LLVM IR emitted by your compiler will be fed into an
  optimization pipeline and `dragon-runner` will trace how long your executable takes.

* Performance grades are relative. The compiler to produce the fastest executable for a given program gets
  a score of 1. Every other compiler gets a score corresponding to the ratio of the fastest time and its
  own time. For example if compiler A generates the fastest executable at 3s and your executable can run
  it in 5s, your score is 3/5, while team A gets 1.

* Your total timing score is the mean of scores for each timing program.

* If your compiler fails to produce the expected output, you recieve the max-timeout for the tournament which
  is set by the grader. (May be 5s to 10s depending on the machine.)

* Compilers that emit well thought out, clean IR should be ammenible to the greatest optimization speedup.
  Those which rely heavily on the runtime may find their executables slower due to a reduced optimization surface
  and the high overhead of runtime function calls. 

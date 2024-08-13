Testing
================

Local Testing
----------------

In each base repository you will find a `test` directory which contains a default JSON config and a `testfiles`
directory to put your tests. The default executable paths in the config should be updated to your local environtment.
For more information on the 415 tester see `here <https://github.com/cmput415/Tester>`_.

Competative Testing
----------------
* Each submission should include a test-suite.

  * Your submitted tests should be unit-tests. Each test should be written to test a particular feature
    and use a minimal subset of the language.
  * You should submit a minimum of 5 tests in your test-suite. If you submit fewer than 5 tests or some of
    your tests are removed for any reason, the TA will add empty tests to your test-suite until it
    contains at least 5 tests.
  * You should name all of your tests according to the feature they test.
  * You should not submit multiple tests that test the same feature.
  * You should not submit tests created by a fuzzer.

* Your competitive testing grade will be determined by a tournament.

  * In this tournament, submissions earn points based on the performance of their submitted compiler and
    test-suite. Each submitted compiler will be run on each submitted test-suite. Consider two distinct
    submissions, submission-A and submission-B. submission-A earns points as follows:

    * **Coherence Points:** if compiler-A passes every test in test-suite-A, submission-A earns 1 point.
    * **Defensive Points:** if compiler-A passes every test in test-suite-B, submission-A earns 2 points.
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

Execution Timing Testing
----------------

* Over a selected set of Gazprea programs, the LLVM IR emitted by each compiler will be fed into an
  optimization pipeline. The 415 tester will trace how long your executable takes to run.

* The fastest executable for a given program gets a score of 1. Every other executable gets the ratio
  between the fastest time and their own time. For example if compiler A generates the fastest
  executable at 3s and your executable can run it in 5s, your score is 3/5, while team A gets 5/5.

* Your total timing score is the mean of individual scores for each timing program.

* If your compiler fails to produce the expected output, you recieve the max-timeout for the tournament which
  is set by the grader. (May be 5s to 10s depending on the machine.)

* Compilers that emit well thought out, clean IR should be ammenible to the greatest optimization speedup.
  Those which rely heavily on the runtime may find their executables slower due to a reduced optimization surface
  and the high overhead of runtime function calls. 
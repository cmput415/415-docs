.. _sec:gazprea_process:

Project Management
==================

Gazprea is written by four people in one repository. This page describes how to run that on GitHub.

Best practices
--------------

Deliver every change through a pull request:

#. Branch from the default branch.
#. Commit your work to the branch and push it.
#. Open a pull request against the default branch.
#. A teammate who did not write it reviews and approves it.
#. Merge, and delete the branch.

Keep a pull request small enough that a teammate can read it in one sitting.

Track the work in issues:

* Open an issue for each piece of work you have identified. Specification sections you have not implemented yet and test packages that are failing both divide cleanly into issues.
* **Assign every issue to the member doing it**, and reassign it if the work changes hands.
* Close issues as the work lands.

If your repository has no **Issues** tab, contact a TA. The tracker is disabled by default and only the teaching team can turn it on.

Marks
-----

Project management is marked at Part 1 and again at Part 2. The lines and what each is worth are under :external+info:ref:`Gazprea project management marks <sec:gazprea_pm_marks>`.

Enforcing them
--------------

You can enforce some of these rules with repository rulesets. Consider configuring them for your team's repo.

`Creating rulesets for a repository <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository>`_ covers creating one under Settings → Rules → Rulesets, and `Available rules for rulesets <https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets>`_ describes the rules you can choose from.

Creating or editing a ruleset requires repository **admin**. If you do not have admin permissions on your repo, contact a TA.

.. warning::
   A ruleset applies to everyone it does not explicitly exempt, so it is possible to lock your own team out of your own default branch. Undoing that requires an organisation owner, so contact a TA rather than trying to recover it yourselves.

.. note::
   © 2024-2026 University of Alberta. All rights reserved.

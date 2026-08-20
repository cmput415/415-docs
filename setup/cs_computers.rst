CS Lab Machines
===============

The lab machines in UCOMM 2-070 and 2-086 are the reference environment for this course. Every toolchain the projects need is already installed and maintained there, and it is the environment the lab exams are written in. **Working on a lab machine is the recommended way to do the projects**, whether you sit down at one in the lab or log in to one remotely.

.. todo::

   Confirm the fully-qualified domain for the lab machines before publishing. The names below assume ``<host>.cs.ualberta.ca``.

Why the lab machines
--------------------

Lab exams are written in person, at a lab machine, in a one-hour block. The environment you get on exam day is the lab machine environment — its compiler, its CMake, its editors, its keyboard shortcuts, its window manager. Time spent that day discovering that your editor is not installed, that your build flags differ, or that your shell configuration lives only on your laptop is time taken out of the exam.

The way to avoid that is to make the lab machine the environment you already work in, so that exam day is an ordinary working session in a familiar place.

The lab machines are also the machines your submissions are built and graded on. Code that builds on your laptop and not on a lab machine scores what it scores on a lab machine.

Choosing a machine
------------------

There are 59 machines across the two lab rooms:

===============  ===============================================  =====
Room             Hostnames                                        Count
===============  ===============================================  =====
UCOMM 2-070      ``ucomm-2070-w00`` – ``ucomm-2070-w24``          25
UCOMM 2-086      ``ucomm-2086-w00`` – ``ucomm-2086-w33``          34
===============  ===============================================  =====

Remote logins are not load balanced, so pick your machine from your student ID rather than picking a low number that everyone else also picks. Take your student ID modulo 59:

.. code-block:: console

 $ echo $(( <your student ID> % 59 ))

If the result is 0–24, your machine is ``ucomm-2070-w<result>``; if it is 25–58, your machine is ``ucomm-2086-w<result minus 25>``. Hostnames pad the number to two digits, so a result of 7 is ``ucomm-2070-w07``.

Nothing binds you to that machine — it is a starting point that spreads the class out. If yours is unreachable or heavily loaded, move to another one. Your files live in ``/cshome``, which is shared across every CS machine, so your work follows you.

Logging in over SSH
-------------------

A terminal session is enough for the whole build-test-debug cycle: ``cmake``, ``ninja``, ``dragon-runner``, ``git``, and a terminal editor.

.. code-block:: console

 $ ssh <ccid>@ucomm-2070-w07.cs.ualberta.ca

The first connection asks you to confirm the host key. After that you are at a shell on the lab machine.

Two things make this much more pleasant, and both are worth setting up now rather than during an exam week:

**Key-based login.** Generate a key on your own machine and copy the public half to the lab machine, and you stop typing your password on every connection:

.. code-block:: console

 $ ssh-keygen -t ed25519
 $ ssh-copy-id <ccid>@ucomm-2070-w07.cs.ualberta.ca

**A host alias.** Put an entry in ``~/.ssh/config`` on your own machine so that ``ssh lab`` is the whole command:

.. code-block:: none

 Host lab
     HostName ucomm-2070-w07.cs.ualberta.ca
     User <ccid>
     ServerAliveInterval 60

**Sessions that survive a dropped connection.** A build or a test run dies with your SSH session if the network hiccups. Start your work inside ``tmux`` and it keeps running:

.. code-block:: console

 $ tmux new -s c415      # start a session
 $ tmux attach -t c415   # reattach to it later, from anywhere

Graphical sessions with X2Go
----------------------------

If you want a graphical desktop on the lab machine — CLion, a file manager, a browser for the local documentation — use `X2Go <https://wiki.x2go.org/doku.php>`__. It gives you the lab machine's desktop in a window on your own machine, and it is far more usable over a home connection than plain X11 forwarding.

#. Install the X2Go client on your own machine. On Ubuntu, ``sudo apt-get install x2goclient``; on macOS and Windows, download it from the `X2Go client page <https://wiki.x2go.org/doku.php/doc:installation:x2goclient>`__.

#. Create a session with these settings:

   * **Host:** your lab machine, e.g. ``ucomm-2070-w07.cs.ualberta.ca``
   * **Login:** your CCID
   * **Session type:** the desktop environment the lab machines run

#. Connect. You get the same desktop you would get sitting at the machine.

X2Go sessions can be suspended and resumed, so you can disconnect, move, and pick up the same desktop with your editor and terminals where you left them.

X11 forwarding (``ssh -X``) also works for a single graphical program, but it is slow over anything other than a campus connection.

Setting up your environment
---------------------------

Setup on the lab machines is much simpler than on your own machine, because the compiler, CMake, Java, ANTLR, LLVM, MLIR, and ``dragon-runner`` are all installed and maintained for you. All you need to do is add the provided definitions to your ``~/.bashrc``.

.. code-block:: shell

     # C415 Predefinitions
     source "/cshome/cmput415/415-resources/415env.sh"

This puts the course toolchain on your path and lets you build from the command line. Log out and back in so that the changes take effect.

Because ``/cshome`` is shared, this is a one-time step: your shell configuration, your dotfiles, and your editor configuration are the same on every lab machine you log in to, including the one you are assigned on exam day.

Installing CLion
----------------

#. Go to the `download page
   <https://www.jetbrains.com/clion/download/#section=linux>`__ and download
   *CLion* for Linux.

#. Assuming you've downloaded the tarball to your ``~/Downloads`` folder, you
   can extract it to
   your home directory
   using the following command:

   .. code-block:: console

    $ tar -xzf ~/Downloads/clion-<version>.tar.gz -C ~

   If you are confident about your ability to setup your own install you can put
   it elsewhere but you will be on your own.

#. From now on, you can start *CLion* by using the following command:

   .. code-block:: console

    $ ~/clion-<version>/bin/clion.sh

#. Perform the initial set up of CLion.

   #. Select ``Do not import settings`` and click ``OK``.

   #. Scroll to the bottom of the license agreement then hit ``Accept``.

   #. Choose if you want to share usage statistics.

   #. You should be presented with a prompt for your license. Select
      ``Activate CLion``, ``JB Account``, click
      ``Log In to JetBrains Account...`` and enter your UAlberta email address
      and JetBrains account password. Click the ``Activate`` button.

   #. Pick your favorite UI. Then click ``Next: Toolchains``.

   #. Click ``Next: Default Plugins``.

   #. You might consider disabling all but the git plugin, and even then, using
      it is up to you. It can be useful to see the color coded files for
      differences at a glance or track changes in a file. You should consider
      disabling all of the web development plugins. Disabling other tools is up
      to you as well. Now select ``Next: Feature Plugins``

   #. Again, the choices here are yours. If you like vim, then maybe the vim
      plugin is up your alley. The markdown plugin can be useful as well. You do
      not need the TeamCity Integration, the Lua integration, nor the Swift
      integration. Select ``Start using CLion``

Because CLion is installed into your ``/cshome`` directory, it is there on every lab machine once you have installed it once. Launch it from an X2Go session; over plain SSH there is no display to put it on.

Checking that you are ready
---------------------------

You are ready for an exam week when all of the following are true on a lab machine you have not used before:

* You can log in, at the machine and over SSH.
* ``which cmake ninja java`` and ``dragon-runner --help`` all work in a fresh shell.
* Your editor of choice starts and has the configuration you expect.
* You can clone one of your project repositories from GitHub and build it.

Work through that list early in the term. Every item on it is quick to fix in week two and expensive to discover in an exam.

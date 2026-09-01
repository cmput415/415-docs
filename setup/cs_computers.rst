CS Lab Machines
===============

The lab machines in UCOMM 2-070 and 2-086 are the reference environment for this course. Every toolchain the projects need is already installed and maintained there, and it is the environment the lab exams are written in. **Working on a lab machine is the recommended way to do the projects**, whether you sit down at one in the lab or log in to one remotely.

They run Ubuntu 20.04 LTS with the Xfce desktop. ``vim``, ``emacs``, ``nano``, ``gedit``, and Visual Studio Code (``code``) are installed.

Why the lab machines
--------------------

Lab exams are written in person, at a lab machine, in a one-hour block. The environment you get on exam day is the lab machine environment — its compiler, its CMake, its editors, its keyboard shortcuts, its window manager. You do not want to discover on exam day that your editor is configured incorrectly or you have been using a different version of MLIR.

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

Remote logins are not load balanced, so pick your machine from your student ID rather than picking a low number that everyone else also picks. Substitute your student ID and run:

.. code-block:: console

 $ n=$(( <your student ID> % 59 )); [ $n -lt 25 ] && printf 'ucomm-2070-w%02d\n' $n || printf 'ucomm-2086-w%02d\n' $(( n - 25 ))

That prints the hostname of your machine: the first 25 numbers land in UCOMM 2-070 and the rest in UCOMM 2-086.

Nothing binds you to that machine — it is a starting point that spreads the class out. If yours is unreachable or heavily loaded, move to another one. Your files live in ``/cshome``, which is shared across every CS machine, so your work follows you.

Logging in over SSH
-------------------

A terminal session is enough for the whole build-test-debug cycle: ``cmake``, ``make``, ``dragon-runner``, ``git``, and a terminal editor.

If you prefer to work with a GUI and an IDE, skip to `Graphical sessions with X2Go`_.

The lab machines do not accept connections from outside the department network, so you reach them through the CS SSH gateway, ``innisfree.cs.ualberta.ca``. Connecting straight to a lab machine times out; ``-J`` makes the jump for you in one command:

.. code-block:: console

 $ ssh -J <ccid>@innisfree.cs.ualberta.ca <ccid>@ucomm-2070-w07.cs.ualberta.ca

The first connection asks you to confirm the host key of each host in turn. After that you are at a shell on the lab machine.

For your convenience, you can set this up nicely:

**A host alias.** Put these entries in ``~/.ssh/config`` on your own machine and the whole command becomes ``ssh lab``:

.. code-block:: none

 Host innis
     HostName innisfree.cs.ualberta.ca
     User <ccid>

 Host lab
     HostName ucomm-2070-w07.cs.ualberta.ca
     User <ccid>
     ProxyJump innis
     ServerAliveInterval 60

``ServerAliveInterval`` keeps the connection from being dropped while you are reading rather than typing.

**Key-based login.** Generate a key on your own machine and copy the public half to the gateway and the lab machine, and you stop typing your password twice on every connection:

.. code-block:: console

 $ ssh-keygen -t ed25519
 $ ssh-copy-id innis
 $ ssh-copy-id lab

**Sessions that survive a dropped connection.** A build or a test run dies with your SSH session if the network hiccups. Start your work inside ``tmux`` and it keeps running:

.. code-block:: console

 $ tmux new -s c415      # start a session
 $ tmux attach -t c415   # reattach to it later, from anywhere

Graphical sessions with X2Go
----------------------------

If you want a graphical desktop on the lab machine — a graphical editor, a file manager, a browser for the local documentation — use `X2Go <https://wiki.x2go.org/doku.php>`__. It gives you the lab machine's desktop in a window on your own machine, and it is far more usable over a home connection than plain X11 forwarding.

#. Install the X2Go client on your own machine. On Ubuntu, ``sudo apt-get install x2goclient``; on macOS and Windows, download it from the `X2Go client page <https://wiki.x2go.org/doku.php/doc:installation:x2goclient>`__.

#. Create a session. Under **Session**:

   * **Host:** your lab machine, e.g. ``ucomm-2070-w07.cs.ualberta.ca``
   * **Login:** your CCID
   * **Session type:** ``XFCE``

#. The gateway applies here too. Still under **Session**, tick **Use Proxy server for SSH connection**, set the proxy type to ``SSH``, and give it ``innisfree.cs.ualberta.ca`` on port 22 with your CCID.

#. Connect. You get an Xfce desktop on the lab machine.

X2Go sessions can be suspended and resumed, so you can disconnect, move, and pick up the same desktop with your editor and terminals where you left them.

The department publishes its own `X2Go Quick Guide <https://www.ualberta.ca/en/computing-science/resources/technical-support/computing-resources/x2go-quick-guide.html>`__ covering the same setup.

X11 forwarding (``ssh -X``, adding ``-X`` to the jump command above) also works for a single graphical program, but it is slow over anything other than a campus connection.

Setting up your environment
---------------------------

Setup on the lab machines is much simpler than on your own machine, because the compiler, CMake, Java, ANTLR, LLVM, MLIR, and ``dragon-runner`` are all installed and maintained for you. All you need to do is add the provided definitions to your ``~/.bashrc``.

.. code-block:: shell

     # C415 Predefinitions
     source "/cshome/cmput415/415-resources/415env.sh"

This puts the course toolchain on your path and lets you build from the command line. Log out and back in so that the changes take effect.

Because ``/cshome`` is shared, this is a one-time step: your shell configuration, your dotfiles, and your editor configuration are the same on every lab machine you log in to, including the one you are assigned on exam day.

A graphical IDE
---------------

Visual Studio Code is installed on the lab machines and is the recommended graphical editor for the course. Launch it from an X2Go session with:

.. code-block:: console

 $ code

Its settings and extensions live in ``~/.config/Code`` and ``~/.vscode`` under ``/cshome``, so whatever you configure follows you to every lab machine, including the one you are assigned on exam day.

Two extensions cover the projects: **C/C++** (``ms-vscode.cpptools``) for C++ editing and debugging, and **CMake Tools** (``ms-vscode.cmake-tools``) for configuring and building from the editor. Install them from the Extensions panel.

Over plain SSH there is no display to put a graphical editor on, so use a terminal editor or connect with X2Go.


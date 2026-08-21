CMPUT 415 Setup Instructions
============================

These instructions are for setting up your development environment for CMPUT 415.

**The recommended environment is a CS lab machine**, either sitting at one in UCOMM 2-070 or 2-086 or logged in remotely over SSH or X2Go. The toolchain is already installed and maintained there, your submissions are built and graded there, and the lab exams are written there. :doc:`CS Lab Machines <cs_computers>` covers connecting to one and the small amount of setup it needs.

Working remotely needs a connection you can rely on, and there are good reasons you might not have one — an unstable link, a long commute, or work you want to do offline. Developing locally is a legitimate choice, and the Ubuntu and macOS chapters tell you how to set it up. Two warnings come with it.

The first is that your local machine is not what your work is judged on. Submissions are built and graded on a lab machine, which runs Ubuntu 20.04 LTS with a fixed toolchain, so build there regularly rather than discovering the difference at a deadline.

The second is that a lab exam is written at a lab machine, in a fixed hour, with no time to install or configure anything. Whatever editor, shell configuration, and habits you rely on have to already exist there. Setting that up is quick in week two and impossible during an exam, so do it early even if you spend most of the term working locally.

Start with "First Steps". Then read "CS Lab Machines", and afterwards the chapter for your own operating system if you intend to work locally as well.

.. toctree::
   :numbered:

   self
   first_steps
   cs_computers
   ubuntu
   macos
   windows

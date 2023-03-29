#################################
PyPasswordManager's Documentation
#################################

Introduction
============
This is a **lightweight** and **minimalist** application for
demonstration purposes. It is a console password manager scripted in
Python, with full password encryption using modern algorithms. It
currently supports user creation, password adding and password deleting.

Installation and Usage
======================
Download the source code and install using pip, after that simply run
**pypasswordmanager** in the terminal.

Making of the app
=================
The app uses, besides its own, only modules from the Python standard
libraries. The ``os`` module is used for path functions and random salt
generation, while the ``cryptography`` module is used for the, well,
cryptography functions. The app is based solely on functional programming,
aiming at simplicity and efficiency.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. toctree::
   :maxdepth: 2
   :caption: Modules

   main_doc
   login_doc
   ops_doc
   crypto_doc

When making changes to the documents always build, check for errors then check
the finished html and pdf changes.

To install sphinx
sudo apt install python3-sphinx

In this directory open a terminal

To build the html
make html

To build the pdf
make latexpdf

Links
See the :doc:`some_file_name` for more information.

When using :ref: to link to a specific section, you need to define a label
immediately before the section title in the target document.

.. _my-section-label:

My Section Title
^^^^^^^^^^^^^^^^

See :ref:`my-section-label`.


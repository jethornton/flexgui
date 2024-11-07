Installing
==========
`Installing Flex GUI Tutorial <https://youtu.be/F8mCt7JJDDM>`_

Download the latest deb file from
`>HERE< <https://github.com/jethornton/flexgui/releases>`_.

If the link is not clickable, copy and paste the following URL into your
browser
::

	https://github.com/jethornton/flexgui/releases

~amd64.deb is for PC's and ~arm64.deb is for Raspberri Pi.

Select the latest release and click on the .deb to start a download.

Install with Gdebi from the file manager. If Gdebi is not installed, open a
terminal and run this command to install it:
::

	sudo apt install gdebi

An alternative is to install from the terminal outright using `dpkg`:
::

	sudo dpkg -i flexgui_1.0.0_amd64.deb

After installing Flex GUI, a menu item `Copy Flex Examples` is added to the
`CNC` menu. This will copy the Flex GUI example files to
~/linuxcnc/configs/`flex_examples`.

.. note:: After updating the Flex GUI some examples may have changed. To get a
   fresh copy of the examples delete the `linuxcnc/configs/flex_examples` or
   rename it.

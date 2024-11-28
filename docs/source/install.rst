Installing
==========

Install with apt
----------------

The advantage of using apt to install Flex GUI is when the repo is updated apt
will know when the version changes and you can install the new version along
with other Debian software.

For a PC create an apt sources file for Flex copy and paste this command in a
terminal
::

	echo 'deb [arch=amd64] https://gnipsel.com/flexgui/apt-repo stable main' | sudo tee /etc/apt/sources.list.d/flexgui.list

For a Raspberry Pi create an apt sources file for Flex copy and paste this command in a
terminal
::

	echo 'deb [arch=arm64] https://gnipsel.com/flexgui/apt-repo stable main' | sudo tee /etc/apt/sources.list.d/flexgui.list

Next get the public key for Flex GUI and copy it to trusted.gpg
::

	sudo curl --silent --show-error https://gnipsel.com/flexgui/apt-repo/pgp-key.public -o /etc/apt/trusted.gpg.d/flexgui.asc

Next update apt
::

	sudo apt update

If you have Flex GUI installed you can see what packages can be upgraded with
the following command
::

	apt list --upgradable

If Flex GUI is not installed you can install it with the following command
::

	sudo apt install flexgui

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

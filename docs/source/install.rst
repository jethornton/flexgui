Installing
==========

Install with apt
----------------

The advantage of using apt to install Flex GUI is when a new version of Flex GUI
is released apt will know a new version is avaliable when you run 
`sudo apt update`. This will allow you to install the new version of Flex GUI
along with other Debian software.

The first command will ask for your password. Neither command will print
anything in the terminal.

For a PC to create an apt sources file for Flex GUI copy and paste this command
in a terminal
::

	echo 'deb [arch=amd64] https://gnipsel.com/flexgui/apt-repo stable main' | sudo tee /etc/apt/sources.list.d/flexgui.list

For a Raspberry Pi create an apt sources file for Flex GUI copy and paste this
command in a terminal
::

	echo 'deb [arch=arm64] https://gnipsel.com/flexgui/apt-repo stable main' | sudo tee /etc/apt/sources.list.d/flexgui.list

To check the above command worked you can list the file with this command
::

	ls /etc/apt/sources.list.d

.. image:: /images/install-02.png
   :align: center


Next get the public key for Flex GUI and copy it to trusted.gpg.d
::

	sudo curl --silent --show-error https://gnipsel.com/flexgui/apt-repo/pgp-key.public -o /etc/apt/trusted.gpg.d/flexgui.asc

If curl is not installed you can install it with the following command
::

	sudo apt install curl

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

Install the deb
---------------

You can still download the deb from github and install with gdebi if that works
better for you. If you don't have an internet connection this is the best way to
install Flex GUI

`Installing Flex GUI Tutorial <https://youtu.be/F8mCt7JJDDM>`_

Download the latest deb file from
`>HERE< <https://github.com/jethornton/flexgui/releases>`_.

If the link is not clickable, copy and paste the following URL into your
browser
::

	https://github.com/jethornton/flexgui/releases

~amd64.deb is for PC's and ~arm64.deb is for Raspberri Pi.

Select the latest release and click on the .deb to start a download.

Right click on the deb file and select `Open with GDebi Package Installer`.
If that option is not there then GDebi is not installed, open a terminal and run
this command to install it:
::

	sudo apt install gdebi

An alternative is to install from the terminal outright using `dpkg`. Make sure
the version number is correct for the deb you have the following command may be
an older version.
::

	sudo dpkg -i flexgui_1.1.0_amd64.deb

After installing Flex GUI, a menu item `Copy Flex Examples` is added to the
`CNC` menu. This will copy the Flex GUI example files to
~/linuxcnc/configs/`flex_examples`.

.. note:: After updating the Flex GUI some examples may have changed. To get a
   fresh copy of the examples delete the `linuxcnc/configs/flex_examples` or
   rename it.

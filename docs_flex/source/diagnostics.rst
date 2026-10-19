=====================
Diagnostics and Tools
=====================

Raspberry Pi 5
--------------

To add the SMP PREEMPT_RT kernel it's easier than ever starting with Linux
kernel version 6.12, the PREEMPT_RT patch is fully integrated into the mainline
code for ARM64 architecture, making it significantly easier to set up.

Back up any critical data on your SD card or SSD before running experimental
updates.

Open your terminal and run the update command explicitly requesting the 64-bit
RT branch:

.. code-block:: text

	sudo WANT_64BIT_RT=1 rpi-update rpi-6.12.y

Reboot your Raspberry Pi 5

To activate the PREEMPT_RT kernel you just downloaded, follow these steps to
update your boot configuration:

Open your system's boot configuration file:

.. code-block:: text

	sudo nano /boot/firmware/config.txt

Scroll to the end of the file or look under the [all] section and add the following lines:

.. code-block:: text

	kernel=kernel8_rt.img
	auto_initramfs=0

Press Ctrl + O then Enter to save, then Ctrl + X to exit the editor.

.. Note:: Disabling auto_initramfs ensures the system loads the raw RT image
   directly without trying to wrap a standard non-RT ramdisk around it

Restart your Raspberry Pi to apply the configuration

.. code-block:: text

	sudo reboot

Once the system comes back up, run the verification command

.. code-block:: text

	uname -a

You should now see the line include `SMP PREEMPT_RT`, confirming that the
real-time kernel is active!


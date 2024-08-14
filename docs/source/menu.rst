Menu
====

.. note:: Every menu item has a command button so you don't need to use any
   menu items if you don't want to.

Adding a menu items creates an action. When you create File > Open menu the
`actionOpen` action is created.

.. image:: /images/menu-01.png
   :align: center

.. warning:: If you use the full screen option you will not be able to exit the application
   if you don't have the Exit action or an Exit Push Button.

.. code-block:: text

 File                    Action Name
  Open                   actionOpen
  Edit                   actionEdit
  Reload                 actionReload
  Save As                actionSave_As
  Edit Tool Table        actionEdit_Tool_Table
  Reload Tool Table      actionReload_Tool_Table
  Ladder Editor          actionLadder_Editor
  Quit                   actionQuit

 Machine
  E Stop                 actionE_Stop
  Power                  action_Power
  Run                    actionRun
  Run From Line          actionRun_From_Line
  Step                   actionStep
  Pause                  actionPause
  Resume                 actionResume
  Stop                   actionStop
  Clear MDI History      actionClear_MDI_History
  Copy MDI History       actionCopy_MDI_History

 Programs
  Show HAL               actionShow_HAL
  HAL Meter              actionHAL_Meter
  HAL Scope              actionHAL_Scope

 View

 Help
  About                 actionAbout
  Quick Reference       actionQuick_Reference

Action Names
------------

When you add a menu item it creates an action and the Object Name is created
from the menu name when you add a menu item.

The Object Name must match the above items exactly in order to be discovered by
Flex GUI.

.. image:: /images/actions-01.png
   :align: center

Recent Files
------------

.. note:: The Recent menu item is added before the next action after actionOpen
   in the order of the Action Editor. There must be at least one action after
   actionOpen for the Recent menu to show up.

.. image:: /images/menu-02.png
   :align: center

Location of the Recent menu from the above action list

.. image:: /images/menu-03.png
   :align: center

Tool Bars
---------

If you right click on the main window you can add a Tool Bar.

.. image:: /images/tool-bar-01.png
   :align: center

To add actions to the Tool Bar drag them from the Action Editor and drop them in
the Tool Bar.

.. image:: /images/tool-bar-02.png
   :align: center

To set the style of a Tool Bar Button use the action name and replace action
with `flex_` for example the actionQuit would be `flex_Quit`
::

	QToolButton#flex_Quit:pressed {
		background-color: rgba(192, 0, 0, 80%); color: white; border none;
	}

Shortcut Keys
-------------

Shortcut keys can be added in the Property Editor by clicking in the shortcut
Value box and pressing the key or key combination you want to use. You can
change text, icon Text or tool Tip.

.. image:: /images/actions-02.png
   :align: center


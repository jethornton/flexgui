Menu
====

Adding a menu items creates an action. When you create File > Open menu the
`actionOpen` action is created.

.. image:: /images/menu-01.png
   :align: center


If you use the full screen option you will not be able to exit the application
if you don't have the actionExit action.

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

When you add a menu item it creates and action and names it based on the menu
name. The action names must match exactly the above items to be found.

.. image:: /images/actions-01.png
   :align: center


Shortcut Keys
-------------

Shortcut keys can be added in the Property Editor by clicking in the shortcut
Value box and pressing the key or key combination you want to use. You can
change text, icon Text or tool Tip but the objectName must match the above
Action Names in order to be `discovered` by Flex GUI.

.. image:: /images/actions-02.png
   :align: center


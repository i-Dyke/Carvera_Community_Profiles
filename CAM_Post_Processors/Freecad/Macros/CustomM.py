# -*- coding: utf-8 -*-
# ***************************************************************************
# *   Copyright (c) 2015 Dan Falck <ddfalck@gmail.com>                      *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************

"""Used for CNC machine code insertions for Path module. Based upon the Default STOP profile"""

import FreeCAD
import FreeCADGui
import Path
from PySide import QtCore
from PySide.QtCore import QT_TRANSLATE_NOOP

translate = FreeCAD.Qt.translate


class CommandM:
    def __init__(self, obj):
        obj.addProperty(
            "App::PropertyEnumeration",
            "Command",
            "Path",
            QT_TRANSLATE_NOOP("App::Property", "Select predefined command or use Extra Commands"),
        )
        obj.Command = ["Pause", "Air ON", "Air OFF", "Extra Commands"]
        obj.addProperty(
            "App::PropertyString",
            "ExtraCommands",
            "Path",
            QT_TRANSLATE_NOOP("App::Property", "Add custom M-code commands (e.g., M123 or M456 P1)"),
        )
        obj.ExtraCommands = ""
        obj.Proxy = self
        mode = 2
        obj.setEditorMode("Placement", mode)

    def dumps(self):
        return None

    def loads(self, state):
        return None

    def onChanged(self, obj, prop):
        pass

    def execute(self, obj):
        if obj.Command == "Pause":
            word = "M600"
        elif obj.Command == "Air ON":
            word = "M07"
        elif obj.Command == "Air OFF":
            word = "M09"
        elif obj.Command == "Extra Commands":
            word = obj.ExtraCommands if obj.ExtraCommands else ""
        else:
            word = ""

        output = ""
        if word:
            output = word + "\n"
        path = Path.Path(output)
        obj.Path = path


class _ViewProviderCommandM:
    def __init__(self, vobj):  # mandatory
        vobj.Proxy = self
        mode = 2
        vobj.setEditorMode("LineWidth", mode)
        vobj.setEditorMode("MarkerColor", mode)
        vobj.setEditorMode("NormalColor", mode)
        vobj.setEditorMode("DisplayMode", mode)
        vobj.setEditorMode("BoundingBox", mode)
        vobj.setEditorMode("Selectable", mode)
        vobj.setEditorMode("ShapeAppearance", mode)
        vobj.setEditorMode("Transparency", mode)
        vobj.setEditorMode("Visibility", mode)

    def dumps(self):  # mandatory
        return None

    def loads(self, state):  # mandatory
        return None

    def getIcon(self):  # optional
        return ":/icons/CAM_Stop.svg"

    def onChanged(self, vobj, prop):  # optional
        mode = 2
        vobj.setEditorMode("LineWidth", mode)
        vobj.setEditorMode("MarkerColor", mode)
        vobj.setEditorMode("NormalColor", mode)
        vobj.setEditorMode("DisplayMode", mode)
        vobj.setEditorMode("BoundingBox", mode)
        vobj.setEditorMode("Selectable", mode)
        vobj.setEditorMode("ShapeAppearance", mode)
        vobj.setEditorMode("Transparency", mode)
        vobj.setEditorMode("Visibility", mode)


class CommandPathCommandM:
    def GetResources(self):
        return {
            "Pixmap": "CAM_Stop",
            "MenuText": QT_TRANSLATE_NOOP("CAM_CommandM", "CommandM"),
            "ToolTip": QT_TRANSLATE_NOOP(
                "CAM_Command", "Add Custom Mcode Command to the program"
            ),
        }

    def IsActive(self):
        if FreeCAD.ActiveDocument is not None:
            for o in FreeCAD.ActiveDocument.Objects:
                if o.Name[:3] == "Job":
                    return True
        return False

    def Activated(self):
        FreeCAD.ActiveDocument.openTransaction("Add Custom Mcode Command to the program")
        FreeCADGui.addModule("Path.Op.Gui.CommandM")
        snippet = """
import Path
import PathScripts
from PathScripts import PathUtils
prjexists = False
obj = FreeCAD.ActiveDocument.addObject("Path::FeaturePython","CommandM")
Path.Op.Gui.CommandM.CommandM(obj)

Path.Op.Gui.CommandM._ViewProviderCommandM(obj.ViewObject)
PathUtils.addToJob(obj)
"""
        FreeCADGui.doCommand(snippet)
        FreeCAD.ActiveDocument.commitTransaction()
        FreeCAD.ActiveDocument.recompute()


if FreeCAD.GuiUp:
    # register the FreeCAD command
    FreeCADGui.addCommand("CAM_CommandM", CommandPathCommandM())


FreeCAD.Console.PrintLog("Loading PathCommandM... done\n")

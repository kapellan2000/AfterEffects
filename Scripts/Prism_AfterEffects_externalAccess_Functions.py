# -*- coding: utf-8 -*-
#
####################################################
#
# PRISM - Pipeline for animation and VFX projects
#
# www.prism-pipeline.com
#
# contact: contact@prism-pipeline.com
#
####################################################
#
#
# Copyright (C) 2016-2020 Richard Frangenberg
#
# Licensed under GNU GPL-3.0-or-later
#
# This file is part of Prism.
#
# Prism is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Prism is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Prism.  If not, see <https://www.gnu.org/licenses/>.


import os
import subprocess

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtCore import *
    from PySide.QtGui import *

from PrismUtils.Decorators import err_catcher_plugin as err_catcher


class Prism_AfterEffects_externalAccess_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin
        self.core.registerCallback(
            "projectBrowser_loadUI", self.projectBrowser_loadUI, plugin=self.plugin
        )
        self.core.registerCallback(
            "openPBFileContextMenu", self.openPBFileContextMenu, plugin=self.plugin
        )
    @err_catcher(name=__name__)
    def getAutobackPath(self, origin, tab):
        autobackpath = ""

        fileStr = "AfterEffects Script ("
        for i in self.sceneFormats:
            fileStr += "*%s " % i

        fileStr += ")"

        return autobackpath, fileStr

    @err_catcher(name=__name__)
    def projectBrowser_loadUI(self, origin):
        #cmenu = QMenu(origin.lw_version)
        #infAct = QAction("Show version info", origin.lw_version)
        #infAct.triggered.connect(self.getAppVersion)
        #rcmenu.addAction(infAct)
        #rcmenu.exec_()
        print(self.core.appPlugin.pluginName)
        print("!!!!")
        if self.core.appPlugin.pluginName == "AfterEffects":

            #rcmenu = QMenu(origin.sceneBrowser)
            #pastAE = QAction("AE", origin)
            #past.triggered.connect(self.pastefile)
            #rcmenu.addAction(pastAE)

            
            psMenu = QMenu("AfterEffects")
            psAction = QAction("Connect", origin)
            psAction.triggered.connect(lambda: self.connectToAfterEffects(origin))
            psMenu.addAction(psAction)
            origin.menuTools.insertSeparator(origin.menuTools.actions()[-2])
            origin.menuTools.insertMenu(origin.menuTools.actions()[-2], psMenu)
            
    def openPBFileContextMenu(self, origin, menu, filepath):
        ext = os.path.splitext(filepath)[1]
        if ext == ".aep":
            
            #pmenu = QMenu("AE", origin)
            
            #data = self.core.entities.getScenefileData(filepath)
            #entity = data.get("type")
            #if entity:
            #    action = QAction("Set as %s preview" % entity, origin)
            #    action.triggered.connect(lambda: self.setAsPreview(origin, filepath))
            #    pmenu.addAction(action)

            #    action = QAction("Export...", origin)
            #    action.triggered.connect(lambda: self.exportDlg(filepath))
            #    pmenu.addAction(action)

            #menu.insertMenu(menu.actions()[0], pmenu)
            data = self.core.entities.getScenefileData(filepath)
            entity = data.get("type")
            if entity:
                action = QAction("Import aep" , origin)
                action.triggered.connect(lambda: self.aepImport(origin, filepath))
                menu.addAction(action)
                
    def aepImport(self, origin, path):
        import Prism_AfterEffects_Functions
        path = path.replace("\\", "/")
        scpt ="app.project.importFile(new ImportOptions(File('"+path+"')));"
        Prism_AfterEffects_Functions.Prism_AfterEffects_Functions.executeAppleScript(origin, scpt)
        #with self.core.waitPopup(self.core, "Creating preview. Please wait..."):
        #    entity = self.core.entities.getScenefileData(path)
        #    previewImg = self.getImageFromScene(path)
        #    self.core.entities.setEntityPreview(entity, previewImg)
        #    origin.refreshEntityInfo()

    @err_catcher(name=__name__)
#    def openPBListContextMenu(self, origin, rcmenu, listWidget, item, path):
#        # gets called before "rcmenu" get displayed for the "Tasks" and "Versions" list in the Project Browser.
#        infAct = QAction("@@@@", self)
#        infAct.triggered.connect(self.showVersionInfo)
#        rcmenu.addAction(infAct)
#        return "55555"

    @err_catcher(name=__name__)
    def customizeExecutable(self, origin, appPath, filepath):
        self.connectToAfterEffects(origin, filepath=filepath)
        return True

    @err_catcher(name=__name__)
    def connectToAfterEffects(self, origin, filepath=""):
        pythonPath = self.core.getPythonPath(executable="Prism Project Browser")

        menuPath = os.path.join(
            self.core.prismRoot,
            "Plugins",
            "Apps",
            "AfterEffects",
            "Scripts",
            "Prism_AfterEffects_MenuTools.py",
        )
        subprocess.Popen([pythonPath, menuPath, "Tools", filepath])

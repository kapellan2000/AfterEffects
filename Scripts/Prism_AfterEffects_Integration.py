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
import sys
import platform
import shutil

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtCore import *
    from PySide.QtGui import *

if platform.system() == "Windows":
    if sys.version[0] == "3":
        import winreg as _winreg
    else:
        import _winreg

from PrismUtils.Decorators import err_catcher_plugin as err_catcher


class Prism_AfterEffects_Integration(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin

        #self.examplePath, self.afVersion = self.getAfterEffectsPath()
        self.examplePath = "c:/Program Files/Common Files/Adobe/CEP/extensions/"
    @err_catcher(name=__name__)
    def getAfterEffectsPath(self, single=True):
        try:
            psPaths = []
            if platform.system() == "Windows":
                key = _winreg.OpenKey(
                    _winreg.HKEY_LOCAL_MACHINE,
                    "SOFTWARE\\Adobe\\After Effects",
                    0,
                    _winreg.KEY_READ | _winreg.KEY_WOW64_64KEY,
                )
                idx = 0
                while True:
                    try:
                        afVersion = _winreg.EnumKey(key, idx)
                        psKey = _winreg.OpenKey(
                            _winreg.HKEY_LOCAL_MACHINE,
                            "SOFTWARE\\Adobe\\After Effects\\" + afVersion,
                            0,
                            _winreg.KEY_READ | _winreg.KEY_WOW64_64KEY,
                        )
                        path = _winreg.QueryValueEx(psKey, "InstallPath")[0]
                        path = os.path.normpath(path)
                        psPaths.append(path.split("\Support Files")[0])
                        idx += 1
                    except:
                        break
            elif platform.system() == "Darwin":
                for foldercont in os.walk("/Applications"):
                    for folder in reversed(sorted(foldercont[1])):
                        if folder.startswith("Adobe After Effects"):
                            psPaths.append(os.path.join(foldercont[0], folder))
                            if single:
                                break
                    break

            if single:
                return psPaths[-1],afVersion if psPaths else None
            else:
                return psPaths if psPaths else []
        except:
            return None

    def addIntegration(self, installPath):
        try:
            #Enable debug mode 
            parentKey = _winreg.OpenKey(_winreg.HKEY_CURRENT_USER,
                "SOFTWARE\\Adobe")
            i = 0
            while True:
               try:
                   key = _winreg.EnumKey(parentKey, i)
                   print (key)
                   i += 1
                   if key[:5]=="CSXS.":
                       key = _winreg.CreateKey(_winreg.HKEY_CURRENT_USER, 'SOFTWARE\\Adobe\\'+key)
                       _winreg.SetValueEx(key, 'PlayerDebugMode', 0, _winreg.REG_SZ, '1')
                       _winreg.CloseKey(key)


               except WindowsError:
                   break
                    
            cmds = []
            if not os.path.exists(installPath):
                QMessageBox.warning(
                    self.core.messageParent,
                    "Prism Integration",
                    "Invalid AfterEffects path: %s.\nThe path doesn't exist."
                    % installPath,
                    QMessageBox.Ok,
                )
                return False
 
                
            integrationBase = os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "Integration"
            )


            cmds = []
            origLFile = os.path.join(integrationBase,"Windows", "prism.aep")
            scriptdir = os.path.join(installPath, "prism.aep")
            d_css = os.path.join(scriptdir,"css")
            d_csxs = os.path.join(scriptdir,"CSXS")
            d_js = os.path.join(scriptdir,"js")
            d_libs = os.path.join(scriptdir,"js","libs")
            
            if os.path.exists(scriptdir):
                cmd = {
                        "type": "removeFile",
                        "args": [scriptdir],
                        "validate": False,
                    }
                cmds.append(cmd) 
            for i in [scriptdir,d_css,d_csxs,d_js,d_libs]:
                cmd = {"type": "createFolder", "args": [i]}
                cmds.append(cmd)
            source = os.path.join(origLFile,"index.html")    
            cmd = {"type": "copyFile", "args": [source, scriptdir]}
            cmds.append(cmd)  
            
            source = os.path.join(origLFile,"css","style.css")
            cmd = {"type": "copyFile", "args": [source, d_css]}
            cmds.append(cmd)
            
            source = os.path.join(origLFile,"CSXS","manifest.xml")
            cmd = {"type": "copyFile", "args": [source, d_csxs]}
            cmds.append(cmd)
            
            source = os.path.join(origLFile,"js","main.js")
            cmd = {"type": "copyFile", "args": [source, d_js]}
            cmds.append(cmd)
            
            source = os.path.join(origLFile,"js","themeManager.js")
            cmd = {"type": "copyFile", "args": [source, d_js]}
            cmds.append(cmd)    
            
            source = os.path.join(origLFile,"js","libs","CSInterface.js")
            cmd = {"type": "copyFile", "args": [source, d_libs]}
            cmds.append(cmd)               





                
            #origLFile = os.path.join(integrationBase,"Windows")
            #scriptdir = os.path.join(installPath)

            #if os.path.exists(scriptdir+"/prism"):
                #os.remove(scriptdir+"/prism")
            #    cmd = {"type": "removeFile", "args": [scriptdir+"/prism"], "validate": False}
            #    cmds.append(cmd)
            #shutil.copy2(origLFile, scriptdir)


            result = self.core.runFileCommands(cmds)
            return result
            #else:
            #    raise Exception(result)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            msgStr = (
                "Errors occurred during the installation of the AfterEffects integration.\nThe installation is possibly incomplete.\n\n%s\n%s\n%s"
                % (str(e), exc_type, exc_tb.tb_lineno)
            )
            msgStr += "\n\nRunning this application as administrator could solve this problem eventually."

            self.core.popup(msgStr, title="Prism Integration")
            return False

    def removeIntegration(self, installPath):
        print(installPath)
        try:

            fPath = os.path.join(installPath, "prism.aep")
            
            cmds = []


            file_paths = []
            for root, directories, files in os.walk(fPath):
                for filename in files:
                    cmd = {
                            "type": "removeFile",
                            "args": [os.path.join(root, filename)],
                            "validate": False,
                        }
                    cmds.append(cmd)
            

            #if os.path.exists(fPath):
            #    os.remove(fPath)
            result = self.core.runFileCommands(cmds)
            
            return True
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()

            msgStr = (
                "Errors occurred during the removal of the AfterEffects integration.\n\n%s\n%s\n%s"
                % (str(e), exc_type, exc_tb.tb_lineno)
            )
            msgStr += "\n\nRunning this application as administrator could solve this problem eventually."

            self.core.popup(msgStr, title="Prism Integration")
            return False

    def updateInstallerUI(self, userFolders, pItem):
    
        try:
        
            psItem = QTreeWidgetItem(["After Effects"])
            psItem.setCheckState(0, Qt.Checked)
            pItem.addChild(psItem)

            psPaths = self.getAfterEffectsPath(single=False) or []
            
            psCustomItem = QTreeWidgetItem(["Custom"])
            psCustomItem.setToolTip(0, 'e.g. "%s"' % self.examplePath)
            psCustomItem.setToolTip(1, 'e.g. "%s"' % self.examplePath)
            psCustomItem.setText(1, "< doubleclick to browse path >")
            psCustomItem.setCheckState(0, Qt.Unchecked)
            psItem.addChild(psCustomItem)
            psItem.setExpanded(True)

            activeVersion = False
            for i in reversed(psPaths):
                psVItem = QTreeWidgetItem([i[-4:]])
                psItem.addChild(psVItem)

                if os.path.exists(i):
                    psVItem.setCheckState(0, Qt.Checked)
                    psVItem.setText(1, i)
                    psVItem.setToolTip(0, i)
                    psVItem.setText(1, i)
                    activeVersion = True
                else:
                    psVItem.setCheckState(0, Qt.Unchecked)
                    psVItem.setFlags(~Qt.ItemIsEnabled)

            if not activeVersion:
                psItem.setCheckState(0, Qt.Unchecked)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            msg = QMessageBox.warning(
                self.core.messageParent,
                "Prism Installation",
                "Errors occurred during the installation.\n The installation is possibly incomplete.\n\n%s\n%s\n%s\n%s"
                % (__file__, str(e), exc_type, exc_tb.tb_lineno),
            )
            return False

    def installerExecute(self, AfterEffectsItem, result):
        try:
            psPaths = []
            installLocs = []

            if AfterEffectsItem.checkState(0) != Qt.Checked:
                return installLocs

            for i in range(AfterEffectsItem.childCount()):
                item = AfterEffectsItem.child(i)
                if item.checkState(0) == Qt.Checked and os.path.exists(item.text(1)):
                    psPaths.append(item.text(1))

            for i in psPaths:
                result["AfterEffects integration"] = self.core.integration.addIntegration(self.plugin.pluginName, path=i, quiet=True)
                if result["AfterEffects integration"]:
                    installLocs.append(i)

            return installLocs
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            msg = QMessageBox.warning(
                self.core.messageParent,
                "Prism Installation",
                "Errors occurred during the installation.\n The installation is possibly incomplete.\n\n%s\n%s\n%s\n%s"
                % (__file__, str(e), exc_type, exc_tb.tb_lineno),
            )
            return False

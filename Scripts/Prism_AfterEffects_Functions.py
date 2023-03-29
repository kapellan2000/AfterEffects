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
import subprocess
import socket

try:
    from PySide2.QtCore import *
    from PySide2.QtGui import *
    from PySide2.QtWidgets import *
except:
    from PySide.QtCore import *
    from PySide.QtGui import *

if platform.system() == "Windows":
    import win32com.client

from PrismUtils.Decorators import err_catcher as err_catcher


class Prism_AfterEffects_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin
        self.win = platform.system() == "Windows"
        self.callbacks = []

    @err_catcher(name=__name__)
#    def registerCallbacks(self):
#        self.callbacks.append(self.core.registerCallback("openPBListContextMenu", self.openPBListContextMenu))

    @err_catcher(name=__name__)
    def startup(self, origin):
        origin.timer.stop()
        root = os.path.dirname(self.pluginPath).replace("\\", "/").split("Scripts")[0]
        with (
            open(
                os.path.join(
                    root,
                    "UserInterfaces",
                    "AfterEffectsStyleSheet",
                    "AfterEffects.qss",
                ),
                "r",
            )
        ) as ssFile:
            ssheet = ssFile.read()

        ssheet = ssheet.replace(
            "qss:",
            os.path.join(
                root,
                "UserInterfaces",
                "AfterEffectsStyleSheet",
            ).replace("\\", "/")
            + "/",
        )
        # ssheet = ssheet.replace("#c8c8c8", "rgb(40, 40, 40)").replace("#727272", "rgb(83, 83, 83)").replace("#5e90fa", "rgb(89, 102, 120)").replace("#505050", "rgb(70, 70, 70)")
        # ssheet = ssheet.replace("#a6a6a6", "rgb(145, 145, 145)").replace("#8a8a8a", "rgb(95, 95, 95)").replace("#b5b5b5", "rgb(155, 155, 155)").replace("#999999", "rgb(105, 105, 105)")
        # ssheet = ssheet.replace("#9f9f9f", "rgb(58, 58, 58)").replace("#b2b2b2", "rgb(58, 58, 58)").replace("#aeaeae", "rgb(65, 65, 65)").replace("#c1c1c1", "rgb(65, 65, 65)")

        qApp.setStyleSheet(ssheet)
        appIcon = QIcon(
            os.path.join(
                self.core.prismRoot, "Scripts", "UserInterfacesPrism", "p_tray.png"
            )
        )
        qApp.setWindowIcon(appIcon)

        if self.win:
            try:
                # CS6: .60, CC2015: .90
                pass
                #self.psApp = win32com.client.Dispatch("AfterEffects.Application")
            except Exception as e:
                QMessageBox.warning(
                    self.core.messageParent,
                    "Warning",
                    "Could not connect to AfterEffects:\n\n%s" % str(e),
                )
                return False
        else:
            self.psAppName = "Adobe AfterEffects CC 2019"
            for foldercont in os.walk("/Applications"):
                for folder in reversed(sorted(foldercont[1])):
                    if folder.startswith("Adobe AfterEffects"):
                        self.psAppName = folder
                        break
                break

            scpt = (
                """
            tell application "%s"
                activate
            end tell
            """
                % self.psAppName
            )
            self.executeAppleScript(scpt)

        return False
        
    @err_catcher(name=__name__)
    def onProjectChanged(self, origin):
        pass

    @err_catcher(name=__name__)
    def sceneOpen(self, origin):
        pass

    @err_catcher(name=__name__)
    def executeScript(self, origin, code, preventError=False):
        if preventError:
            try:
                return eval(code)
            except Exception as e:
                msg = "\npython code:\n%s" % code
                exec("raise type(e), type(e)(e.message + msg), sys.exc_info()[2]")
        else:
            return eval(code)

    @err_catcher(name=__name__)
    def executeAppleScript(self, script):
        HOST = '127.0.0.1'
        PORT = 9888
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            data = (script).encode("utf-8")
            s.sendall(data)
            data = s.recv(1024)

        return data

    @err_catcher(name=__name__)
    def getCurrentFileName(self, origin, path=True):
        try:
            scpt = "app.project.file.fsName;" #fsName name
    
            file_name, file_extension = os.path.splitext(self.executeAppleScript(scpt))
            currentFileName = str(file_name)[2:].replace("\\\\","/")
            
            if path:
                return currentFileName
            else:
                return currentFileName.split("\\")[-1:][0]
        except:
            currentFileName = ""
            return


    @err_catcher(name=__name__)
    def getSceneExtension(self, origin):
        print(origin)
        doc = self.core.getCurrentFileName()
        if doc != "":
            return os.path.splitext(doc)[1]
        return self.sceneFormats[0]

    @err_catcher(name=__name__)
    def onSaveExtendedOpen(self, origin):
        origin.l_format = QLabel("Save as:")
        origin.cb_format = QComboBox()
        origin.cb_format.addItems(self.sceneFormats)
        curFilename = self.core.getCurrentFileName()
        if curFilename:
            ext = os.path.splitext(curFilename)[1]
            idx = self.sceneFormats.index(ext)
            if idx != -1:
                origin.cb_format.setCurrentIndex(idx)
        rowIdx = origin.w_details.layout().rowCount()
        origin.w_details.layout().addWidget(origin.l_format, rowIdx, 0)
        origin.w_details.layout().addWidget(origin.cb_format, rowIdx, 1)

    @err_catcher(name=__name__)
    def onGetSaveExtendedDetails(self, origin, details):
        details["fileFormat"] = origin.cb_format.currentText()

    @err_catcher(name=__name__)
    def getCharID(self, s):
        return self.psApp.CharIDToTypeID(s)

    @err_catcher(name=__name__)
    def getStringID(self, s):
        return self.psApp.StringIDToTypeID(s)

    @err_catcher(name=__name__)
    def saveScene(self, origin, filepath, details={}):
        try:    
                scpt ="app.project.save(File('"+filepath+"'));"
                print(filepath)
                name = self.executeAppleScript(scpt)
                if name is None:
                    raise
        except:
            self.core.popup("There is no active document in AfterEffects.")
            return False



    @err_catcher(name=__name__)
    def getImportPaths(self, origin):
        return False

    @err_catcher(name=__name__)
    def getFrameRange(self, origin):
        pass

    @err_catcher(name=__name__)
    def setFrameRange(self, origin, startFrame, endFrame):
        pass

    @err_catcher(name=__name__)
    def getFPS(self, origin):
        pass

    @err_catcher(name=__name__)
    def getAppVersion(self, origin):
        if self.win:
            version = self.psApp.Version
        else:
            scpt = (
                """
                tell application "%s"
                    application version
                end tell
            """
                % self.psAppName
            )
            version = self.executeAppleScript(scpt)

        return version

    @err_catcher(name=__name__)
    def onProjectBrowserStartup(self, origin):
        origin.actionStateManager.setEnabled(False)
        psMenu = QMenu("AfterEffects", origin)
        psAction = QAction("Open tools", origin)
        psAction.triggered.connect(self.openAfterEffectsTools)
        psMenu.addAction(psAction)
        origin.menuTools.addSeparator()
        origin.menuTools.addMenu(psMenu)
        
        #origin.lw_version.setEnabled(False)
        #test = QAction("TEST", origin)
        #test.triggered.connect()
        #origin.lw_version.rcmenu.addAction(test)
        #origin.lw_version.customContextMenuRequested()

    @err_catcher(name=__name__)
    

    @err_catcher(name=__name__)
#    def openPBListContextMenu(self, origin, rcmenu, listWidget, item, path):
#        inftest = QAction("Import" ,origin)
#        #inftest.triggered.connect(self.importSelectedVersion)
#        rcmenu.addAction(inftest)
#        print(listWidget)
#        print(item)
#        print(path)
#        #return rcmenu



    @err_catcher(name=__name__)
    def openScene(self, origin, filepath, force=False):
        # load scenefile
        if (not filepath.endswith(".aep")):
            return False

        scpt ="app.open(File('"+filepath+"'));"
        name = self.executeAppleScript(scpt)
        return True

    @err_catcher(name=__name__)
    def correctExt(self, origin, lfilepath):
        return lfilepath

    @err_catcher(name=__name__)
    def setSaveColor(self, origin, btn):
        btn.setPalette(origin.savedPalette)

    @err_catcher(name=__name__)
    def clearSaveColor(self, origin, btn):
        btn.setPalette(origin.oldPalette)

    @err_catcher(name=__name__)
    def importImages(self, origin):
        fString = "Please select an import option:"
        msg = QMessageBox(
            QMessageBox.NoIcon, "AfterEffects Import", fString, QMessageBox.Cancel
        )
        msg.addButton("Current pass", QMessageBox.YesRole)
        #   msg.addButton("All passes", QMessageBox.YesRole)
        #   msg.addButton("Layout all passes", QMessageBox.YesRole)
        self.core.parentWindow(msg)
        action = msg.exec_()

        if action == 0:
            self.AfterEffectsImportSource(origin)
        #   elif action == 1:
        #       self.AfterEffectsImportPasses(origin)
        #   elif action == 2:
        #       self.AfterEffectsLayout(origin)
        else:
            return

    @err_catcher(name=__name__)
    def AfterEffectsImportSource(self, origin):
        sourceData = origin.compGetImportSource()
        print(sourceData)
        print(sourceData[0])
        for i in sourceData:
            filePath = os.path.dirname(i[0])
            firstFrame = i[1]
            lastFrame = i[2]

            #mpb = origin.mediaPlayer.seq
        
            #mpb = origin.mediaPlaybacks["shots"]
            #sourceFolder = os.path.dirname(
            #    os.path.join(mpb["basePath"], mpb["seq"][0])
            #).replace("\\", "/")
            try:
                    scpt ="app.project.setDefaultImportFolder(Folder('" + filePath + "'));app.project.importFileWithDialog();app.project.setDefaultImportFolder();"
                    name = self.executeAppleScript(scpt)
                    if name is None:
                        raise
            except:
                self.core.popup(" Error  107.")
                return False


            # curReadNode = AfterEffects.createNode("Read",'file %s first %s last %s' % (filePath,firstFrame,lastFrame),False)

    @err_catcher(name=__name__)
    def AfterEffectsImportPasses(self, origin):
        sourceFolder = os.path.dirname(
            os.path.dirname(os.path.join(origin.basepath, origin.seq[0]))
        ).replace("\\", "/")
        passes = [
            x
            for x in os.listdir(sourceFolder)
            if x[-5:] not in ["(mp4)", "(jpg)", "(png)"]
            and os.path.isdir(os.path.join(sourceFolder, x))
        ]

        for curPass in passes:
            curPassPath = os.path.join(sourceFolder, curPass)

            imgs = os.listdir(curPassPath)
            if len(imgs) == 0:
                continue

            if len(imgs) > 1:
                if (
                    not hasattr(origin, "pstart")
                    or not hasattr(origin, "pend")
                    or origin.pstart == "?"
                    or origin.pend == "?"
                ):
                    return

                firstFrame = origin.pstart
                lastFrame = origin.pend

                curPassName = imgs[0].split(".")[0]
                increment = "####"
                curPassFormat = imgs[0].split(".")[-1]

                filePath = os.path.join(
                    sourceFolder,
                    curPass,
                    ".".join([curPassName, increment, curPassFormat]),
                ).replace("\\", "/")
            else:
                filePath = os.path.join(curPassPath, imgs[0]).replace("\\", "/")
                firstFrame = 0
                lastFrame = 0

            curReadNode = AfterEffects.createNode(
                "Read",
                "file %s first %s last %s" % (filePath, firstFrame, lastFrame),
                False,
            )

    @err_catcher(name=__name__)
    def setProject_loading(self, origin):
        pass

    @err_catcher(name=__name__)
    def onPrismSettingsOpen(self, origin):
        pass

    @err_catcher(name=__name__)
    def createProject_startup(self, origin):
        pass

    @err_catcher(name=__name__)
    def editShot_startup(self, origin):
        pass

    @err_catcher(name=__name__)
    def shotgunPublish_startup(self, origin):
        pass

    @err_catcher(name=__name__)
    def openAfterEffectsTools(self):
        self.dlg_tools = QDialog()

        lo_tools = QVBoxLayout()
        self.dlg_tools.setLayout(lo_tools)

        b_saveVersion = QPushButton("Save Version")
        b_saveComment = QPushButton("Save Extended")
        b_export = QPushButton("Export")
        b_projectBrowser = QPushButton("Project Browser")
        b_settings = QPushButton("Settings")

        b_saveVersion.clicked.connect(self.core.saveScene)
        b_saveComment.clicked.connect(self.core.saveWithComment)
        b_export.clicked.connect(self.exportImage)
        b_projectBrowser.clicked.connect(self.core.projectBrowser)
        b_settings.clicked.connect(self.core.prismSettings)

        lo_tools.addWidget(b_saveVersion)
        lo_tools.addWidget(b_saveComment)
        lo_tools.addWidget(b_export)
        lo_tools.addWidget(b_projectBrowser)
        lo_tools.addWidget(b_settings)

        self.core.parentWindow(self.dlg_tools)
        self.dlg_tools.setWindowTitle("Prism")

        self.dlg_tools.show()

        return True

    @err_catcher(name=__name__)
    def exportImage(self):
        if not self.core.projects.ensureProject():
            return False

        if not self.core.users.ensureUser():
            return False

        curfile = self.core.getCurrentFileName()
        fname = self.core.getScenefileData(curfile)
        if fname["filename"] == "invalid":
            entityType = "context"
        else:
            entityType = fname["filename"]

        self.dlg_export = QDialog()
        self.core.parentWindow(self.dlg_export)
        self.dlg_export.setWindowTitle("Prism - Export image")

        lo_export = QVBoxLayout()
        self.dlg_export.setLayout(lo_export)

        self.rb_task = QRadioButton("Export into current %s" % entityType)
        self.w_task = QWidget()
        lo_prismExport = QVBoxLayout()
        lo_task = QHBoxLayout()
        self.w_comment = QWidget()
        lo_comment = QHBoxLayout()
        self.w_comment.setLayout(lo_comment)
        lo_comment.setContentsMargins(0, 0, 0, 0)
        lo_version = QHBoxLayout()
        custom_version = QHBoxLayout()
        lo_extension = QHBoxLayout()
        lo_localOut = QHBoxLayout()
        l_task = QLabel("Task:")
        l_task.setMinimumWidth(110)
        self.le_task = QLineEdit()
        self.b_task = QPushButton(u"▼")
        self.b_task.setMinimumSize(35, 0)
        self.b_task.setMaximumSize(35, 500)
        l_comment = QLabel("Comment (optional):")
        l_comment.setMinimumWidth(110)
        self.le_comment = QLineEdit()
        self.chb_useNextVersion = QCheckBox("Use next version")
        self.chb_useNextVersion.setChecked(True)
        self.chb_useNextVersion.setMinimumWidth(110)
        
        self.custom_name = QCheckBox("custom task name")
        self.custom_name.setChecked(False)
        self.custom_name.setMinimumWidth(110)
        self.cb_versions = QComboBox()
        self.cb_versions.setEnabled(False)
        self.cb_versions.setStyleSheet('''*    
        QComboBox QAbstractItemView 
            {
            min-width: 300px;
            }
        ''')
        l_ext = QLabel("Format:")
        l_ext.setMinimumWidth(110)
        self.cb_formats = QComboBox()
        self.cb_formats.addItems([".mp4", ".jpg", ".png", ".tif", ".exr"])
        self.chb_localOutput = QCheckBox("Local output")
        lo_task.addWidget(l_task)
        lo_task.addWidget(self.le_task)
        lo_task.addWidget(self.b_task)
        lo_comment.addWidget(l_comment)
        lo_comment.addWidget(self.le_comment)
        lo_version.addWidget(self.chb_useNextVersion)
        lo_version.addWidget(self.cb_versions)
        lo_version.addStretch()
        
        custom_version.addWidget(self.custom_name)
        custom_version.addWidget(self.cb_versions)
        custom_version.addStretch()
        lo_extension.addWidget(l_ext)
        lo_extension.addWidget(self.cb_formats)
        lo_extension.addStretch()
        lo_localOut.addWidget(self.chb_localOutput)
        lo_prismExport.addLayout(lo_task)
        lo_prismExport.addWidget(self.w_comment)
        lo_prismExport.addLayout(lo_version)
        
        lo_prismExport.addLayout(custom_version)
        lo_prismExport.addLayout(lo_extension)
        lo_prismExport.addLayout(lo_localOut)
        self.w_task.setLayout(lo_prismExport)
        self.w_task.setLayout(lo_prismExport)
        lo_version.setContentsMargins(0, 0, 0, 0)

        rb_custom = QRadioButton("Export to custom location")

        self.b_export = QPushButton("Export")

        lo_export.addWidget(self.rb_task)
        lo_export.addWidget(self.w_task)
        lo_export.addWidget(rb_custom)
        lo_export.addStretch()
        lo_export.addWidget(self.b_export)

        self.rb_task.setChecked(True)
        self.dlg_export.resize(400, 300)

        self.rb_task.toggled.connect(self.exportToggle)
        self.b_task.clicked.connect(self.exportShowTasks)
        self.le_comment.textChanged.connect(self.validateComment)
        self.chb_useNextVersion.toggled.connect(self.exportVersionToggled)
        self.le_task.editingFinished.connect(self.exportGetVersions)
        self.b_export.clicked.connect(self.saveExport)

        if not self.core.useLocalFiles:
            self.chb_localOutput.setVisible(False)

        self.exportGetTasks()
        self.core.callback(
            name="AfterEffects_onExportOpen",
            types=[],
            args=[self],
        )

        self.dlg_export.show()

        self.cb_versions.setMinimumWidth(300)
        self.cb_formats.setMinimumWidth(300)

        return True

    @err_catcher(name=__name__)
    def exportToggle(self, checked):
        self.w_task.setEnabled(checked)

    @err_catcher(name=__name__)
    def exportGetTasks(self):
        self.taskList = self.core.getTaskNames("2d")

        if len(self.taskList) == 0:
            self.b_task.setHidden(True)
        else:
            if "_ShotCam" in self.taskList:
                self.taskList.remove("_ShotCam")

    @err_catcher(name=__name__)
    def exportShowTasks(self):
        tmenu = QMenu(self.dlg_export)

        for i in self.taskList:
            tAct = QAction(i, self.dlg_export)
            tAct.triggered.connect(lambda x=None, t=i: self.le_task.setText(t))
            tAct.triggered.connect(self.exportGetVersions)
            tmenu.addAction(tAct)

        tmenu.exec_(QCursor.pos())

    @err_catcher(name=__name__)
    def exportGetVersions(self):
        existingVersions = []
        outData = self.exportGetOutputName()
        if outData is not None:
            versionDir = os.path.dirname(outData[1])

            if os.path.exists(versionDir):
                for i in reversed(sorted(os.listdir(versionDir))):
                    if len(i) < 5 or not i.startswith("v"):
                        continue

                    if sys.version[0] == "2":
                        if not unicode(i[1:5]).isnumeric():
                            continue
                    else:
                        if not i[1:5].isnumeric():
                            continue

                    existingVersions.append(i)

        self.cb_versions.clear()
        self.cb_versions.addItems(existingVersions)

    def exportGetOutputName(self, useVersion="next"):
        if self.le_task.text() == "":
            return

        extension = self.cb_formats.currentText()
        fileName = self.core.getCurrentFileName()

        if self.core.useLocalFiles:
            if self.chb_localOutput.isChecked():
                fileName = self.core.convertPath(fileName, target="local")
            else:
                fileName = self.core.convertPath(fileName, target="global")

        hVersion = ""
        pComment = self.le_comment.text()
        if useVersion != "next":
            hVersion = useVersion.split(self.core.filenameSeparator)[0]
            pComment = useVersion.split(self.core.filenameSeparator)[1]

        fnameData = self.core.getScenefileData(fileName)
        if fnameData["type"] == "shot":
            outputPath = os.path.abspath(
                os.path.join(
                    fileName,
                    os.pardir,
                    os.pardir,
                    os.pardir,
                    os.pardir,
                    "Renders",
                    "2dRender",
                    self.le_task.text(),
                )
            )
            if hVersion == "":
                hVersion = self.core.getHighestVersion(outputPath)
                if hVersion == None:
                    hVersion = fnameData["version"]
            outputFile = os.path.join(
                "shot"
                + "_"
                + fnameData["shot"]
                + "_"
                + self.le_task.text()
                + "_"
                + hVersion
                + extension
            )
        elif fnameData["type"] == "asset":
            base = self.core.getAssetPath()
            outputPath = os.path.abspath(
                os.path.join(
                    base,
                    "Renders",
                    "2dRender",
                    self.le_task.text(),
                )
            )
            if hVersion == "":
                hVersion = self.core.getHighestVersion(outputPath)
            outputFile = os.path.join(
                fnameData["asset_path"]
                + "_"
                + self.le_task.text()
                + "_"
                + hVersion
                + extension
            )
        else:
            return

        outputPath = os.path.join(outputPath, hVersion)
        if pComment != "":
            outputPath += "_" + pComment

        outputName = os.path.join(outputPath, outputFile)

        return outputName, outputPath, hVersion

    @err_catcher(name=__name__)
    def exportVersionToggled(self, checked):
        self.cb_versions.setEnabled(not checked)
        self.w_comment.setEnabled(checked)

    @err_catcher(name=__name__)
    def validateComment(self, text):
        self.core.validateLineEdit(self.le_comment)

    @err_catcher(name=__name__)
    def saveExport(self):
        if self.rb_task.isChecked():
            taskName = self.le_task.text()
            if taskName is None or taskName == "":
                QMessageBox.warning(
                    self.core.messageParent, "Warning", "Please choose a taskname"
                )
                return

            if not self.core.fileInPipeline():
                QMessageBox.warning(
                    self.core.messageParent,
                    "Warning",
                    "The current file is not inside the Pipeline.\nUse the Project Browser to create a file in the Pipeline.",
                )
                return False

            oversion = "next"
            if not self.chb_useNextVersion.isChecked():
                oversion = self.cb_versions.currentText()

            if oversion is None or oversion == "":
                QMessageBox.warning(
                    self.core.messageParent, "Warning", "Invalid version"
                )
                return

            outputPath, outputDir, hVersion = self.exportGetOutputName(oversion)

            outLength = len(outputPath)
            if platform.system() == "Windows" and outLength > 255:
                msg = "The outputpath is longer than 255 characters (%s), which is not supported on Windows. Please shorten the outputpath by changing the comment, taskname or projectpath." % outLength
                self.core.popup(msg)
                return

            if not os.path.exists(outputDir):
                os.makedirs(outputDir)
            
            details = {
                "version": hVersion,
                "sourceScene": self.core.getCurrentFileName(),
            }

            self.core.saveVersionInfo(
                filepath=os.path.dirname(outputPath),
                details=details,
            )
        else:
            startLocation = os.path.join(
                self.core.projectPath,
                self.core.getConfig("paths", "assets", configPath=self.core.prismIni),
                "Textures",
            )
            outputPath = QFileDialog.getSaveFileName(
                self.dlg_export,
                "Enter output filename",
                startLocation,
                "MP4 (*.mp4);;JPEG (*.jpg *.jpeg);;PNG (*.png);;TIFF (*.tif *.tiff);;OpenEXR (*.exr)",
            )[0]

            if outputPath == "":
                return

        ext = os.path.splitext(outputPath)[1].lower()

        scpt = """
        var resultFile = new File('""" + outputPath.replace("\\","//") + """')
        var renderQueue = app.project.renderQueue;
        //var sel = app.project.item(1);
        app.activeViewer.setActive();
        var sel = app.project.activeItem;
        var render = renderQueue.items.add(sel);
        render.outputModules[1].file = resultFile;
        app.project.renderQueue.queueInAME(false);
        """
        currentFileName = self.executeAppleScript(scpt)


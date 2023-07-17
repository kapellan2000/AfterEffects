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

class Prism_AfterEffects_Variables(object):
    def __init__(self, core, plugin):
        self.version = "v2.0.0.beta17.3"
        self.pluginName = "AfterEffects"
        self.pluginType = "App"
        self.appShortName = "AfterEffects"
        self.appType = "2d"
        self.hasQtParent = False
        self.sceneFormats = [".aep"]
        self.appSpecificFormats = self.sceneFormats
        self.appColor = [200, 50, 50]
        self.appVersionPresets = ["13.0.0"]
        self.hasFrameRange = False
        #self.canOverrideExecuteable = False
        self.platforms = ["Windows", "Darwin"]
        self.pluginDirectory = os.path.abspath(
            os.path.dirname(os.path.dirname(__file__))
        )
        self.appIcon = os.path.join(
            self.pluginDirectory, "UserInterfaces", "AE.ico"
        )
        
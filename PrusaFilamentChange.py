# -*- encoding: utf-8 -*-

# Heavily based on Cura's FilamentChange.py (inside Cura app bundle on macOS)
# Used this blog post for info, since Ultimaker's docs were down:
# https://ryanbuhl.com/ryanbuhl.com/2020/09/19/cura-post-processing-scripts-part-iii-insertatlayerchange-initialization-and-user-settings/

import json
import io
import string
from ..Script import Script
from UM.Logger import Logger

class PrusaFilamentChange(Script):
    def getSettingDataString(self):
        return json.dumps({
            "name": "Prusa Filament Change",
            "key": "PrusaFilamentChange",
            "metadata": {},
            "version": 2,
            "settings": {
                "enable": {
                    "label": "Enable",
                    "description": "When enabled, will write settings at end of gcode",
                    "type": "bool",
                    "default_value": True
                },
                "layer": {
                    "label": "Layer",
                    "description": "At what layer should filament change occur. This will be before the layer starts printing.",
                    "type": "int",
                    "default_value": 1,
                    "minimum_value": 1,
                    "minimum_value_warning": "1",
                    "enabled": "enable"
                },
                "finalchange": {
                    "label": "Change after final layer",
                    "description": "Add a final filament change at the end of the print.",
                    "type": "bool",
                    "default_value": False,
                    "enabled": "enable"
                }
            }
        })

    def execute(self, data):
        Logger.log("d", "Executing PrusaFilamentChange now")
        """Adds Prusa-friendly filament change G-code at the specific layer

        :param data: A list of layers of g-code.
        :return: A similar list, with filament change commands inserted.
        """
        enable = self.getSettingValueByKey("enable")
        layer = self.getSettingValueByKey("layer") + 1
        finalchange = self.getSettingValueByKey("finalchange")

        if not enable:
            Logger.log("d", "Skipping filament change (disabled).")
            return data

        if not 0 < layer < len(data):
            Logger.logException("w", "Layer index out of range.")
            return data

        color_change = """


; Filament change code by PrusaFilamentChange
G60 S2 ; Save current print position
G1 X220 Y-3.0 ; Go outside print area
M600 ; Filament change
M117 Remove extrusion then continue
M0 ; Pause the print
G1 R2 ; Return to saved print position


"""

        data[layer] = color_change + data[layer]
        Logger.log("d", "Added filament change before layer " + str(layer-1))

        if not finalchange:
            Logger.log("d", "Skipping addition of final filament change.")
            return data

        final_change = """


; Filament change code by PrusaFilamentChange
G1 X220 Y-3.0 ; Go outside print area
M140 S0 ; Turn off heatbed, since we're done printing
M600 ; Filament change


"""

        # The final "layer" is Cura's End G-code
        data[-1] = final_change + data[-1]
        Logger.log("d", "Added final filament change.")
        return data

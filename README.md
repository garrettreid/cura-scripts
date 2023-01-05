# cura-scripts
This is meant to become a collection of post-processing scripts for Ultimaker Cura, doing [G-code](https://en.wikipedia.org/wiki/G-code) modification of sliced models before 3D printing. At the moment, there's only one: `PrusaFilamentChange.py`.

![A dialog box showing Prusa Filament Change in Cura, with the Enabled option checked, Layer 26, and the Change after final layer option not checked.](/resources/PrusaFilamentChange.png?raw=true "PrusaFilamentChange")

## PrusaFilamentChange
This is meant to compensate for a poorly behaving filament change operation on the Prusa MK3s+. The MK3s+ implements the [M600 filament change](https://reprap.org/wiki/G-code#M600:_Filament_change_pause) operation to include an extrusion after the filament change is complete, followed by an immediate return to the printing location. If you need your first layer after filament change to be clean, dragging in some just-extruded plastic doesn't help.

`PrusaFilamentChange.py` is a G-code modification script, similar to Cura's Filament Change. It doesn't ask for most settings, since RepRap firmware ignores parameters to M600. Instead, it generates a sequence of operations at the specified layer to leave the print head paused away from the print after a filament change:
```
G60 S2 ; Save current print position
G1 X220 Y-3.0 ; Go outside print area
M600 ; Filament change
M0 Remove extrusion then continue ; Pause the print
G1 R2 ; Return to saved print position
```

To use, remove the extra extrusion after filament change pause, then resume. If you're printing over USB (e.g. OctoPrint), this won't be on the printer's UI.

If you want to include a filament swap back at the end of the print, that's also an option. Check the box, and the last thing your print will do is a filament change.

## Installation
Cura indexes post-processing scripts from its internal scripts directory and user's script directory. On macOS, that's ~/Library/Application Support/cura/**version**/scripts/. On Windows, that's \AppData\Roaming\cura\scripts.

To install a script, download it, place it in that directory, and \[re\]start Cura. Keep in mind scripts are fully functional software - you should review scripts before installing ones you don't trust!

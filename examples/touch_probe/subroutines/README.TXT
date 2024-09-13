Edit the subroutine path to SUBROUTINE_PATH = ./subroutines if it isn't already
Add a section to the main INI file for p_tool parameters

INI SECTION PARAMETERS

[TOOLSENSOR] 		(INI section descriptor)
RAPID_FEED = 30 	(initial probe feedrate)
SEARCH_FEED = 15 	(2nd probe touch feedrate)
X_PROBE_COORD = -11 (X location of sensor)
Y_PROBE_COORD = -6 	(Y location of sensor)
Z_START = -.1 		(Z start location over sensor)
Z_RETRACT_DIST = .2	(2nd (fine) probe retract distance)
Z_MAXPROBE = -2 	(Z max probe travel before it gives up)

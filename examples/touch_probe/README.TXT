USE AT YOUR OWN RISK!
Add a section to the main INI file for p_tool parameters

INI SECTION PARAMETERS

[TOOLSENSOR] 			( INI section descriptor )
LINEAR_UNITS = 1		( 1 for inch 0 for metric )
SEARCH_FEED = 30 		( initial search feedrate )
PROBE_FEED = 15 		( 2nd probe touch feedrate )
SEARCH_DIST = .5		( dist before probe gives up )
RETRACT_DIST = .2		( 2nd (fine) probe retract distance )
FINAL_DIST = .2			( dist off work after probe is done )
X_PROBE_COORD = -11		( X location of sensor )
Y_PROBE_COORD = -6 		( Y location of sensor )
Z_START = -.1 			( Z start location over sensor )
Z_MAXPROBE = -2 		( Z max probe travel before it gives up )
PROBE_HOLE_MAX_RAD = 1	( Max hole Radius to probe )
PROBE_TIP_DIAM = 6		( probe tip is in mm - most tips are metric )



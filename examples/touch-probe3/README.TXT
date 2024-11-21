USE AT YOUR OWN RISK!
Note: due to the nature of tool setter locaions and cnc setups
the p_tool.ngc has been left in for a GUIDE ONLY. Deternine what works
best for your setup. Feel free to modify these routines to your liking. 

To make user variables persistent create an entry in the .var file for each one as indicated.
2000	0.000000
2001	0.000000
. . . .
2070	0.000000

The values entered from the UI will be saved to the .var file loaded upon startup and 
updated as changes are made. The following user number variables are used or reserved
for use with these probe routines.
Some are used in the UI file and some are workspace variables.

#2000	SEARCH_FEED
#2001	FINE_FEED
#2002	SEARCH_DIST
#2003	RETRACT_DIST
#2004	XY_travel_dist
#2005	offset dist to begin corner probing  			    
#2006	X start point for corners, bolt pattern center & hole mill 			
#2007	Y start point for corners, bolt pattern center & hole mill
#2008	Z max for bar & tool
#2009	tool Z Start dist
#2010	max hole radius
#2011	max bar radius
#2012	probe tip radius calc
#2013	angle_base_dist
#2014	angle first point
#2015	Probe tip Diam from UI
#2016	var angles, dist, bar, hole
#2017	var angles, dist, bar, hole
#2018	var angles,	dist, bar, hole
#2019	var bar & hole
#2020	var dist, bar, hole
#2021	var dist, bar, hole
#2022	var bar
#2023	var bar
#2024	X Result
#2025	Y Result
#2026	Z Result
#2027	var in p_hole
#2028	var in p_hole
#2029	var in p_hole
#2030	var in p_hole
#2031	var in p_hole
#2032	angle XY search dist
#2033	setter X coord reserved
#2034	setter Y coord reserved
#2035	setter Z coord reserved
#2036	Z-safe for edge probe routines

#2037	hole pattern diameter
#2038	hole pattern hole count
#2039	hole pattern start angle
#2040	hole pattern angle increment
#2041	hole pattern start
#2042	hole pattern Z depth
#2043	hole pattern Radius
#2044 	hole pattern Feedrate
#2045 	hole pattern Clear Return point
#2046	hole pattern spindle speed

#2047	hole mill tool diameter
#2048	hole mill depth of cut
#2049	hole mill current depth step
#2050	hole mill Z Clear Return point
#2051	hole mill Z depth
#2052	hole mill diameter
#2053	hole mill feedrate
#2054	hole mill spindle speed
#2055	hole mill X start point 
#2056	hole mill Y start point 
#2057	countersink pattern angle increment additive
#2058	temp counter for restore
#2059	Q word for G83 drill cycle

#2060	tap X Center
#2061	tap Y Center
#2062	tap Z Start
#2063	tap Z Clear
#2064	tap Z Depth
#2065	tap TPI
#2066	tap IPR calculated from TPI
#2067	tap Speed
#2068	tap Feed ( for linear moves only)
#2069	reserved
#2070	reserved



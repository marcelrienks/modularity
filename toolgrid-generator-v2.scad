/******************************
* Adjustable Board Parameters
******************************/
/* [Display Mode] */
print_mode = "drawer";// [single_tile, drawer_grid]
generate_part = "tiles"; // [tiles, connector_only]

/* [Drawer Dimensions] */
drawer_width = 231;// Interior width in mm
drawer_length = 473;// Interior length in mm

/* [Tile Grid Configuration] */
tile_columns = 16; // Number of hole columns per tile (4-16)
tile_rows = 16; // Number of hole rows per tile (4-16)

/* [Hole Settings] */
pin_hole_diameter = 4.2; // Tool peg hole diameter in mm
hole_center_spacing = 9.5;// Center-to-center distance between holes in mm [8:.5:12]

/* [Material & Weight Reduction] */
use_lightweight = true; // Enable lightweight mode with cross-braces
base_thickness = 8; // Base board thickness in mm (6mm minimum)
lightweight_thickness = 4; // Thickness of cross-braces in lightweight mode [2:8]
lightweight_web_spacing = 8; // Number of holes between support webs [4:2:16]

/* [Interlocking Tabs - Tiles puzzle together with male tabs locking into female slots] */
tab_front = "female";// [male, female, none]
tab_back = "male";// [male, female, none]
tab_left = "female";// [male, female, none]
tab_right = "male";// [male, female, none]

/* [Tab Configuration - Advanced] */
tab_hole_diameter = 4; // Diameter of interlocking tab holes in mm
tab_offset = 1.52; // Distance from edge to tab center in mm
male_tab_clearance = .1; // Clearance around male tabs (mm) for fit tolerance

/* [Single Tile Trim - Only applies in single-tile mode] */
trim_width = 0;// Add/remove width in mm [-3:8]
trim_length = 0;// Add/remove length in mm [-3:8]
custom_label = ""; // Optional label for tiles

/* [Advanced Parameters] */
edge_tile_min_width = 12; // Minimum edge tile width in mm before discarding

/* [hidden] */
/*************************** 
* Text Rendering Constants
***************************/
TEXT_SIZE = 3;
TEXT_OFFSET_Y = 0.2;
TEXT_CHAR_WIDTH = 3;
CYLINDER_SEGMENTS = 20;
CIRCLE_SEGMENTS = 12;

/*************************** 
* Calculated Parameters - DO NOT EDIT
***************************/

// Map new parameter names to maintain compatibility
drawer = (print_mode == "drawer_grid");
lite = use_lightweight;
part = (generate_part == "connector_only") ? "connector" : "tiles";
label = custom_label;
num_cols = tile_columns;
num_rows = tile_rows;
hole_diameter = pin_hole_diameter;
hole_spacing = hole_center_spacing;
lite_thickness = lightweight_thickness;
web_spacing = lightweight_web_spacing;
tab_diameter = tab_hole_diameter;
tab_side = tab_offset;
tab_clearance = male_tab_clearance;
minimum_width = edge_tile_min_width;
board_thickness = base_thickness;

// Calculate the overall dimensions of the board in millimeters
board_width_mm = (num_cols) * hole_spacing + ((drawer)?0:trim_width);
board_length_mm = (num_rows) * hole_spacing + ((drawer)?0:trim_length);

// Convert dimensions from millimeters to inches
board_width_in = board_width_mm / 25.4;
board_length_in = board_length_mm / 25.4;

// Dynamic tab positioning (quarter and three-quarter points)
tab_position = [floor(num_cols * hole_spacing / 4), floor(num_cols * hole_spacing * 3 / 4)];

// calculate drawer dimensions
r_width = drawer_width%(num_cols * hole_spacing)+((drawer_width%(num_cols * hole_spacing) > minimum_width)?0:board_width_mm);
w_reduce = (drawer_width%(num_cols * hole_spacing) > minimum_width)?0:1;
r_length = drawer_length%(num_rows * hole_spacing)+((drawer_length%(num_rows * hole_spacing) > minimum_width)?0:board_width_mm);
l_reduce = (drawer_length%(num_rows * hole_spacing) > minimum_width)?0:1;
w_holes = floor(r_width/hole_spacing);
l_holes = floor(r_length/hole_spacing);

// Calculate lite dimensions
lite_offset = (hole_spacing-hole_diameter)/2-.5;

// Creates the base pegboard with holes and optional locking tab cutouts
// Parameters:
//   rows       - Number of hole rows
//   cols       - Number of hole columns  
//   board_width_mm  - Total width in mm
//   board_length_mm - Total length in mm
//   qty        - Quantity label to display (count of identical tiles)
//   tag        - Identifier text for tile type
module pegboard(rows, cols, board_width_mm=board_width_mm, board_length_mm=board_length_mm,qty=1,tag="") {
	 if(qty > 0) difference() {
        // Create the base board
        cube([board_width_mm, board_length_mm, board_thickness], center = false);
        // Create the holes
        if(rows && cols) for (row = [0 : rows - 1]) {
            for (col = [0 : cols - 1]) {
                translate([(col+.5) * hole_spacing, (row + .5) * hole_spacing, -1])
                    cylinder(h = board_thickness + 2, d = hole_diameter, $fn=CIRCLE_SEGMENTS);
            }
        }
        // create the female tabs
			if(tab_front == "female") {
				translate([0,tab_side,0]) slot(length=board_width_mm);
			}
			if(tab_back == "female" && trim_length ==0) {
				translate([0, board_length_mm-tab_side, 0]) slot(length=board_width_mm);
			}
			if(tab_left == "female") {
				translate([tab_side,0,0]) rotate([0,0,90]) slot(length=board_length_mm);
			}
			if(tab_right == "female" && trim_width ==0) {
				translate([board_width_mm-tab_side,0,0]) rotate([0,0,90]) slot(length=board_length_mm);
			}
			if(lite) {
				trim_l = (drawer?r_length%hole_spacing:trim_length);
				trim_w = (drawer?r_width%hole_spacing:trim_width);
				lite(num_cols=cols,num_rows=rows,trim_l=trim_l,trim_w=trim_w);
			}
			if(qty) {
				translate([2,TEXT_OFFSET_Y,board_thickness/2]) rotate([90,0,0]) {
					color("black") linear_extrude(height=1) text(size=TEXT_SIZE,halign="left",valign="center",text=str("x",qty));
				}
			}
			if(tag) {
				if(hole_spacing+len(tag)*TEXT_CHAR_WIDTH > board_width_mm) {
					translate([board_width_mm-.2,2,board_thickness/2]) rotate([90,0,90]) {
						color("black") linear_extrude(height=1) text(size=TEXT_SIZE,halign="left",valign="center",text=tag);
					}
				} else {
					translate([hole_spacing,TEXT_OFFSET_Y,board_thickness/2]) rotate([90,0,0]) {
						color("black") linear_extrude(height=1) text(size=TEXT_SIZE,halign="left",valign="center",text=tag);
					}
				}
			}
			if(label) {
				if(tab_position.x+len(label)*TEXT_CHAR_WIDTH > board_width_mm) {
					translate([board_width_mm-.2,(hole_spacing+len(tag)*TEXT_CHAR_WIDTH > board_width_mm?len(tag)*TEXT_CHAR_WIDTH+2:2),board_thickness/2]) rotate([90,0,90]) {
						color("black") linear_extrude(height=1) text(size=TEXT_SIZE,halign="left",valign="center",text=label);
					}
				} else {
					translate([tab_position.x+3,TEXT_OFFSET_Y,board_thickness/2]) rotate([90,0,0]) {
						color("black") linear_extrude(height=1) text(size=TEXT_SIZE,halign="left",valign="center",text=label);
					}
				}
			}
    }
}

// Adds lightweight cross-brace structure to reduce material usage
// Parameters:
//   num_cols   - Number of hole columns
//   num_rows   - Number of hole rows
//   trim_l     - Additional length offset for remainder tiles (mm)
//   trim_w     - Additional width offset for remainder tiles (mm)
module lite(num_cols,num_rows,trim_l, trim_w) {
	web_width = ceil(num_cols/web_spacing);
	web_length = ceil(num_rows/web_spacing);
	width = floor(num_cols/web_width-1)*hole_spacing;
	length = floor(num_rows/web_length-1)*hole_spacing;
	if(num_rows && num_cols) for(x = [0:1:web_width-1], y = [0:1:web_length-1]) {
		translate([lite_offset+(hole_diameter+1)/2+(width+hole_spacing)*x,lite_offset+(hole_diameter+1)/2+(length+hole_spacing)*y,lite_thickness]) linear_extrude(height=board_thickness) minkowski() {
			square([width+((x+1 == web_width)?(trim_w+hole_spacing*(num_cols%web_width)):0), length+((y+1 == web_length)?(trim_l+hole_spacing*(num_rows%web_length)):0)], center = false);
			circle(d=hole_diameter+1, $fn=CIRCLE_SEGMENTS);
		}
	}
}

// Creates male locking tabs that protrude from tile edges
// Parameters:
//   length     - Length along which tabs can be placed (mm)
module tabs(length=board_width_mm) {
	for(x=tab_position) {
		if(x+tab_diameter/2 < length)
		translate([x,0,0]) cylinder(d=tab_diameter-tab_clearance,h=board_thickness, $fn=CYLINDER_SEGMENTS);
	}
}

// Creates female slots for male tabs to lock into
// Parameters:
//   length     - Length along which slots can be placed (mm)
module slot(length=board_width_mm) {
	for(x=tab_position) {
		if(x+tab_diameter/2+1 < length) translate([x,0,-1]) cylinder(d=tab_diameter-tab_clearance,h=board_thickness+2, $fn=CYLINDER_SEGMENTS);
	}
}

// Connector piece to join two female-slot faces together
// Creates two cylindrical pegs matching the male tab dimensions
module connector() {
	offset = -(tab_diameter * 2);
	translate([offset,-tab_side,0]) cylinder(d=tab_diameter-tab_clearance,h=board_thickness, $fn=CYLINDER_SEGMENTS);
	translate([offset,tab_side,0]) cylinder(d=tab_diameter-tab_clearance,h=board_thickness, $fn=CYLINDER_SEGMENTS);
}
// Combines pegboard with male tabs to create a complete tile unit
// Parameters:
//   rows       - Number of hole rows
//   cols       - Number of hole columns
//   board_width_mm  - Total width in mm
//   board_length_mm - Total length in mm
//   tab_right  - Right edge tab configuration (passed for drawer mode)
//   tab_back   - Back edge tab configuration (passed for drawer mode)
//   qty        - Quantity label to display
//   tag        - Identifier text for tile type
module unit(rows=num_rows,cols=num_cols,board_width_mm=board_width_mm,board_length_mm=board_length_mm,tab_right=tab_right,tab_back=tab_back,qty=1,tag="") {
	if(qty > 0) { 
		// Generate the pegboard with the specified number of rows and columns
		pegboard(rows=rows,cols=cols,board_width_mm=board_width_mm,board_length_mm=board_length_mm,tag=tag,qty=qty);
		// create the male tabs
		if(tab_front == "male") {
			translate([0,-tab_side,0]) tabs(length=board_width_mm);
		}
		if(tab_back == "male" && trim_length ==0) {
			translate([0, board_length_mm + tab_side, 0]) tabs(length=board_width_mm);
		}
		if(tab_left == "male") {
			translate([-tab_side,0,0]) rotate([0,0,90]) tabs(length=board_length_mm);
		}
		if(tab_right == "male" && trim_width ==0) {
			translate([board_width_mm + tab_side,0,0]) rotate([0,0,90]) tabs(length=board_length_mm);
		}
	}
}
/**************************************
* Generate all required tiles
**************************************/
if(!drawer && part != "connector") { // Single tile mode
	unit(rows=num_rows,cols=num_cols,board_width_mm=board_width_mm,board_length_mm=board_length_mm);
} else if(drawer && part != "connector") { // Multiple tiles to fit drawer
	space = ($preview)?0:tab_diameter;
	
	// Calculate number of full tiles that fit
	full_tiles_width = floor(drawer_width/(num_cols * hole_spacing));
	full_tiles_length = floor(drawer_length/(num_rows * hole_spacing));
	
	// Calculate remainder dimensions
	remainder_width = drawer_width - (full_tiles_width * num_cols * hole_spacing);
	remainder_length = drawer_length - (full_tiles_length * num_rows * hole_spacing);
	
	// Calculate holes needed for remainder tiles
	remainder_cols = floor(remainder_width / hole_spacing);
	remainder_rows = floor(remainder_length / hole_spacing);
	
	// Actual dimensions of remainder tiles
	actual_remainder_width = remainder_cols * hole_spacing;
	actual_remainder_length = remainder_rows * hole_spacing;
	
	if($preview) {
		// Preview: Show grid layout with colors
		// Full tiles
		for(x = [0:1:full_tiles_width-1], y = [0:1:full_tiles_length-1]) {
			color(((x+y)%2?"red":"blue")) {
				translate([x*(num_cols * hole_spacing+space), y*(num_rows * hole_spacing+space), 0]) {
					unit(rows=num_rows, cols=num_cols);
				}
			}
		}
		// Remainder width tiles (right edge)
		if(remainder_cols > 0) {
			for(y = [0:1:full_tiles_length-1]) {
				color("yellow") {
					translate([full_tiles_width*(num_cols * hole_spacing+space), y*(num_rows * hole_spacing+space), 0]) {
						unit(rows=num_rows, cols=remainder_cols, board_width_mm=actual_remainder_width, tab_right="none");
					}
				}
			}
		}
		// Remainder length tiles (bottom edge)
		if(remainder_rows > 0) {
			for(x = [0:1:full_tiles_width-1]) {
				color("green") {
					translate([x*(num_cols * hole_spacing+space), full_tiles_length*(num_rows * hole_spacing+space), 0]) {
						unit(rows=remainder_rows, cols=num_cols, board_length_mm=actual_remainder_length, tab_back="none");
					}
				}
			}
		}
		// Corner tile (if both remainders exist)
		if(remainder_cols > 0 && remainder_rows > 0) {
			color("pink") {
				translate([full_tiles_width*(num_cols * hole_spacing+space), full_tiles_length*(num_rows * hole_spacing+space), 0]) {
					unit(rows=remainder_rows, cols=remainder_cols, board_width_mm=actual_remainder_width, board_length_mm=actual_remainder_length, tab_right="none", tab_back="none");
				}
			}
		}
	} else {
		// Export: Output as single combined model
		// Full tiles (base)
		if(full_tiles_width > 0 && full_tiles_length > 0) {
			unit(rows=num_rows, cols=num_cols, 
				 qty=full_tiles_width*full_tiles_length, tag="Base");
		}
		
		// Remainder width tiles (right edge)
		if(remainder_cols > 0 && full_tiles_length > 0) {
			translate([full_tiles_width*(num_cols * hole_spacing), 0, 0]) {
				unit(rows=num_rows, cols=remainder_cols, 
					 board_width_mm=actual_remainder_width, 
					 qty=full_tiles_length, tag="Side-Right", tab_right="none");
			}
		}
		
		// Remainder length tiles (bottom edge)
		if(remainder_rows > 0 && full_tiles_width > 0) {
			translate([0, full_tiles_length*(num_rows * hole_spacing), 0]) {
				unit(rows=remainder_rows, cols=num_cols, 
					 board_length_mm=actual_remainder_length, 
					 qty=full_tiles_width, tag="Side-Back", tab_back="none");
			}
		}
		
		// Corner tile (if both remainders exist)
		if(remainder_cols > 0 && remainder_rows > 0) {
			translate([full_tiles_width*(num_cols * hole_spacing), full_tiles_length*(num_rows * hole_spacing), 0]) {
				unit(rows=remainder_rows, cols=remainder_cols, 
					 board_width_mm=actual_remainder_width, 
					 board_length_mm=actual_remainder_length, 
					 tag="Corner", tab_right="none", tab_back="none");
			}
		}
	}
}

if(part != "tiles") {
	connector();
}

/******************************************
* Output details to console
******************************************/

// Output the board length and width in mm
echo("Board width: ", board_width_mm, " mm");
echo("Board length: ", board_length_mm, " mm");
// Output the board length and width in inches
echo("Board width: ", board_width_in, " inches");
echo("Board length: ", board_length_in, " inches");

// Output the total length and width in mm
echo("Total width: ", drawer_width, " mm");
echo("Total length: ", drawer_length, " mm");
// Output the total length and width in inches
echo("Total width: ", drawer_width/25.4, " inches");
echo("Total length: ", drawer_length/25.4, " inches");
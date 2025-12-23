/* 
 * Socket Tree Generator
 * Holds sockets in organized tree structure
 * Compatible with toolgrid-generator.scad peg hole pattern
 */

/* [Display Mode] */
print_mode = "single"; // [single, multi_row]

/* [Grid Integration] */
hole_center_spacing = 9.5; // [8:12]
pin_hole_diameter = 4.2; // [3:8]

/* [Drive Size] */
drive_size = "1-2"; // [1-2, 1-4, 3-8]

/* [Tree Dimensions] */
tree_width = 45; // [30:60]
tree_height = 60; // [40:80]
tree_depth = 15; // [10:30]

/* [Socket Configuration] */
socket_diameter = 8; // [5:15] - Socket hole diameter
num_socket_rows = 3; // [1:5] - Number of rows
sockets_per_row = 4; // [2:8] - Sockets per row

/* [Pin Configuration] */
pin_diameter = 4.0; // [3:6]
num_pins_x = 2; // [1:4]
num_pins_y = 2; // [1:4]

/* [Rotation] */
holder_rotation = 0; // [0:360]

/* [Wall Thickness] */
wall_thickness = 3; // [2:5]
floor_thickness = 2; // [1:4]

/* [Advanced] */
pin_offset_from_edge = 3; // [1:8]

// ===== CALCULATED PARAMETERS =====
pin_spacing_x = tree_width / (num_pins_x + 1);
pin_spacing_y = tree_height / (num_pins_y + 1);
socket_spacing_x = tree_width / (sockets_per_row + 1);
socket_spacing_y = tree_height / (num_socket_rows + 1);

// ===== MAIN MODULES =====

module socket_hole(x, y) {
    translate([x, y, -1]) {
        cylinder(d=socket_diameter, h=tree_depth + 2, $fn=20);
    }
}

module tree_base() {
    difference() {
        cube([tree_width, tree_height, tree_depth]);
        
        // Create socket holes in grid pattern
        for (row = [1:num_socket_rows]) {
            for (col = [1:sockets_per_row]) {
                socket_hole(
                    col * socket_spacing_x,
                    row * socket_spacing_y
                );
            }
        }
        
        // Support pins cutouts
        for (x = [1:num_pins_x]) {
            for (y = [1:num_pins_y]) {
                pin_x = x * pin_spacing_x;
                pin_y = y * pin_spacing_y;
                translate([pin_x, pin_y, pin_offset_from_edge]) {
                    cylinder(d=pin_diameter, h=tree_depth, $fn=20);
                }
            }
        }
    }
    
    // Support pins
    for (x = [1:num_pins_x]) {
        for (y = [1:num_pins_y]) {
            pin_x = x * pin_spacing_x;
            pin_y = y * pin_spacing_y;
            translate([pin_x, pin_y, 0]) {
                cylinder(d=pin_diameter, h=pin_offset_from_edge + pin_diameter/2, $fn=20);
            }
        }
    }
}

module mounting_pegs() {
    peg_diameter = pin_hole_diameter - 0.2;
    peg_height = 5;
    
    translate([pin_diameter/2 + wall_thickness, tree_height/2, 0]) {
        cylinder(d=peg_diameter, h=peg_height, $fn=20);
    }
    translate([tree_width - wall_thickness - pin_diameter/2, tree_height/2, 0]) {
        cylinder(d=peg_diameter, h=peg_height, $fn=20);
    }
}

module complete_tree() {
    translate([tree_width/2, tree_height/2, 0]) {
        rotate([0, 0, holder_rotation]) {
            translate([-tree_width/2, -tree_height/2, 0]) {
                tree_base();
            }
        }
    }
    mounting_pegs();
}

// ===== GENERATION =====

if (print_mode == "single") {
    complete_tree();
} else if (print_mode == "multi_row") {
    spacing = hole_center_spacing * 3;
    for (i = [0:2]) {
        translate([i * spacing, 0, 0]) {
            complete_tree();
        }
    }
}

// ===== DEBUG OUTPUT =====
echo("=== Socket Tree Generator ===");
echo("Drive size: ", drive_size);
echo("Tree dimensions: ", tree_width, "×", tree_height, "×", tree_depth, "mm");
echo("Sockets: ", num_socket_rows, " rows × ", sockets_per_row, " per row");
echo("Socket diameter: ", socket_diameter, "mm");
echo("Support pins: ", num_pins_x, "×", num_pins_y);
echo("Rotation: ", holder_rotation, "°");

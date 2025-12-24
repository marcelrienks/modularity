/******************************
 * Ratchet Holder Generator
 * Parametric ratchet holder for pegboard integration
 * Compatible with toolgrid-generator.scad
 ******************************/

/* [Display Mode] */
print_mode = "single"; // [single, multi_row]

/* [Grid Integration] */
hole_center_spacing = 9.5; // [8:12]
pin_hole_diameter = 4.2; // [3:8]

/* [Drive Size] */
drive_size = "1-4"; // [1-4, 3-8]

/* [Housing Dimensions] */
// Auto-calculated based on drive_size, but can be overridden
housing_width = (drive_size == "1-4") ? 29.5 : 31.75; // [20:40]
housing_height = (drive_size == "1-4") ? 13 : 17.5; // [10:30]
housing_depth = (drive_size == "1-4") ? 21.1 : 24.4; // [15:50]

/* [Cavity Dimensions] */
// Auto-calculated based on drive_size, but can be overridden
cavity_width = (drive_size == "1-4") ? 18 : 22; // [10:30]
cavity_height = (drive_size == "1-4") ? 9 : 13; // [6:20]

/* [Pin Configuration] */
pin_diameter = 4.0; // [3:6]
num_pins_x = 2; // [1:4]
num_pins_y = 2; // [1:4]

/* [Rotation] */
holder_rotation = 0; // [0:360]

/* [Wall Thickness] */
wall_thickness = 3; // [2:5]
floor_thickness = 4; // [1:4]

/* [Mounting Pegs] */
peg_diameter = 3.8; // [2.5:5]
peg_height = 6; // [3:10]

/* [Advanced] */
pin_offset_from_edge = 3; // [1:8]
fillet_radius = 1; // [0:3]

// ===== CALCULATED PARAMETERS =====

// Calculate total housing dimensions in local coordinate system
// The mounting pegs extend downward from Z=0
total_housing_width = housing_width;
total_housing_height = housing_height;
total_housing_depth = housing_depth;

// Pin spacing for support pins inside the cavity
pin_spacing_x = (housing_width - 2 * wall_thickness) / (num_pins_x + 1);
pin_spacing_y = (housing_height - 2 * wall_thickness) / (num_pins_y + 1);

// Cavity position (centered within housing)
cavity_x = wall_thickness + (housing_width - 2 * wall_thickness - cavity_width) / 2;
cavity_y = wall_thickness + (housing_height - 2 * wall_thickness - cavity_height) / 2;
cavity_z = floor_thickness;

// ===== MODULES =====

/**
 * Basic housing block with cavity subtracted
 */
module housing_body() {
    difference() {
        // Solid block
        cube([housing_width, housing_height, housing_depth]);
        
        // Main cavity for ratchet head
        translate([cavity_x, cavity_y, cavity_z]) {
            cube([cavity_width, cavity_height, housing_depth]);
        }
        
        // Support pins (drilled holes through the cavity)
        for (x = [1:num_pins_x]) {
            for (y = [1:num_pins_y]) {
                pin_x = wall_thickness + pin_spacing_x * x;
                pin_y = wall_thickness + pin_spacing_y * y;
                translate([pin_x, pin_y, floor_thickness - 0.1]) {
                    cylinder(d=pin_diameter, h=housing_depth, $fn=20);
                }
            }
        }
    }
}

/**
 * Mounting pegs that extend downward to attach to pegboard
 * Positioned at corners with inset from edges
 */
module mounting_pegs() {
    peg_inset = wall_thickness + pin_diameter / 2;
    
    // Front-left
    translate([peg_inset, peg_inset, 0]) {
        cylinder(d=peg_diameter, h=-peg_height, $fn=20);
    }
    
    // Front-right
    translate([housing_width - peg_inset, peg_inset, 0]) {
        cylinder(d=peg_diameter, h=-peg_height, $fn=20);
    }
    
    // Back-left
    translate([peg_inset, housing_height - peg_inset, 0]) {
        cylinder(d=peg_diameter, h=-peg_height, $fn=20);
    }
    
    // Back-right
    translate([housing_width - peg_inset, housing_height - peg_inset, 0]) {
        cylinder(d=peg_diameter, h=-peg_height, $fn=20);
    }
}

/**
 * Complete holder with rotation applied
 * Rotation is applied around the center of the housing footprint
 */
module complete_holder() {
    translate([housing_width / 2, housing_height / 2, 0]) {
        rotate([0, 0, holder_rotation]) {
            translate([-housing_width / 2, -housing_height / 2, 0]) {
                housing_body();
                mounting_pegs();
            }
        }
    }
}

/**
 * Multiple holders arranged for batch printing
 */
module multi_row_holders() {
    spacing = hole_center_spacing * 2.5;
    for (i = [0:3]) {
        translate([i * spacing, 0, 0]) {
            complete_holder();
        }
    }
}

// ===== GENERATION =====

if (print_mode == "single") {
    complete_holder();
} else if (print_mode == "multi_row") {
    multi_row_holders();
}

// ===== DEBUG OUTPUT =====
echo("=== Ratchet Holder Generator ===");
echo("Drive size: ", drive_size);
echo("Housing dimensions: ", housing_width, "×", housing_height, "×", housing_depth, "mm");
echo("Cavity dimensions: ", cavity_width, "×", cavity_height, "mm");
echo("Support pins: ", num_pins_x, "×", num_pins_y, " at spacing ", pin_spacing_x, "×", pin_spacing_y);
echo("Mounting pegs: 4 at corners, diameter ", peg_diameter, "mm, height ", peg_height, "mm");
echo("Rotation: ", holder_rotation, "°");

/* 
 * Wrench Holder Generator
 * Holds wrenches in various sizes
 * Compatible with toolgrid-generator.scad peg hole pattern
 */

/* [Display Mode] */
print_mode = "single"; // [single, multi_row]

/* [Grid Integration] */
hole_center_spacing = 9.5; // [8:12]
pin_hole_diameter = 4.2; // [3:8]

/* [Wrench Size] */
wrench_size = "large"; // [small, large]
width_offset = 0; // [-5:5] - Fine-tune width

/* [Housing Dimensions] */
housing_width = 40; // [25:55]
housing_height = 30; // [20:45]
housing_depth = 45; // [30:70]

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
fillet_radius = 1; // [0:3]

// ===== CALCULATED PARAMETERS =====
final_width = housing_width + width_offset;
pin_spacing_x = final_width / (num_pins_x + 1);
pin_spacing_y = housing_height / (num_pins_y + 1);

// ===== MAIN MODULES =====

module holder_base() {
    difference() {
        cube([final_width, housing_height, housing_depth]);
        
        translate([
            (final_width - 20) / 2,
            (housing_height - 15) / 2,
            floor_thickness
        ]) {
            cube([20, 15, housing_depth]);
        }
        
        for (x = [1:num_pins_x]) {
            for (y = [1:num_pins_y]) {
                pin_x = x * pin_spacing_x;
                pin_y = y * pin_spacing_y;
                translate([pin_x, pin_y, pin_offset_from_edge]) {
                    cylinder(d=pin_diameter, h=housing_depth, $fn=20);
                }
            }
        }
    }
    
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
    
    translate([pin_diameter/2 + wall_thickness, housing_height/2, 0]) {
        cylinder(d=peg_diameter, h=peg_height, $fn=20);
    }
    translate([final_width - wall_thickness - pin_diameter/2, housing_height/2, 0]) {
        cylinder(d=peg_diameter, h=peg_height, $fn=20);
    }
}

module complete_holder() {
    translate([final_width/2, housing_height/2, 0]) {
        rotate([0, 0, holder_rotation]) {
            translate([-final_width/2, -housing_height/2, 0]) {
                holder_base();
            }
        }
    }
    mounting_pegs();
}

// ===== GENERATION =====

if (print_mode == "single") {
    complete_holder();
} else if (print_mode == "multi_row") {
    spacing = hole_center_spacing * 2.5;
    for (i = [0:3]) {
        translate([i * spacing, 0, 0]) {
            complete_holder();
        }
    }
}

// ===== DEBUG OUTPUT =====
echo("=== Wrench Holder Generator ===");
echo("Size: ", wrench_size);
echo("Housing: ", final_width, "×", housing_height, "×", housing_depth, "mm");
echo("Support pins: ", num_pins_x, "×", num_pins_y);
echo("Rotation: ", holder_rotation, "°");

"""CadQuery-based handle geometry builder."""

import math
import cadquery as cq


def _tan_deg(degrees: float) -> float:
    """Return tangent of angle in degrees."""
    return math.tan(math.radians(degrees))


class HandleBuilder:
    """Build 3D handle geometry from parameters using CadQuery."""

    # Outward flare angle of cradle walls (degrees from vertical)
    WALL_ANGLE_DEG = 20.0

    def __init__(self, params):
        """Initialize builder with parameters."""
        self.params = params
        self.shape = None

    def build(self):
        """Build the handle geometry and return CadQuery Shape object.

        Geometry (matches reference model image):
          - Rectangular stem at base: square cross-section, mounts to ToolGrid surface.
          - Cradle above stem: flat floor with central mounting hole, four walls
            angled outward (flared) by WALL_ANGLE_DEG, height = user height param.
          - User 'diameter' sets the inner cradle width; stem size derived from it.
        """
        d = self.params.diameter   # grip diameter (mm)
        h = self.params.height     # cradle wall height (mm)

        ref = self.params.REFERENCE_PARAMS
        fillet_r = ref["d165"]          # 0.3 mm — edge fillet radius
        mount_hole_d = ref["d176"]      # 2.6 mm — mounting hole diameter
        floor_t = ref["d144"]           # 0.6 mm — cradle floor thickness

        # Derived dimensions
        stem_size = d * 0.5             # stem square side length
        stem_h = d * 0.4               # stem height
        floor_size = d * 0.6           # cradle floor square side length
        top_size = floor_size + 2 * h * _tan_deg(self.WALL_ANGLE_DEG)

        wall_z_bottom = stem_h + floor_t
        wall_z_top = wall_z_bottom + h

        # ── Stem (square prism) ────────────────────────────────────────────────
        stem = (
            cq.Workplane("XY")
            .box(stem_size, stem_size, stem_h, centered=(True, True, False))
        )

        # ── Cradle floor (square slab with central mounting hole) ──────────────
        floor = (
            cq.Workplane("XY")
            .workplane(offset=stem_h)
            .rect(floor_size, floor_size)
            .extrude(floor_t)
            .faces(">Z")
            .workplane()
            .circle(mount_hole_d / 2)
            .cutThruAll()
        )

        # ── Cradle walls (loft from floor square to wider top square) ──────────
        cradle = (
            cq.Workplane("XY")
            .workplane(offset=wall_z_bottom)
            .rect(floor_size, floor_size)
            .workplane(offset=wall_z_top)
            .rect(top_size, top_size)
            .loft()
        )

        # ── Union all three parts ──────────────────────────────────────────────
        result = stem.union(floor).union(cradle)

        # ── Fillet outer vertical edges of stem (skip if fillet corrupts shape) ─
        try:
            filleted = result.edges("|Z").fillet(fillet_r)
            if filleted.val().isValid():
                result = filleted
        except Exception:
            pass

        self.shape = result.val()
        return self.shape

    def validate(self) -> bool:
        """Check geometric validity (watertight, no self-intersections)."""
        if self.shape is None:
            return False
        try:
            if not self.shape.isValid():
                return False
            if hasattr(self.shape, 'isClosed'):
                return self.shape.isClosed()
            return True
        except Exception:
            return False

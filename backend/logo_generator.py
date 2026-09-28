import cadquery as cq

def create_logo():

    outer = (
        cq.Workplane("XY")
        .circle(12)
        .extrude(.8)
    )

    inner = (
        cq.Workplane("XY")
        .circle(6)
        .extrude(.8)
    )

    logo = outer.cut(inner)

    return logo
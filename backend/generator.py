import cadquery as cq
import os

from logo_builder import generate_logo_geometry


LAYOUT = {

    "name_x": 0,
    "name_y": 0,

    "title_x": 0,
    "title_y": -20,

    "logo_x": 90,
    "logo_y": 20,
    "logo_width": 60
}


def build_plate(
    name,
    title="",
    logo_path=None,
    graphics=None
):

    if graphics is None:
        graphics = []

    os.makedirs(
        "outputs",
        exist_ok=True
    )


    # Base plate

    plate_width = 254
    plate_height = 64
    plate_thickness = 1.5
    
    plate = (
        cq.Workplane("XY")
        .rect(
        plate_width,
        plate_height
        )
        .extrude(
        plate_thickness
        )
        .edges("|Z")
        .fillet(3)
    )

    model = plate

    # Name

    name_text = (
        cq.Workplane("XY")
        .workplane(offset=1.51)
        .center(
            LAYOUT["name_x"],
            LAYOUT["name_y"]
        )
        .text(
            txt=name,
            fontsize=24,
            distance=2,
            font="Source Sans Pro"
        )
    )

    model = model.union(
        name_text
    )

    # Title

    if title and title.strip():

        title_text = (
            cq.Workplane("XY")
            .workplane(offset=1.51)
            .center(
                LAYOUT["title_x"],
                LAYOUT["title_y"]
            )
            .text(
                txt=title,
                fontsize=16,
                distance=1,
                font="Source Sans Pro"
            )
        )

        model = model.union(
            title_text
        )

    # Dedicated Logo Position

    if logo_path:

        try:

            print(
                "Using logo:",
                logo_path
            )

            logo = generate_logo_geometry(
                logo_path,
                target_width=LAYOUT["logo_width"]
            )

            logo = (
                logo
                .translate(
                    (
                        LAYOUT["logo_x"],
                        LAYOUT["logo_y"],
                        1.5
                    )
                )
            )

            model = model.union(
                logo
            )

        except Exception as e:

            print(
                "Logo generation failed:",
                e
            )

    # Additional Graphics

    for graphic in graphics:

        try:

            graphic_path = graphic["path"]

            graphic_x = graphic.get(
                "x",
                0
            )

            graphic_y = graphic.get(
                "y",
                0
            )

            graphic_width = graphic.get(
                "width",
                40
            )

            graphic_rotation = graphic.get(
                "rotation",
                0
            )

            shape = generate_logo_geometry(
                graphic_path,
                target_width=graphic_width
            )

            if graphic_rotation != 0:

                shape = shape.rotate(
                    (0, 0, 0),
                    (0, 0, 1),
                    graphic_rotation
                )

            shape = shape.translate(
                (
                    graphic_x,
                    graphic_y,
                    1.5
                )
            )

            model = model.union(
                shape
            )

        except Exception as e:

            print(
                "Graphic generation failed:",
                e
            )

    filename = f"outputs/{name}.stl"

    cq.exporters.export(
        model,
        filename
    )

    return filename
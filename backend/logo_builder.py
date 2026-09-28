from contour_to_cad import contour_to_logo


def generate_logo_geometry(
    path,
    scale_factor=1.0,
    target_width=40
):

    return contour_to_logo(
        path,
        target_width * scale_factor
    )
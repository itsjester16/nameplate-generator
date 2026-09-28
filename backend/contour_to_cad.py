import cv2
import cadquery as cq


def contour_depth(hierarchy, index):

    depth = 0

    parent = hierarchy[0][index][3]

    while parent != -1:

        depth += 1
        parent = hierarchy[0][parent][3]

    return depth


def contour_to_logo(
    image_path,
    target_width=40,
    thickness=.8
):

    image = cv2.imread(
        image_path,
        cv2.IMREAD_GRAYSCALE
    )

    if image is None:
        raise ValueError(
            f"Could not load image: {image_path}"
        )

    # Increase resolution before contour extraction

    image = cv2.resize(
        image,
        None,
        fx=4,
        fy=4,
        interpolation=cv2.INTER_CUBIC
    )

    # Light smoothing

    image = cv2.GaussianBlur(
        image,
        (3, 3),
        0
    )

    # More forgiving threshold

    _, binary = cv2.threshold(
        image,
        100,
        255,
        cv2.THRESH_BINARY_INV
    )

    # Reconnect thin line segments

    kernel = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE,
        (3, 3)
    )

    binary = cv2.morphologyEx(
        binary,
        cv2.MORPH_CLOSE,
        kernel
    )

    # Debug image
    cv2.imwrite(
        "outputs/debug_binary.png",
        binary
    )

    contours, hierarchy = cv2.findContours(
        binary,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_NONE
    )

    if hierarchy is None:
        raise ValueError(
            "No contours found."
        )

    valid_indices = []

    for i, contour in enumerate(contours):

        if cv2.contourArea(contour) > 100:
            valid_indices.append(i)

    if not valid_indices:
        raise ValueError(
            "No valid contours found."
        )

    print(
        "Valid contours:",
        len(valid_indices)
    )

    # Calculate overall logo bounds

    all_points = []

    for i in valid_indices:

        contour = contours[i]

        for point in contour:
            all_points.append(point)

    all_x = [
        p[0][0]
        for p in all_points
    ]

    all_y = [
        p[0][1]
        for p in all_points
    ]

    min_x = min(all_x)
    max_x = max(all_x)

    min_y = min(all_y)
    max_y = max(all_y)

    logo_width = max_x - min_x

    if logo_width == 0:
        raise ValueError(
            "Logo width is zero."
        )

    scale = target_width / logo_width

    center_x = (
        min_x + max_x
    ) / 2

    center_y = (
        min_y + max_y
    ) / 2

    contour_shapes = {}

    for i in valid_indices:

        contour = contours[i]

        # Preserve much more detail

        epsilon = (
            0.0005
            * cv2.arcLength(
                contour,
                True
            )
        )

        contour = cv2.approxPolyDP(
            contour,
            epsilon,
            True
        )

        points = []

        for point in contour:

            x = (
                point[0][0]
                - center_x
            ) * scale

            y = (
                center_y
                - point[0][1]
            ) * scale

            points.append(
                (
                    float(x),
                    float(y)
                )
            )

        if len(points) < 3:
            continue

        try:

            shape = (
                cq.Workplane("XY")
                .polyline(points)
                .close()
                .extrude(thickness)
            )

            contour_shapes[i] = shape

        except Exception as e:

            print(
                f"Skipped contour {i}: {e}"
            )

    if not contour_shapes:
        raise ValueError(
            "No geometry created."
        )

    combined_logo = None

    for i in valid_indices:

        if i not in contour_shapes:
            continue

        shape = contour_shapes[i]

        depth = contour_depth(
            hierarchy,
            i
        )

        try:

            if combined_logo is None:

                combined_logo = shape

            elif depth % 2 == 0:

                combined_logo = (
                    combined_logo
                    .union(shape)
                )

            else:

                combined_logo = (
                    combined_logo
                    .cut(shape)
                )

        except Exception as e:

            print(
                f"Boolean operation failed on contour {i}: {e}"
            )

    if combined_logo is None:
        raise ValueError(
            "Failed to create logo geometry."
        )

    return combined_logo
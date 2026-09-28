import cv2


def get_contours(image_path):

    image = cv2.imread(
        image_path,
        cv2.IMREAD_GRAYSCALE
    )

    _, binary = cv2.threshold(
        image,
        127,
        255,
        cv2.THRESH_BINARY_INV
    )

    contours, _ = cv2.findContours(
        binary,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    return contours


def save_contour_preview(
    image_path,
    output_path
):

    print("================================")
    print("Processing Logo")
    print("Image Path:", image_path)
    print("Output Path:", output_path)
    print("================================")

    image = cv2.imread(
        image_path,
        cv2.IMREAD_COLOR
    )

    if image is None:
        raise Exception(
            f"OpenCV could not load: {image_path}"
        )

    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    _, binary = cv2.threshold(
        gray,
        127,
        255,
        cv2.THRESH_BINARY_INV
    )

    contours, _ = cv2.findContours(
        binary,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    contours = [
        c for c in contours
        if cv2.contourArea(c) > 100
    ]

    print("Contours found:", len(contours))

    debug = image.copy()

    cv2.drawContours(
        debug,
        contours,
        -1,
        (0, 255, 0),
        2
    )

    cv2.imwrite(
        output_path,
        debug
    )

    print(
        "Saved contour preview:",
        output_path
    )

    return len(contours)
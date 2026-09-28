from PIL import Image
from PIL import ImageDraw
import os

def create_preview(
    name,
    title,
    logo_path=None,
    image_path=None
):

    width = 900
    height = 300

    img = Image.new(
        "RGB",
        (width, height),
        "white"
    )

    draw = ImageDraw.Draw(img)

    draw.rectangle(
        [(10, 10), (890, 290)],
        outline="black",
        width=4
    )

    draw.text(
        (350, 100),
        name,
        fill="black"
    )

    draw.text(
        (320, 180),
        title,
        fill="black"
    )

    if logo_path and os.path.exists(logo_path):

        logo = Image.open(logo_path)

        logo.thumbnail((120, 120))

        img.paste(
            logo,
            (40, 90)
        )
    
    if image_path and os.path.exists(image_path):

        aircraft = Image.open(image_path)

        aircraft.thumbnail((180, 120))

        img.paste(
            aircraft,
            (650, 90)
        )
        
    
    filename = f"outputs/{name}_preview.png"

    img.save(filename)

    return filename
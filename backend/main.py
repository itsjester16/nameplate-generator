import json

from fastapi import FastAPI
from fastapi import Form
from fastapi import File
from fastapi import UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from generator import build_plate
from image_processor import save_upload
from preview_generator import create_preview
from logo_to_geometry import save_contour_preview


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.post("/generate")
async def generate(
    name: str = Form(...),
    title: str = Form(""),
    graphics_config: str = Form("[]"),
    logo: UploadFile | None = File(None),
    graphics: list[UploadFile] = File([])
):

    logo_path = None

    if logo is not None:

        logo_path = save_upload(
            logo,
            "uploads/logos"
        )

        print(
            "Logo saved:",
            logo_path
        )

        count = save_contour_preview(
            logo_path,
            f"outputs/{name}_contours.png"
        )

        print(
            "Contour count:",
            count
        )

    try:

        graphic_settings = json.loads(
            graphics_config
        )

    except Exception:

        graphic_settings = []

    graphic_paths = []

    for graphic in graphics:

        path = save_upload(
            graphic,
            "uploads/images"
        )

        graphic_paths.append(path)

        print(
            "Graphic saved:",
            path
        )

    graphics_data = []

    for i, path in enumerate(
        graphic_paths
    ):

        settings = {}

        if i < len(
            graphic_settings
        ):
            settings = graphic_settings[i]

        graphics_data.append({
            "path": path,
            "x": settings.get(
                "x",
                65
            ),
            "y": settings.get(
                "y",
                10
            ),
            "width": settings.get(
                "width",
                45
            )
        })

    print(
        "Graphics data:",
        graphics_data
    )

    filename = build_plate(
        name=name,
        title=title,
        logo_path=logo_path,
        graphics=graphics_data
    )

    first_graphic = None

    if len(graphic_paths) > 0:
        first_graphic = graphic_paths[0]

    create_preview(
        name=name,
        title=title,
        logo_path=logo_path,
        image_path=first_graphic
    )

    return FileResponse(
        path=filename,
        media_type="application/octet-stream",
        filename=f"{name}.stl"
    )
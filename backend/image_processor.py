import os

def save_upload(upload_file, folder):

    os.makedirs(folder, exist_ok=True)

    file_path = os.path.join(
        folder,
        upload_file.filename
    )

    with open(file_path, "wb") as buffer:
        buffer.write(
            upload_file.file.read()
        )

    return file_path
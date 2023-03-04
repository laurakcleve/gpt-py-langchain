import os
from datetime import datetime
import json


def log(data, file_type="txt", suffix=None):
    timestamp_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    if file_type == "json":
        data = json.dumps(data)

    file_name = (
        f"./output/{timestamp_str}"
        + (f"_{suffix}" if suffix is not None else "")
        + "."
        + file_type
    )
    with open(file_name, "w") as f:
        f.write(data)


def log_chunks(chunks):
    # Create folder structure based on timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_folder = f"output/chunks/{timestamp}"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop over chunks and write each one to its own file in the output folder
    for i, chunk in enumerate(chunks):
        filename = f"chunk_{i}.txt"
        filepath = os.path.join(output_folder, filename)
        with open(filepath, "w") as file:
            file.write(chunk.page_content)

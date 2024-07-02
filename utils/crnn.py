import os
import shutil


def rename_images_from_txt(txt_file_path):
    with open(txt_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for i, line in enumerate(lines):
        parts = line.strip().split()
        if len(parts) < 2:
            print(f"Line {i + 1} is malformed: {line}")
            continue

        image_path = parts[0]
        license_plate = parts[1]
        new_file_name = f"{license_plate}_{i}.jpg"

        new_directory = os.path.dirname(new_image_path)
        new_file_path = os.path.join(new_directory, new_file_name)

        try:
            shutil.copy(os.path.join("./NumberData", image_path), os.path.join("./Format_Data", new_file_path))
            print(f"Renamed {image_path} to {new_file_path}")
        except FileNotFoundError:
            print(f"File not found: {image_path}")
        except Exception as e:
            print(f"Error renaming file {image_path}: {e}")


# Example usage
txt_file_path = 'NumberData/data.txt'  # replace with your txt file path
new_image_path = "./Format_Data"
rename_images_from_txt(txt_file_path)

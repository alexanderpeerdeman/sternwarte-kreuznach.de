from slugify import slugify
from datetime import datetime, timedelta
from pathlib import Path
import re
import json
import html2text
import requests
import shutil
import yaml


def find_image(data, talk):
    image_id = int(talk["BildID"])
    file_database = data[43]["data"]

    result = [entry for entry in file_database if int(entry["ID"]) == image_id]

    assert len(result) <= 1
    return result


def find_speakers(talk):
    # Not every talk has a speaker
    talk_id = int(talk["ID"])
    relations = data[97]["data"]

    ref_strings = []

    for relation in relations:
        if int(relation["VortragID"]) == talk_id:
            speakers_database = data[68]["data"]

            for entry in speakers_database:
                if int(entry["ID"]) == int(relation["ReferentID"]):
                    ref_strings.append(entry["Title"])

    return ref_strings


def write_file(talk_folder, yaml_dict, talk_content):
    with open(talk_folder + "/" + "index.md", "w") as md:
        markdown_output = [
            "---\n",
            yaml.dump(yaml_dict, allow_unicode=True),
            "---\n",
            talk_content
        ]
        md.writelines(markdown_output)


def find_content(talk):

    talk_content = ""

    if talk["Content"] is not None:
        original_stripped = html2text.html2text(talk["Content"])

        talk_content = re.sub(
            r'(?<!\n)\n(?![\n\t])', ' ', original_stripped.replace('\r', ''))
    return talk_content


if __name__ == "__main__":

    with open("db1033256-1.json", "r") as json_file:
        data = json.load(json_file)

        for talk in data[88]["data"]:

            yaml_dict = {}

            talk_created = datetime.strptime(
                talk["Created"], '%Y-%m-%d %H:%M:%S')

            talk_date = datetime.strptime(talk["Datum"], '%Y-%m-%d')

            talk_speakers = find_speakers(talk)

            if len(talk_speakers) > 0:
                yaml_dict["talk_speakers"] = []

                for speaker in talk_speakers:
                    yaml_dict["talk_speakers"].append(speaker)

            yaml_dict["title"] = talk["Title"]

            friendly_name = slugify(yaml_dict["title"], max_length=255, replacements=[
                ['Ä', 'AE'], ['ä', 'ae'],
                ['Ö', 'OE'], ['ö', 'oe'],
                ['Ü', 'UE'], ['ü', 'ue'],
                ['ß', 'ss'],
            ])

            talk_folder = "../content/vhs/{}/{}".format(
                talk_date.year, friendly_name)
            Path(talk_folder).mkdir(parents=True, exist_ok=True)

            # Find corresponding image and download it
            image_object = find_image(data, talk)
            downloaded_image = False

            if len(image_object) > 0:
                image_file_location = image_object[0]["FileFilename"]
                new_image_file_name = talk_folder + "/" + friendly_name + "-title" + \
                    "." + image_file_location.split(".")[-1].lower()

                image_file_name = image_object[0]["Name"]
                image_file_title = image_object[0]["Title"]

                if not Path(new_image_file_name).is_file():
                    download_url = "https://sternwarte-kreuznach.de/assets/" + image_file_location

                    r = requests.get(download_url, stream=True)

                    if r.status_code == 200:
                        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                        r.raw.decode_content = True

                        # Open a local file with wb ( write binary ) permission.
                        with open(new_image_file_name, 'wb') as f:
                            shutil.copyfileobj(r.raw, f)

                        downloaded_image = True

                    else:
                        print('Image could not be retreived!')

                yaml_dict["talk_images"] = []
                yaml_dict["talk_images"].append(
                    new_image_file_name.split("/")[-1])

            yaml_dict["date"] = talk_created.isoformat()
            yaml_dict["talk_date"] = talk_date.isoformat()

            write_file(talk_folder, yaml_dict, find_content(talk))

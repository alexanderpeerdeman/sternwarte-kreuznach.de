from slugify import slugify
from datetime import datetime
from pathlib import Path
import re
import json
import html2text
import requests
import shutil


def find_image(data, id):
    file_database = data[43]["data"]

    for entry in file_database:
        if int(entry["ID"]) == id:
            return entry


def find_speakers(talk_id):

    # Not every talk has a speaker

    talk_id = int(talk_id)
    print("\n#### VortragID:", talk_id)
    relations = data[97]["data"]

    ref_strings = []

    for relation in relations:
        if int(relation["VortragID"]) == talk_id:
            speakers_database = data[68]["data"]

            for entry in speakers_database:
                if int(entry["ID"]) == int(relation["ReferentID"]):
                    print(entry["Title"])
                    ref_strings.append(entry["Title"])

    return ref_strings


if __name__ == "__main__":

    with open("db1033256-1.json", "r") as json_file:
        data = json.load(json_file)

        for talk in data[88]["data"]:
            talk_content = ""
            if talk["Content"] is not None:
                original_stripped = html2text.html2text(talk["Content"])

                talk_content = re.sub(
                    r'(?<!\n)\n(?![\n\t])', ' ', original_stripped.replace('\r', ''))

            talk_created = datetime.strptime(
                talk["Created"], '%Y-%m-%d %H:%M:%S')

            talk_date = datetime.strptime(talk["Datum"], '%Y-%m-%d')

            talk_speakers = find_speakers(talk["ID"])

            talk_title = talk["Title"]
            print(talk_title)
            talk_start = talk["UhrzeitAnfang"]
            talk_price = "{} (Ermäßigt: {})".format(
                talk["PreisAmount"], talk["PreisErmAmount"])
            talk_is_supplementary = talk["IsZusatz"]
            talk_is_sparse = talk["KeineDetails"]

            friendly_name = slugify(talk_title, replacements=[
                ['Ä', 'AE'], ['ä', 'ae'],
                ['Ö', 'OE'], ['ö', 'oe'],
                ['Ü', 'UE'], ['ü', 'ue'],
                ['ß', 'ss'],
            ])

            if talk_date < datetime(2005, 1, 1):
                continue

            talk_folder = "../content/vhs/{}/{}".format(
                talk_date.year, friendly_name)
            Path(talk_folder).mkdir(parents=True, exist_ok=True)

            # Find corresponding image and download it
            talk_image_id = int(talk["BildID"])
            image_object = find_image(data, talk_image_id)
            downloaded_image = False

            if image_object is not None:
                image_file_location = image_object["FileFilename"]
                new_image_file_name = talk_folder + "/" + friendly_name + "-title" + \
                    "." + image_file_location.split(".")[-1].lower()

                image_file_name = image_object["Name"]
                image_file_title = image_object["Title"]

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
                else:
                    downloaded_image = True

            markdown_output = [
                "---\n",
                'title: "{}"\n'.format(talk_title)
            ]

            # TODO Check for date in theme and display accordingly
            markdown_output += "talk_date: {}\n".format(talk_date.isoformat())

            if len(talk_speakers) > 0:
                markdown_output += "talk_speakers:\n"

                for speaker in talk_speakers:
                    markdown_output += "    - {}\n".format(speaker)

            if downloaded_image:
                markdown_output += [
                    "images:\n    - {}\n".format(
                        new_image_file_name.split("/")[-1])
                ]

            markdown_output += [
                "date: {}\n".format(talk_created.isoformat()),
                "---\n",
                talk_content
            ]

            with open(talk_folder + "/" + "index.md", "w") as md:
                md.writelines(markdown_output)

from slugify import slugify
from datetime import datetime, timedelta
from pathlib import Path
import re
import json
import html2text
import requests
import shutil
import yaml


def find_image(data, id):
    file_database = data[43]["data"]

    result = [entry for entry in file_database if int(entry["ID"]) == id]

    assert len(result) <= 1
    return result


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

            talk_start = talk["UhrzeitAnfang"]

            if talk_start is not None:
                talk_start_precise = [int(e) for e in talk_start.split(":")]
                print(talk_start_precise)
                talk_start_time_offset = timedelta(
                    hours=talk_start_precise[0], minutes=talk_start_precise[1], seconds=talk_start_precise[2])
            else:
                # if there is no record of the start time, set start time to 20:00:00
                talk_start_time_offset = timedelta(hours=20)

            talk_date = datetime.strptime(talk["Datum"], '%Y-%m-%d')
            talk_date += talk_start_time_offset

            talk_speakers = find_speakers(talk["ID"])

            talk_title = talk["Title"]
            print(talk_title)
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

            if talk_date < datetime(2015, 7, 1):
                continue

            talk_folder = "../content/vhs/{}/{}".format(
                talk_date.year, friendly_name)
            Path(talk_folder).mkdir(parents=True, exist_ok=True)

            # Find corresponding image and download it
            talk_image_id = int(talk["BildID"])
            image_object = find_image(data, talk_image_id)
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
                else:
                    downloaded_image = True
            
            ### Write talk as markdown file with yaml front matter ###

            yaml_dict = {}
            yaml_dict["title"] = talk_title
            yaml_dict["date"] = talk_created.isoformat()
            yaml_dict["talk"] = {}
            yaml_dict["talk"]["date"] = talk_date.isoformat()
            
            if len(talk_speakers) > 0:
                yaml_dict["talk"]["speakers"] = []

                for speaker in talk_speakers:
                    yaml_dict["talk"]["speakers"].append(speaker)

            if downloaded_image:
                yaml_dict["talk"]["images"] = []
                yaml_dict["talk"]["images"].append(new_image_file_name.split("/")[-1])

            markdown_output = [  
                "---\n",
                yaml.dump(yaml_dict),
                "---\n",
                talk_content
            ]

            with open(talk_folder + "/" + "index.md", "w") as md:
                md.writelines(markdown_output)

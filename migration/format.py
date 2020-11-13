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
    
    for idx, entry in enumerate(file_database):
        if int(entry["ID"]) == id:
            return entry


if __name__ == "__main__":

    with open("db1033256-1.json", "r") as json_file:
        data = json.load(json_file)

        for id in range(40):
            talk = data[88]["data"][id]

            print("Talk content: \n{}".format(talk["Content"]))
            talk_content = html2text.html2text(talk["Content"], )

            talk_created = datetime.strptime(talk["Created"], '%Y-%m-%d %H:%M:%S')
            print("Created: {}".format(talk_created))

            talk_date = talk["Datum"]
            print("Date: {}".format(talk_date))

            # FIND REFERENTEN BASED ON VORTRAGID

            # talk_speaker = talk["Referent"]
            # print("Referent: {}".format(talk_speaker))

            talk_title = talk["Title"]
            print("Title: {}".format(talk_title))

            talk_start = talk["UhrzeitAnfang"]
            print("UhrzeitAnfang: {}".format(talk_start))

            talk_price = "{} (Ermäßigt: {})".format(
                talk["PreisAmount"], talk["PreisErmAmount"])
            print("Preis: {}".format(talk_price))

            talk_is_supplementary = talk["IsZusatz"]
            print("IsZusatz: {}".format(talk_is_supplementary))

            talk_is_sparse = talk["KeineDetails"]
            print("KeineDetails: {}".format(talk_is_sparse))

            # Find corresponding image and download it
            talk_image_id = int(talk["BildID"])
            image_object = find_image(data, talk_image_id)

            image_file_name = image_object["Name"]
            image_file_title = image_object["Title"]
            image_file_location = image_object["FileFilename"]

            print("### File: {}\nTitle: {}\n{}\n".format(
                image_file_name, image_file_title, image_file_location))

            download_url = "https://sternwarte-kreuznach.de/assets/" + image_file_location

            friendly_name = slugify(talk_title)

            talk_year = talk_date[:4]
            talk_folder = "../content/vhs/{}/{}".format(talk_year, friendly_name)
            Path(talk_folder).mkdir(parents=True, exist_ok=True)

            with open(talk_folder + "/" + "index.md", "w") as md:
                md.writelines(
                    [
                        "---\n",
                        'title: "{}"\n'.format(talk_title),
                        "talk_date: {}\n".format(talk_date),
                        "date: {}\n".format(talk_created.isoformat()),
                        "---\n",
                        talk_content
                    ]
                )

            print("Attemting to download from {}".format(download_url))
            r = requests.get(download_url, stream=True)

            new_image_file_name = talk_folder + "/" + friendly_name + "-title" + \
                "." + image_file_location.split(".")[-1].lower()

            if r.status_code == 200:
                # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                r.raw.decode_content = True

                # Open a local file with wb ( write binary ) permission.
                with open(new_image_file_name, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)

                print('Image sucessfully Downloaded: ', new_image_file_name)
            else:
                print('Image could not be retreived!')

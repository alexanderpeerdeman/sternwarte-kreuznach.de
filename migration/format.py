import json
import html2markdown
import requests
import shutil

if __name__ == "__main__":

    with open("db1033256-1.json", "r") as json_file:
        data = json.load(json_file)

        talk = data[88]["data"][13]

        talk_content = talk["Content"]
        print("Talk content: \n{}".format(html2markdown.convert(talk_content)))

        talk_created = talk["Created"]
        print("Created: {}".format(talk_created))

        talk_date = talk["Datum"]
        print("Date: {}".format(talk_date))

        talk_speaker = talk["Referent"]
        print("Referent: {}".format(talk_speaker))

        talk_title = talk["Title"]
        print("Title: {}".format(talk_title))

        talk_start = talk["UhrzeitAnfang"]
        print("UhrzeitAnfang: {}".format(talk_start))

        talk_price = "{} (Ermäßigt: {})".format(talk["PreisAmount"], talk["PreisErmAmount"])
        print("Preis: {}".format(talk_price))

        talk_is_supplementary = talk["IsZusatz"]
        print("IsZusatz: {}".format(talk_is_supplementary))

        talk_is_sparse = talk["KeineDetails"]
        print("KeineDetails: {}".format(talk_is_sparse))

        talk_image_id = int(talk["BildID"])

        file_database_id = 43

        image_object = data[file_database_id]["data"][talk_image_id]

        image_file_name = image_object["Name"]
        image_file_title = image_object["Title"]
        image_file_location = image_object["Filename"]

        print("### File: {}\nTitle: {}\n{}\n".format(image_file_name, image_file_title, image_file_location))

        download_url = "https://sternwarte-kreuznach.de/" + image_file_location

        print("Attemting to download from {}".format(download_url))
        r = requests.get(download_url, stream=True)
        print(r)

        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True

            # Open a local file with wb ( write binary ) permission.
            with open(image_file_name, 'wb') as f:
                shutil.copyfileobj(r.raw, f)

            print('Image sucessfully Downloaded: ', image_file_name)
        else:
            print('Image could not be retreived!')





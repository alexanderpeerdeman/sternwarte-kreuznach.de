import json
import html2markdown
import requests
import shutil

if __name__ == "__main__":

    with open("db1033256-1.json", "r") as json_file:
        data = json.load(json_file)


        ## List all tables
        # for idx, entry in enumerate(data[2:]):
        #     print(idx, entry["name"])

        ## List all field of vortrag
        for x in data[88]["data"]:
            print(x.keys())
            print(x["BildID"])
            break

            # Content
            # Created
            # Datum
            # Referent
            # Title
            # UhrzeitAnfang
            # BildID
            # Preis (+ Ermäßigt)
            # IsZusatz
            # Keine Details?



        file_database_id = 43
        image_id = 278

        image_object = data[file_database_id]["data"][image_id]

        print(data[43]["data"][278].keys())
        print(image_object)

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





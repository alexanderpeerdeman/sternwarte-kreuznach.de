import json
import html2markdown

if __name__ == "__main__":

    with open("SiteTree.json", "r") as json_file:
        data = json.load(json_file)
        posts = data[2]['data']

        print(posts[0])

        for post in posts:

            plain = html2markdown.convert(post["Content"])
            filename = post["URLSegment"] + ".md"
            print(filename)

            out = "---\n"
            out += "title: {}\n".format(post["Title"])
            out += "date: {}\n".format(post["Created"])
            out += "images: \n"
            out += "summary: TODO...\n"
            out += "---\n"
            out += plain

            print(out)

            with open("../content/blog/" + filename, "w") as target_file:
                target_file.write(out)
# convert jpg into progressive while resizing. "\>" is for downscaling only.
convert -strip -interlace plane -resize 2100\> -quality 85 namibia-large.jpg namibia.jpg



# Code um nur die zukünftigen Vorträge zu erhalten. Erfordert eine bestimmte Formatierung des Datums in der .md-file
# {{ range (where .Pages ".Params.talk_date" "ge" $currentTime) }}
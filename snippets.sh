# convert jpg into progressive while resizing. "\>" is for downscaling only.
convert -strip -interlace plane -resize 2100\> -quality 85 namibia-large.jpg namibia.jpg



# Code um nur die zukünftigen Vorträge zu erhalten. Erfordert eine bestimmte Formatierung des Datums in der .md-file
# {{ $currentTime := now.Format "2006-01-02T15:04:05" }}
# {{ range (.Paginate (where (.Pages.ByParam "talk_date") ".Params.talk_date" "ge" $currentTime) 12 ).Pages }}
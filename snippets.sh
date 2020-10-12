# convert jpg into progressive while resizing. "\>" is for downscaling only.
convert -strip -interlace plane -resize 2100\> -quality 85 namibia-large.jpg namibia.jpg
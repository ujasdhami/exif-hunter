from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
import sys
import shutil
import urllib.request

working_dir = os.getcwd()

immage = input("Enter image path (including image): ")

upath = 'tmp'
if not os.path.isdir(upath):
	os.makedirs(upath)

os.chdir(upath)
curr_dir = os.getcwd()

img_src = immage
img_dst = curr_dir
shutil.copy(img_src, img_dst)
   
def degrees_deci(degree, minutes, seconds, direction):
	deg_deci = degree + minutes / 60 + seconds / 3600
	if direction == "S" or direction == "W":
		deg_deci *= -1
	return deg_deci
    
def google_coordinates(coordinates):            
	lat_d = degrees_deci(float(coordinates["lat"][0]),
			float(coordinates["lat"][1]),
			float(coordinates["lat"][2]),
			coordinates["lat_ref"])
	lon_d = degrees_deci(float(coordinates["lon"][0]),
			float(coordinates["lon"][1]),
			float(coordinates["lon"][2]),
			coordinates["lon_ref"])
	return f"Locate on Google Maps: https://maps.google.com/?q={lat_d},{lon_d}"


media = os.listdir()

if len(media) == 0:
	print("\nAn error while processing the image.")
	exit()

for source in media:
	try:
		element = Image.open(source)
		print(f"\n\n\n\nFile: {source}\n\n\n\n")
		coordinates = {}
		if element._getexif() == None:
			print(f"{source} contains no EXIF data.")
		else:
			for tag, value in element._getexif().items():
				tname = TAGS.get(tag)
				if tname == "GPSInfo":
					for glock, values in value.items():
						print(f"{GPSTAGS.get(glock)} - {values}")
						if GPSTAGS.get(glock) == "GPSLatitude":
							coordinates["lat"] = values
						elif GPSTAGS.get(glock) == "GPSLongitude":
							coordinates["lon"] = values
						elif GPSTAGS.get(glock) == "GPSLatitudeRef":
							coordinates["lat_ref"] = values
						elif GPSTAGS.get(glock) == "GPSLongitudeRef":
							coordinates["lon_ref"] = values   
				else:
					print(f"{tname} - {value}")
			if coordinates:
				print(google_coordinates(coordinates))
	except IOError:
		print("Invalid file format. Skipping...")

os.chdir(working_dir)
url_scope = "tmp"
shutil.rmtree(url_scope)

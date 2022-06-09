from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
import sys
import csv
  
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
            
working_dir = os.getcwd()
os.chdir(os.path.join(working_dir, "scope"))
media = os.listdir()

if len(media) == 0:
	print("You don't have files in the 'scope' folder. Please add some.")
	exit()
with open("../extracted_csv.csv", "a", newline="") as csv_file:
	writer = csv.writer(csv_file)

	for source in media:
		try:
			element = Image.open(source)
			print(f"\n\n\n\nFile: {source}\n\n\n\n")
			print(f"\nAdding to CSV file...")
			coordinates = {}
			writer.writerow(("Filename", source))
			if element._getexif() == None:
				writer.writerow((source, "Contains no exif data."))
			else:
				for tag, value in element._getexif().items():
					tname = TAGS.get(tag)
					if tname == "GPSInfo":
						for glock, values in value.items():
							writer.writerow((GPSTAGS.get(glock), {values}))
							if GPSTAGS.get(glock) == "GPSLatitude":
								coordinates["lat"] = values
							elif GPSTAGS.get(glock) == "GPSLongitude":
								coordinates["lon"] = values
							elif GPSTAGS.get(glock) == "GPSLatitudeRef":
								coordinates["lat_ref"] = values
							elif GPSTAGS.get(glock) == "GPSLongitudeRef":
								coordinates["lon_ref"] = values   
					else:
						writer.writerow((tname, value))
				if coordinates:
					writer.writerow(("Google Maps URL",google_coordinates(coordinates)))
		except IOError:
			print("Invalid source format. Skipping...")

os.chdir(working_dir)

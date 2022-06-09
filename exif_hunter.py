from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import os
import sys

print("""
Exif Hunter v 1.0
by Ujas Dhami (https://github.com/ujasdhami)                                                
""")

while True:
	prompt = input("\n\nChoose an option:\n\n1. Extract EXIF in here\n2. Extract EXIF in a TXT file\n3. Export EXIF to CSV\n4. Remove EXIF data\n5. Extract EXIF from image URL\n6. Extract EXIF from a system file\n7. Quit\n\nYour choice: ")
	var = int(prompt)
	if var == 1:
		break
	elif var == 2:
		print(f"\nExtraction procedure complete.")
		sys.stdout = open("extracted.txt", "w")
		break
	elif var == 3:
		exec(open("csv_gen.py").read())
		print("\nExport complete.")
		sys.exit()
	elif var == 4:
		exec(open("exif_del.py").read())
		print ("\nEXIF data is removed from the scope.")
		sys.exit()
	elif var == 5:
		exec(open("exif_url.py").read())
		print ("\nExtraction Complete.")
		sys.exit()
	elif var == 6:
		exec(open("exif_sys.py").read())
		print ("\nExtraction Complete.")
		sys.exit()
	elif var == 7:
		print ("\nQuitting...")
		sys.exit()
	else:
		print("Invalid option selected.")
           
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

if prompt == "1":
	sys.stdout.close()
os.chdir(working_dir)
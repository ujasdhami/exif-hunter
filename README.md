# About

EXIF Hunter 1.0 is a tool for extracting EXIF data from images with various options to utilize.

## Features

EXIF Hunter provides:

* Data extraction from images
* Automatic cataloguing into a CSV format 
* Image EXIF extraction from URLs 

It has options of quick extraction without exporting to files, as well. 

## Prerequisites

This tool requires the latest versions of:

* Pillow
* Python-CSV

and these can be installed by using the command `pip install -r requirements.txt` after you clone the repository.

Other modules are installed by default with Python 3.

## Steps

1. Clone or download the repo's zip. 
2. `cd` to that folder and run `pip install -r requirements.txt`.
3. You can either extract multiple images' EXIF information or one, at a time. To use the multi-image mode, paste all your images into the `scope` folder before running the main file.
4. Run `exif_hunter.py`.

and that's it.

If you face any kind of permission issues, it can be solved by using `chmod +x *`.

## Support

This tool supports JPG, JPEG and TIFF file formats.
import os
from PIL import Image
presentdir = os.getcwd()
os.chdir(os.path.join(presentdir, "scope"))
elements = os.listdir()
if len(elements) == 0:
    print("Images not found in 'scope'. Please add some images first.")
    exit()
for file in elements:
    try:
        element = Image.open(file)
        element_data = list(element.getdata())
        delexif = Image.new(element.mode, element.size)
        delexif.putdata(element_data)
        delexif.save(file)
    except IOError:
        print("Image format not supported. Supported format is JPG.")

import requests
import re
from cairosvg import svg2png
from PIL import Image
from PIL import ImageEnhance
import shutil

DEVICE_X_RESOLUTION=1860
DEVICE_Y_RESOLUTION=2480

URL = "https://www.yr.no/en/content/2-3081368/meteogram.svg"

response = requests.get(URL)

open("meteogram.svg", "wb").write(response.content)

old_meteogram="meteogram.svg"
textfile = open(old_meteogram, 'r')
filetext = textfile.read()
textfile.close()

content_new = re.sub(".location-header.*?}","" ,filetext, flags=re.DOTALL)
content_new = re.sub(".served-by-header.*?}","" ,content_new, flags=re.DOTALL)
content_new = re.sub(".day-label.*?}","" ,content_new, flags=re.DOTALL)
content_new = re.sub(".hour-label.*?}","" ,content_new, flags=re.DOTALL)
content_new = re.sub(".y-axis-label.*?}","" ,content_new, flags=re.DOTALL)
content_new = re.sub(".legend-label.*?}","" ,content_new, flags=re.DOTALL)
content_new = re.sub(".precipitation-values-over-max.*?}","" ,content_new, flags=re.DOTALL)
content_new = re.sub("Temperature °C","" ,content_new, flags=re.DOTALL)
content_new = re.sub("Wind m/s","" ,content_new, flags=re.DOTALL)
content_new = re.sub("Precipitation mm","" ,content_new, flags=re.DOTALL)
content_new = re.sub("<svg x=\"0\" y=\"4\" width=\"10\" height=\"10\">.*?</svg>","" ,content_new, flags=re.DOTALL)

new_meteogram="new.svg"
f = open(new_meteogram, "w")
f.write(content_new)
f.close()

svg2png(url="new.svg", write_to="meteogram.png")

background = Image.new("RGB", (DEVICE_X_RESOLUTION, DEVICE_Y_RESOLUTION), color="white")
meteogram = Image.open("meteogram.png")#.convert("L")
enhancer = ImageEnhance.Sharpness(meteogram)
#meteogram = enhancer.enhance(4)

meteogram = meteogram.resize((DEVICE_X_RESOLUTION, DEVICE_X_RESOLUTION//2)) # 1860x930
background.paste(meteogram, (0, DEVICE_Y_RESOLUTION+80-DEVICE_X_RESOLUTION//2))

background.save("meteogram.png")

shutil.copyfile("meteogram.png","/some/dir/meteogram.png")
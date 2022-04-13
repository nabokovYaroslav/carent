import os
from PIL import Image


def convert_to_webp(source):
  base_path = os.path.splitext(source)[0]
  file_path = base_path + '.webp'
  # check for exists webp version of image
  if(os.path.isfile(file_path)):
    return
  image = Image.open(source)
  image.save(file_path, format="webp", quality=75)

def is_webp(http_accept):
  formats = http_accept.split(',')
  if 'image/webp' in formats:
    webp = True
  else:
    webp = False
  return webp

import filecmp
import os
from io import BytesIO

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image

from utils.webp import convert_to_webp


ADAPTIVE_RESOLUTIONS = [
	(540, 540),
	(720, 720),
	(960, 960),
	(1140, 1140),
]

TUMBNAIL_SIZE = 60, 60

MAX_SIZE = max(ADAPTIVE_RESOLUTIONS)

EXTENSIONS = [
	('.webp', convert_to_webp)
]

def change_resolution(image):
	if image:
		im_io = BytesIO()
		im = Image.open(image.file)
		im.thumbnail(MAX_SIZE, Image.ANTIALIAS)
		im.save(im_io, im.format, optimize=True)
		im_file = InMemoryUploadedFile(im_io, None, image.file.name, None, None, None)
		im_io = BytesIO()
		return im_file
	return None

def create_adaptive_resolution_image(image_path, formatting):
	if(os.path.isfile(image_path)):
		path, ext = os.path.splitext(image_path)
		for resolution in ADAPTIVE_RESOLUTIONS:
			file_path = "{}-{}x{}{}".format(path, resolution[0], resolution[1], ext)
			with Image.open(image_path) as im:
				im.thumbnail(resolution, Image.ANTIALIAS)
				im.save(file_path)
			if formatting:
				create_adaptive_format_image(file_path)

def create_adaptive_format_image(image_path):
	if(os.path.isfile(image_path)):
		for extension in EXTENSIONS:
			handler = extension[1]
			handler(image_path)

def crop_center(pil_img, crop_width, crop_height):
	img_width, img_height = pil_img.size
	return pil_img.crop(((img_width - crop_width) // 2,
						 (img_height - crop_height) // 2,
						 (img_width + crop_width) // 2,
						 (img_height + crop_height) // 2))
		
def create_tumbnail_image(image_path, formatting=None):
	if(os.path.isfile(image_path)):
		path, ext = os.path.splitext(image_path)
		file_path = "{}-{}x{}{}".format(path, TUMBNAIL_SIZE[0], TUMBNAIL_SIZE[1], ext)
		with Image.open(image_path) as im:
			im = crop_center(im, min(im.size), min(im.size))
			im.thumbnail(TUMBNAIL_SIZE, Image.ANTIALIAS)
			im.save(file_path)
		if formatting:
			create_adaptive_format_image(file_path)

def delete_images(image_path):
	base_path, ext = os.path.splitext(image_path)
	extensions = [v[0] for v in EXTENSIONS] + [ext]
	resolutions = ADAPTIVE_RESOLUTIONS + [TUMBNAIL_SIZE]
	# delete original image
	for extension in extensions:
		file_path = "{}{}".format(base_path, extension)
		if(os.path.isfile(file_path)):
			os.remove(file_path)
	
	# delete all additional images
	for resolution in resolutions:
		for extension in extensions:
			file_path = "{}-{}x{}{}".format(base_path, resolution[0], resolution[1], extension)
			if(os.path.isfile(file_path)):
				os.remove(file_path)

def compare_images(existing_image_path : str, image_in_memory: InMemoryUploadedFile):
	path = default_storage.save(image_in_memory.name, ContentFile(image_in_memory.read()))
	tmp_file = os.path.join(settings.MEDIA_ROOT, path)
	equal = False
	if filecmp.cmp(existing_image_path, tmp_file):
		equal = True
	os.remove(tmp_file)
	return equal
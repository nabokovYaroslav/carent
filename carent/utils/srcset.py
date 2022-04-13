import os

from utils.image import ADAPTIVE_RESOLUTIONS, TUMBNAIL_SIZE

def get_srcset(url, extension_image):
    path, ext = os.path.splitext(url)
    ext = ext.replace('.', '')
    srcset = ""
    if extension_image != None:
        ext = extension_image
    for resolution in ADAPTIVE_RESOLUTIONS:
        srcset += "{}-{}x{}.{} {}w,".format(path, resolution[0], resolution[1], ext, resolution[0])
    return srcset

def get_adaptive_image(url, extension_image):
    path, ext = os.path.splitext(url)
    ext = ext.replace('.', '')
    if extension_image != None:
        ext = extension_image
    return "{}.{}".format(path, ext)

def get_tumbnail(url, extension_image):
    path, ext = os.path.splitext(url)
    ext = ext.replace('.', '')
    if extension_image != None:
        ext = extension_image
    return "{}-{}x{}.{}".format(path, TUMBNAIL_SIZE[0], TUMBNAIL_SIZE[1], ext)
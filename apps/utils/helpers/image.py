from io import BytesIO

from PIL import Image, ImageOps
from PIL import Image as pil, ExifTags
from PIL import UnidentifiedImageError

from .file import rename_file


def get_pil_supported_format_or_default(image, format=None):
    """
    Returns the supported format of the given image or the default format if the given format is not supported.
    """
    DEFAULT_FORMATS = [
        'JPEG',
        'PNG',
        'WEBP',
    ]

    if format:
        format = format.upper()
        if format in DEFAULT_FORMATS:
            return format

        for pil_ext, pil_format in pil.EXTENSION.items():
            if pil_format == format:
                return format

    return image.format.upper()


def pil_extension_to_format_or_none(ext):
    """
    Returns the format of the given extension or None if the extension is not supported.
    """
    return pil.EXTENSION.get(ext.lower(), None)


def pil_format_to_extension_or_none(format):
    """
    Returns the extension of the given format or None if the format is not supported.
    """
    DEFAULT_EXTENSIONS = {
        'JPEG': '.jpg',
        'PNG': '.png',
        'WEBP': '.webp',
    }

    format = format.upper()
    if format in DEFAULT_EXTENSIONS:
        return DEFAULT_EXTENSIONS[format]

    for pil_ext, pil_format in pil.EXTENSION.items():
        if pil_format == format:
            return pil_ext

    return None


def resize_image(image, size, thumb=True):
    """
    Resizes the given image to the given size.
    """
    if thumb:
        image.thumbnail(size, pil.ANTIALIAS)
        return image

    return image.resize(size, pil.ANTIALIAS)


def normalize_rotation(image):
    """
    Normalizes the rotation of the given image.
    """
    try:
        image._getexif()
    except AttributeError:
        return image

    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == 'Orientation':
            break
    else:
        return image

    format = image.format
    exif = image._getexif()
    if exif is None:
        return image

    action_nr = exif.get(orientation, None)

    if action_nr is None:
        return image
    if action_nr in (3, 4):
        image = image.rotate(180, expand=True)
    elif action_nr in (5, 6):
        image = image.rotate(270, expand=True)
    elif action_nr in (7, 8):
        image = image.rotate(90, expand=True)
    if action_nr in (2, 4, 5, 7):
        image = ImageOps.mirror(image)

    image.format = format

    return image


def get_centring_from_crop(crop):
    """
    Returns the centring for the given crop.
    """
    vertical = {
        'top': 0,
        'middle': 0.5,
        'bottom': 1,
    }
    horizontal = {
        'left': 0,
        'center': 0.5,
        'right': 1,
    }
    return [
        vertical[crop[0]],
        horizontal[crop[1]],
    ]


def get_processed_image(image_file, image_name, **kwargs):
    """
    Returns the processed image using the Pillow library.

    Adapted from `django-resized`
    https://github.com/un1t/django-resized
    version 1.0.1

    Args:
        image_file (file object): The file object containing the image data to be processed.
        image_name (str): The name of the image file.
        **kwargs: Additional keyword arguments to customize the image processing.

    Returns:
        tuple: A tuple containing a bytes object representing the processed image data and the filename of the image.

    Keyword Args:
        size (tuple): A tuple of the width and height of the output image.
        scale (float): A scaling factor for the output image.
        crop (str): A string representing the cropping mode for the output image.
        quality (int): An integer representing the quality of the output image.
        keep_meta (bool): A boolean value indicating whether to keep the metadata of the input image.
        force_format (str): A string representing the image format to be used for the output image.
        prefix (str): A string representing the prefix to be used for the filename of the output image.
    """

    size = kwargs.get('size', None)
    scale = kwargs.get('scale', None)
    crop = kwargs.get('crop', None)
    quality = kwargs.pop('quality', -1)
    keep_meta = kwargs.get('keep_meta', True)
    force_format = kwargs.get('force_format', None)
    prefix = kwargs.get('prefix', None)

    try:
        img = Image.open(image_file)
    except UnidentifiedImageError:
        return None, ''

    img = normalize_rotation(img)

    rgb_formats = ('jpeg', 'jpg')
    rgba_formats = ('png')

    if force_format and force_format.lower() in rgb_formats and img.mode != 'RGB':
        img = img.convert('RGB')
    if force_format and force_format.lower() in rgba_formats and img.mode != 'RGBA':
        img = img.convert('RGBA')

    resample = Image.ANTIALIAS

    if size is None:
        size = img.size

    if crop:
        thumb = ImageOps.fit(
            img,
            size,
            resample,
            centering=get_centring_from_crop(crop)
        )

    elif None in size:
        thumb = img
        if size[0] is None and size[1] is not None:
            scale = size[1] / img.size[1]
        elif size[1] is None and size[0] is not None:
            scale = size[0] / img.size[0]

    else:
        img.thumbnail(
            size,
            resample,
        )
        thumb = img

    if scale is not None:
        thumb = ImageOps.scale(
            thumb,
            scale,
            resample
        )

    img_info = img.info
    if not keep_meta:
        img_info.pop('exif', None)

    bytes_io = BytesIO()
    img_format = get_pil_supported_format_or_default(img, force_format)

    if img_format == "WEBP" and quality == -1:
        quality = 100

    thumb.save(bytes_io, format=img_format, quality=quality, **img_info)

    ext = pil_format_to_extension_or_none(img_format)
    filename = rename_file(image_name, prefix, ext)

    return bytes_io, filename

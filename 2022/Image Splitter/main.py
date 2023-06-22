import pyinputplus as pyip
from PIL import Image
from pathlib import Path
from shutil import rmtree as remove_folder


def get_path(p):
    p = Path(p)
    if not p.exists():
        raise Exception('Path must exist.')
    if not p.is_file():
        raise Exception('Path must include the file in it (ie. C:\\my_photo.jpg).')
    if not p.suffix in ['.png', '.jpg']:
        raise Exception('Image must be PNG or JPG.')
    return p


def main():
    path = pyip.inputCustom(get_path, 'Enter image path: ', )
    new_folder = path.parent / Path(path.stem + ' - SPLITTED')
    if new_folder.exists():
        remove_folder(new_folder)
    new_folder.mkdir()
    image = Image.open(path)
    width = pyip.inputInt('Enter the WIDTH you want each sub-image would have (in pixels): ', min=1, max=image.size[0])
    height = pyip.inputInt('Enter the HEIGHT you want each sub-image would have (in pixels): ', min=1, max=image.size[1])

    idx = 0
    for x in range(0, image.size[0], width):
        for y in range(0, image.size[1], height):
            sub_image = image.crop([x, y, x + width, y + height])
            sub_image.save(Path(new_folder, str(idx) + path.suffix))
            idx += 1


if __name__ == '__main__':
    main()
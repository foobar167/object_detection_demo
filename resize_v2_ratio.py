# Resize images with aspect ratio.
# Save directory tree structure.
# Save image format or change image format if necessary.
# Example:
# python resize_v2_ratio.py --input ./data/raw --output ./data/images --size "(800, 600)"
import os
import argparse

from PIL import Image

FILTER = Image.ANTIALIAS  # could be: NEAREST, BILINEAR, BICUBIC and ANTIALIAS


def resize(image, imsize):
    """ Resize image proportionally """
    w1, h1 = image.size
    if w1 <= imsize[0] and h1 <= imsize[1]:
        return image  # return unchanged image if its size is small enough
    w1, h1 = float(w1), float(h1)
    w2, h2 = float(imsize[0]), float(imsize[1])
    aspect_ratio1 = w1 / h1
    aspect_ratio2 = w2 / h2
    if aspect_ratio1 == aspect_ratio2:
        return image.resize((int(w2), int(h2)), FILTER)
    elif aspect_ratio1 > aspect_ratio2:
        return image.resize((int(w2), int(w2 / aspect_ratio1)), FILTER)
    else:  # aspect_ratio1 < aspect_ratio2
        return image.resize((int(h2 * aspect_ratio1), int(h2)), FILTER)


if __name__ == '__main__':
    # Set command-line arguments
    parser = argparse.ArgumentParser(
        description='Resize images to uniformed target size.',
    )
    parser.add_argument(
        '--input',
        help='Directory path to images.',
        default='./data/raw',
        type=str,
    )
    parser.add_argument(
        '--output',
        help='Directory path to save resized images.',
        default='./data/images',
        type=str,
    )
    parser.add_argument(
        '--size',
        help='Target size to resize as a tuple of 2 integers.',
        default='(800, 600)',
        type=str,
    )
    parser.add_argument(
        '--force_ext',
        help='Change image extension.',
        default='',  # do not change image extension by default, save it
        type=str,
    )
    parser.add_argument(
        '--rename',
        help='Save image name or rename it to directory name.',
        default='',  # save image name by default, do not rename it
        type=str,
    )
    args = parser.parse_args()

    # Get arguments from command-line
    input_dir = args.input
    output_dir = args.output
    size = eval(args.size)
    msg = '--size argument must be a tuple of 2 integers'
    assert isinstance(size, tuple) and len(size) == 2, msg
    ext = args.force_ext
    rename = args.rename

    # Recursively resize files in directories
    input_dir_len = len(input_dir) + 1  # +1 is to remove trailing slash or backslash
    basename = os.path.basename(input_dir)
    for path, dirs, files in os.walk(input_dir):
        # Get sub-directory name and create it in output_dir
        sub_dir = os.path.join(output_dir, path[input_dir_len:])
        os.makedirs(sub_dir, exist_ok=True)

        # Get number of files in the path and set zero padding number
        n = len(files)  # number of images to resize
        zero_padding = len(str(n))  # zero padding number
        i = 1  # files counter

        for file in files:
            try:  # try to open file as an image
                img = Image.open(os.path.join(path, file))
                img = img.convert('RGB')  # discard alpha channel
            except OSError as err:  # file is NOT an image
                pass  # do nothing
            else:  # file is an image
                # Create new file name
                file_name, file_ext = os.path.splitext(file)
                if ext == '':  # save original extension
                    file_ext = img.format.lower()
                else:  # change original extension
                    file_ext = ext.lower()
                if rename != '':  # rename file name
                    dir_name = os.path.basename(path)
                    if dir_name == basename:
                        dir_name = os.path.basename(output_dir)
                    file_name = dir_name + '_' + str(i).zfill(zero_padding)
                    i += 1
                new_name = file_name + '.' + file_ext
                # Resize and save image to output_dir
                # print(new_name)  # for debug purposes
                print('.', end='', flush=True)
                img = resize(img, size)
                img.save(os.path.join(sub_dir, new_name))

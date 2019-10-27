# Resize images using fixed width and height, without aspect ratio.
# Resize images with fixed file format. For example, JPG images only.
# Example:
# python resize_v1_fixed.py --input ./data/raw --output ./data/images --ext jpg --size "(800, 600)"
import os
import cv2
import glob
import argparse

if __name__ == '__main__':
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
        '--ext',
        help='Raw image files extension to resize.',
        default='jpg',
        type=str,
    )
    parser.add_argument(
        '--size',
        help='Target size to resize as a tuple of 2 integers.',
        default='(800, 600)',
        type=str,
    )
    args = parser.parse_args()

    input_dir = args.input
    output_dir = args.output
    ext = args.ext
    size = eval(args.size)
    msg = '--target-size must be a tuple of 2 integers'
    assert isinstance(size, tuple) and len(size) == 2, msg
    names = glob.glob(os.path.join(input_dir, f'*.{ext}'))
    os.makedirs(output_dir, exist_ok=True)
    n = len(names)  # number of images to resize
    zero_padding = len(str(n))  # zero padding number
    print(f'{n} files to resize from directory '
          f'`{input_dir}` to target size: {size}')

    for i, name in enumerate(names, 1):
        print('.', end='', flush=True)
        img = cv2.imread(name)
        resized = cv2.resize(img, size)
        new_name = str(i).zfill(zero_padding) + f'.{ext}'
        new_name = os.path.join(output_dir, new_name)
        cv2.imwrite(new_name, resized)

    print(f'\n\nDone resizing {n} files.\n'
          f'Saved to directory: `{output_dir}`')

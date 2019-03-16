"""

Prepare Peltarion platform data for image classification.
 
Resize all jpg/png images to the same size, create index.csv file and create
a zip bundle compatible for import into the Peltarion platform.

Assumes input images are stored under
input_path/class_1/*.[jpg|png]
input_path/class_2/*.[jpg|png]
...
where class_1, class_2, etc are the names of the different classes

Images of other modes than 'RGB' or 'RGBA' will be ignored.

For help, run:
    > python resize_and_bundle_images.py -- --help
"""

import os
from glob import glob
import argparse

from PIL import Image
import pandas as pd
import zipfile36 as zipfile

parser = argparse.ArgumentParser()
parser.add_argument('--input_path', default='./data',
                    help="Directory containing sub-directories with images")
parser.add_argument('--output_path', default='./data/resized',
                    help="Directory to write output to, should not exist")
parser.add_argument('--zip_filename', default='data.zip',
                    help="Filename of the output zip bundle file")
parser.add_argument('--new_width', default=300,
                    help="Width to resize all images to")
parser.add_argument('--new_height', default=200,
                    help="Height to resize all images to")
parser.add_argument('--crop_square', default=False,
                    help="Crop to square", action='store_true')

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))


def crop(im):
    width, height = im.size
    if width > height:
        y1 = 0
        y2 = height
        x1 = round((width - height) / 2)
        x2 = width - round((width - height) / 2)
    else:
        y1 = round((height - width) / 2)
        y2 = height - round((height - width) / 2)
        x1 = 0
        x2 = width
    crop_im = im.crop((x1,y1,x2,y2))
    return crop_im


def main():
    args = parser.parse_args()

    if os.path.exists(args.output_path):
        raise ValueError('Output path already exists', args.output_path)
    os.makedirs(args.output_path)

    # Include images of type jpg and png
    images_full_path = glob(os.path.join(args.input_path, '*', '*.jpg')) \
                     + glob(os.path.join(args.input_path, '*', '*.png'))

    print("Num images found: ", len(images_full_path))

    images = []
    classes = []
    for i in images_full_path:
        print(i)
        img_type = i.split('/')[-1].split('.')[-1] # 'jpg' or 'png'
        i_rel_path = os.path.join(*i.split('/')[-2:]) # path including 'class/file'
        class_name = i_rel_path.split('/')[0]

        # Create class directory
        if not os.path.exists(os.path.join(args.output_path, class_name)):
            os.makedirs(os.path.join(args.output_path, class_name))

        # Open image, resize and save in new path
        im = Image.open(i)
        if im.mode not in ['RGB', 'RGBA']:
            continue
        im = im.convert('RGB')
        if args.crop_square == True:
            im = crop(im)
        new_img = im.resize((int(args.new_width), int(args.new_height)))
        new_img_rel_path = i_rel_path.split('.')[0] + "_resized." + img_type
        new_img_path = os.path.join(args.output_path, new_img_rel_path)
        new_img.save(new_img_path, quality=95)

        # Save img relative path and class for index.csv file
        images.append(new_img_rel_path)
        classes.append(class_name)

    # Save index.csv file, one row per image
    dataset_index = pd.DataFrame({'image': images, 'class': classes})
    dataset_index.to_csv(os.path.join(args.output_path,'index.csv'), index=False)

    # Create zip file with index.csv and resized images
    zipf = zipfile.ZipFile(os.path.join(args.output_path, args.zip_filename),
                           'w',
                           zipfile.ZIP_DEFLATED)
    zipdir(args.output_path, zipf)
    zipf.close()


if __name__ == '__main__':
    main()

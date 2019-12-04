import functools
import os
import random
import sys
from argparse import ArgumentParser

import PIL
import librosa as lr
import numpy as np
import pandas as pd
import sidekick


class Pipeline:
    def __init__(self, argv=None):
        self.args = self.parse_args(argv=argv)
        self.data_dir = self.args.data_dir
        self.output_dir = self.args.output_dir
        self.data_name = self.args.data_name
        self.nbr_of_random_crops = self.args.nbr_of_random_crops
        self.zip_dir = self.args.zip_dir

        self.sample_rate = 44100
        self.fft_length = 1024
        self.desired_size = 128

    def waw_to_image(self, waw_file):
        # Load waw file
        audio, sample_rate = lr.load(waw_file, sr=self.sample_rate)
        # Compute short fourier transform
        # Complex value STFT
        stft = lr.stft(
            audio,
            hop_length=512,
            n_fft=self.fft_length,
            center=False
        )
        # Real value spectrogram
        spectrogram = np.abs(stft) ** 2.0
        # Spectrogram to db
        mel_basis = lr.filters.mel(self.sample_rate, n_fft=1024, n_mels=128,
                                   fmax=sample_rate / 2, fmin=20)
        mel_spectrogram = np.dot(mel_basis, spectrogram)
        db_mel_spectrogram = lr.power_to_db(mel_spectrogram, ref=np.max)
        # Rescale to image
        rescaled_db_mel_spectrogram = (db_mel_spectrogram + 80) / 80 * 255
        # Convert to image format
        image = PIL.Image.fromarray(rescaled_db_mel_spectrogram.astype(np.uint8))
        image = image.convert('L')
        # Random crop image
        if image.size[0] < self.desired_size or image.size[1] < self.desired_size:
            new_im = PIL.Image.new("L", (self.desired_size, self.desired_size))
            # Paste in the middle
            new_im.paste(image, ((self.desired_size - image.size[0]) // 2,
                                 (self.desired_size - image.size[1]) // 2))
        else:
            new_im = image
        crop_w = round(random.uniform(0, image.size[0] - self.desired_size))
        crop_h = round(random.uniform(0, image.size[1] - self.desired_size))
        new_im = new_im.crop(
            (crop_w, crop_h, self.desired_size + crop_w, self.desired_size + crop_h))
        return new_im

    def create_data_set(self):
        df_all = pd.read_csv("train_curated.csv")
        df_all['fname'] = self.data_dir + df_all['fname']
        labels = df_all['labels'].str.get_dummies(',').sort_index(axis=1)
        df_all = pd.concat((df_all, labels), axis=1)
        df_train = df_all.iloc[12:]
        df_test = df_all.iloc[:12]
        df_list = [(df_train, 'train'), (df_test, 'test')]

        for df, set in df_list:
            if set == 'train':
                data = list()
                for row in df.to_dict('records'):
                    for j in range(self.nbr_of_random_crops):
                        try:
                            img = self.waw_to_image(row['fname'])
                            row['image'] = img
                            data.append(row)
                        except FileNotFoundError:
                            print("An exception occurred")

                df_new = pd.DataFrame(data)
                class_labels = list(labels.keys())
                df_new = df_new.astype({class_labels[i] : np.int64 for i in range(len(class_labels))})

                # Create dataset
                set_image_format = functools.partial(
                    sidekick.process_image, file_format='png')
                sidekick.create_dataset(
                    os.path.join(self.zip_dir, self.data_name + 'dataset.zip'),
                    df_new,
                    preprocess={'image': set_image_format},
                    progress=True
                )

    @staticmethod
    def parse_args(argv=None):
        argv = argv if argv is not None else sys.argv[1:]
        parser = ArgumentParser(description=__doc__)
        parser.add_argument('--data-dir', help='Base directory of data',
                            default='train_curated/')
        parser.add_argument('--output-dir', help='Where to stroe the zip file',
                            default='freesound_peltarion/')
        parser.add_argument('--data-name', help='Name that explain data',
                            default='base')
        parser.add_argument('--zip_dir', help='Name that explain data',
                            default='peltarion_data')
        parser.add_argument('--nbr_of_random_crops',
                            help='Number of times to randomly crop the images',
                            type=int, default=1)
        return parser.parse_args(argv)

if __name__ == '__main__':
    Pipeline().create_data_set()
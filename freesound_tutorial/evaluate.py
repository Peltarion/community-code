import sidekick
import numpy as np
import PIL
import pandas as pd


def evaluate():

    df = pd.read_pickle('dataframe.pkl')
    data_frame_input = [{'fname': PIL.Image.open(df.iloc[i]['fname'])}
                        for i in range(10)]

    client = sidekick.Deployment(
        url='https://a.peltarion.com/deployment/ac7c3d9c-e45e-40b7-8249-dcc0dc3e6130/forward',
        token='7d269cb2-110f-4045-b6d7-4cd643d8b150')

    # MAYBE BETTER WITH LAZY PREDICTION....
    predictions = client.predict_many(data_frame_input)

    for i, pred in enumerate(predictions):
        result = {}
        max_pred = [0, '']
        print(' ')
        print('Sampel file: ' + str(df.iloc[i]['fname']))
        print('True label: ' + str(df.iloc[i]['labels']))
        for key in pred.keys():
            if pred[key] > max_pred[0]:
                max_pred[0] = pred[key]
                max_pred[1] = key
            if pred[key] > 0.5:
                result[key] = pred[key]
        print('Results: ')
        print(result)
        print('Max predictions: ')
        print(max_pred)

if __name__ == '__main__':
    evaluate()


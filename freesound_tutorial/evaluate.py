import PIL
import pandas as pd
import sidekick


def evaluate():

    df = pd.read_pickle('dataframe.pkl')
    data_frame_input = [{'fname': PIL.Image.open(df.iloc[i]['fname'])}
                        for i in range(10)]

    client = sidekick.Deployment(
        url='<url>',
        token='<token>'
    )

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

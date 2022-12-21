import torch
import pandas as pd
from PIL import Image


def predict(image, model_path='yolov5/runs/train/exp/weights/best.pt'):
    model = torch.hub.load('yolov5', 'custom', model_path, source='local')
    model.names = ['хлеб', 'бутерброд', 'сыр', 'кофе', 'омлет', 'каша', 'чай']

    results = model(image)
    data = pd.DataFrame(results.pandas().xyxy[0])
    df = data.copy()
    df.loc[df['name'] == 'porridge', 'name'] = 'каша'
    df.loc[df['name'] == 'coffee', 'name'] = 'кофе'
    df.loc[df['name'] == 'cheese', 'name'] = 'сыр'
    df.loc[df['name'] == 'bread', 'name'] = 'хлеб'
    df.loc[df['name'] == 'tea', 'name'] = 'чай'
    df.loc[df['name'] == 'cheese_sandwich', 'name'] = 'бутерброд'
    df.loc[df['name'] == 'Omlet', 'name'] = 'омлет'
    BJG = pd.read_csv('NeuroUtils/bjg.csv', sep=';')
    BJG.loc[BJG['name'] == 'Porridge', 'name'] = 'каша'
    BJG.loc[BJG['name'] == 'Coffe', 'name'] = 'кофе'
    BJG.loc[BJG['name'] == 'Cheese', 'name'] = 'сыр'
    BJG.loc[BJG['name'] == 'Bread', 'name'] = 'хлеб'
    BJG.loc[BJG['name'] == 'Tea', 'name'] = 'чай'
    BJG.loc[BJG['name'] == 'Casserole', 'name'] = 'бутерброд'
    BJG.loc[BJG['name'] == 'Omlet', 'name'] = 'омлет'
    BJG = BJG.rename(columns={'name': 'имя', 'squirrels': 'белки', 'fats': 'жиры', 'carbohydrates': 'углеводы',
                              'calories': 'калории'})
    df.drop(columns={'xmin', 'ymin', 'xmax', 'ymax', 'confidence', 'class'}, axis=1, inplace=True)
    df=df.rename(columns={'name':'имя'})
    df = df.drop_duplicates()
    df['качество'] = 'хорошее'
    for index, row in df.iterrows():
        for index2, row2 in BJG.iterrows():
            if row['имя'] == row2['имя']:
                df.at[index, 'белки'] = row2['белки']
                df.at[index, 'жиры'] = row2['жиры']
                df.at[index, 'углеводы'] = row2['углеводы']
                df.at[index, 'калории'] = row2['калории']
                break

    img = results.render()
    img = Image.fromarray(img[0])
    return (df, img)

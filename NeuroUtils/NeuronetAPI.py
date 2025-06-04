import torch
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

def predict(image, model_path='yolov5/runs/train/exp/weights/best.pt'):
    model = torch.hub.load('yolov5', 'custom', model_path, source='local')
    my_custom_names = ['хлеб', 'каша', 'запеканка', 'кофе', 'бутерброд', 'сыр', 'фрукты', 'омлет', 'паста', 'масло', 'чай']
    model.names = my_custom_names
    results = model(image)
    data = pd.DataFrame(results.pandas().xyxy[0])
    df = data.copy()
    df =df.rename(columns={0:'xmin', 1:'ymin', 2:'xmax', 3:'ymax', 4:'confidence', 5:'class_id'})
    df['name'] = df['class_id'].map(lambda x: my_custom_names[int(x)] if x < len(my_custom_names) else 'неизвестный')
    # df.loc[df['name'] == 'porridge', 'name'] = 'каша'
    # df.loc[df['name'] == 'coffee', 'name'] = 'кофе'
    # df.loc[df['name'] == 'cheese', 'name'] = 'сыр'
    # df.loc[df['name'] == 'bread', 'name'] = 'хлеб'
    # df.loc[df['name'] == 'tea', 'name'] = 'чай'
    # df.loc[df['name'] == 'cheese_sandwich', 'name'] = 'бутерброд'
    # df.loc[df['name'] == 'Omlet', 'name'] = 'омлет'
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
    df.drop(columns={'xmin', 'ymin', 'xmax', 'ymax', 'confidence', 'class_id'}, axis=1, inplace=True)
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


if __name__== "__main__":
    dir = '100.jpg' # Colored
    # dir = 'ReadyMaterial/Food/Mix/12.jpg'   # Black and white
    # dir = 'yolov5/1.jpg'
    (data, image) = predict(dir, 'yolov5/runs/train/yolov5s_results2/weights/best.pt')
    data

    plt.imshow(image)
    image

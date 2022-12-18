import torch
import pandas as pd

def predict(image, model_path):
    model = torch.hub.load('yolov5', 'custom', model_path, source='local')

    results = model(image)
    data = pd.DataFrame(results.pandas().xyxy[0])
    img = results.render()
    return (data, img)
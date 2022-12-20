import datetime

from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State
from NeuroUtils import NeuronetAPI
import numpy as np
from PIL import Image
import base64
from io import BytesIO as _BytesIO
import dash_io as dio


def b64_to_pil(string):
    decoded = base64.b64decode(string)
    buffer = _BytesIO(decoded)
    im = Image.open(buffer)

    return im

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Upload(
        id='upload-image',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=False
    ),
    html.Div(id='output-image-upload'),
])


@app.callback(Output('output-image-upload', 'children'),
              Input('upload-image', 'contents'))
def update_output(content):
    if content is not None:
        encoded = dio.url_to_pillow(content)
        (data,image) = NeuronetAPI.predict(encoded)
        children = [
                html.Img(src=content),
                html.Img(src=image),
            ]
        return children

if __name__ == '__main__':
    app.run_server(debug=True)

from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from NeuroUtils import NeuronetAPI
from PIL import Image
import base64
from io import BytesIO as _BytesIO
import dash_io as dio
import webbrowser
from threading import Timer
import os


def b64_to_pil(string):
    decoded = base64.b64decode(string)
    buffer = _BytesIO(decoded)
    im = Image.open(buffer)

    return im

external_stylesheets = ['assets/style.css']
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.title = 'NeuroNet'

app.layout = html.Div(className='root', children=[
    #html.Div(children=html.Img(src='assets/'), className='icodiv'),
    html.H1('NeuroNet', className='hb'),
    html.Div(className='content',
             children=[
                 html.Div(className='left', id='left',
                     children=[
                        dcc.Upload(
                                id='upload-image',
                                children=html.Div([
                                    'Перетащите файл сюда или ',
                                    html.A('нажмите'), ', чтобы загрузить '
                                ]),
                                className='empty',
                                # Allow multiple files to be uploaded
                                multiple=False,
                                accept='image/*'
                            ),
                     ]
                 ),
                html.Div(className='right',
                         id='right',
                         children=[
                            html.Div(className='empty', children=html.Label('Результат', className='labelc')),
                         ]
                ),
                html.Div(id='table',
                         children=html.Div(className='empty-table', children=html.Label('БЖУ таблица', className='labelc'))
                         ),
             ]),
            html.Div('Разработчики: Игорь (ColaChanel) Коновалов,'
                     ' Данилл (X_O_R_S) Шаманаев,'
                     ' Назари (Nazari) Кирилов,'
                     ' Артём (zqwy01) Синицын,'
                     ' Даниил (Kar En Tuk) Торопчин', className='neurofooter')
    # '''dcc.Upload(
    #     id='upload-image',
    #     children=html.Div([
    #         'Drag and Drop or ',
    #         html.A('Select Files')
    #     ]),
    #     style={
    #         'width': '100%',
    #         'height': '60px',
    #         'lineHeight': '60px',
    #         'borderWidth': '1px',
    #         'borderStyle': 'dashed',
    #         'borderRadius': '5px',
    #         'textAlign': 'center',
    #         'margin': '10px'
    #     },
    #     # Allow multiple files to be uploaded
    #     multiple=False
    # ),'''
    #html.Div(id='output-image-upload'),
])

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

@app.callback([Output('left', 'children'),
              Output('right', 'children'),
              Output('table', 'children')],
              Input('upload-image', 'contents'),
              prevent_initial_call=True)
def update_output(content):
    if content is not None:
        encoded = dio.url_to_pillow(content)
        (data, image) = NeuronetAPI.predict(encoded)
        content = [
            dcc.Upload(id='upload-image',
            children = [html.Img(src=content, className='neuroimg',)],
            accept='image/*'
            ),
            html.Label('Нажмите на изображение для загрузки нового')
        ]
        img = [html.Img(src=image, className='neuroimg'),html.Label('Результат')]
        table=html.Div(className='empty-table', children=html.Label('БЖУ таблица', className='labelc'))
        if not data.empty:
            table = [
                generate_table(data),
                html.Label('Данные БЖУ таблицы на 100 грамм', className='label-table'),
            ]
        return content, img, table

def open_browser():
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        webbrowser.open('http://127.0.0.1:5000/')

if __name__ == '__main__':
    Timer(1, open_browser).start()
    app.run_server(debug=True, port=5000)

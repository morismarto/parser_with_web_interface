from pynput.keyboard import Key, Controller
from flask import Flask, render_template, request, jsonify
from notifypy import Notify
import webbrowser
import os
from scraper import Parser
from time import sleep

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST', 'GET'])
def submit():
    Parser(url=request.json['url'], headless=False, stealth_mode=True).parse()
    return jsonify({k: v for k, v in zip(range(Parser.length_product_descr()), Parser.get_data())})
    

# @app.route('/table')
# def table():
#     return 


exiting = False
@app.route('/shutdown')
def shutdown():
    global exiting
    exiting = True
    return 'Done'

@app.teardown_request
def teardown(e):
    if exiting:
        os._exit(0)

@app.route('/focus')
def focus():
    keyboard = Controller()
    keyboard.press(Key.tab)
    return 'Sucsess'

    

def notify():
    notification = Notify()
    notification.title = "Парсер"
    notification.message = "Парсер запущен на localhost..."
    notification.send(block=False)


if __name__ == '__main__':
    notify()
    webbrowser.open(url='http://127.0.0.1:5000', new=0)
    app.run()

# -*- coding: utf-8 -*-
from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests
import json

# from xmljson import badgerfish as bf
# from xml.etree.ElementTree import fromstring
# from json import dumps
# import xmltodict

app = Flask(__name__)


def getXMLData(url):
    try:
        response = requests.get(url)
    except:
        return 'HTTP GET Error!'

    text = response.text.encode('utf-8')
    soup = BeautifulSoup(text, 'lxml')
    items = soup.findAll('items')

    #	print(items[0])
    #	print('JSON')
    # jsonString = xmltodict.parse(str(items[0]), encoding='utf-8')
    # print(jsonString)

    return items


@app.errorhandler(500)
def internalServerError(e):
    return render_template('500.html'), 500


@app.route("/")
def index():
    uri = 'http://apis.data.go.kr/9710000/BillInfoService/getBillInfoList?serviceKey=D%2FiJQ8nHK7VOJpnJoTTt%2F234%2FUsP8ujCvSRKfw60Z%2FXk0JJfUDr5FrUWAurDfQsgV7uxMKd2Sh0u0YMnAYXs9w%3D%3D&numOfRows=999&pageSize=999&pageNo=1&startPage=1'

    items = getXMLData(uri)

    return render_template('index.html', items=items)


@app.route('/search/<string:keyword>')
def search(keyword):
    uri = 'http://apis.data.go.kr/9710000/BillInfoService/getBillInfoList?serviceKey=p7UBJeNZxl1cDhlLLsZT3H0ikrzKZ7miawcXdCvHKVm%2FjpxWbvKb1UWDyJlL7oNp7CTHgLejQR0QYax17zG46Q%3D%3D&numOfRows=999&pageSize=999&pageNo=1&startPage=1'
    item = None

    # obj = getXMLData(uri)
    # obj = obj['items']
    # for x in range(999):
    #     if keyword == obj['item'][x]['name']:
    #         return dumps(obj['item'][x])


@app.route('/congressman/<string:name>')
def congressman(name):
    uri = 'http://apis.data.go.kr/9710000/NationalAssemblyInfoService/getMemberCurrStateList?serviceKey=p7UBJeNZxl1cDhlLLsZT3H0ikrzKZ7miawcXdCvHKVm%2FjpxWbvKb1UWDyJlL7oNp7CTHgLejQR0QYax17zG46Q%3D%3D&numOfRows=999&pageSize=999&pageNo=1&startPage=1'
    item = None

    # obj = getXMLData(uri)
    # obj = obj['items']
    # for x in range(999):
    #     if name == obj['item'][x]['empnm']:
    #         return dumps(obj['item'][x])

    return render_template('500.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)

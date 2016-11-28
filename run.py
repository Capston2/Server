# -*- coding: utf-8 -*-
from flask import Flask, render_template
from bs4 import BeautifulSoup
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
from json import dumps
import requests
import json
import xmltodict

app = Flask(__name__)


def getXMLData(url):
    try:
        response = requests.get(url)
    except:
        return 'HTTP GET Error!'

    text = response.text.encode('utf-8')
    soup = BeautifulSoup(text, 'xml')
    items = soup.findAll('items')

    jsonString = xmltodict.parse(str(items[0]), encoding='utf-8')

    return jsonString


@app.errorhandler(500)
def internalServerError(e):
    return render_template('500.html'), 500


@app.route("/")
def index():
    # uri = 'http://apis.data.go.kr/9710000/BillInfoService/getBillInfoList?ServiceKey=p7UBJeNZxl1cDhlLLsZT3H0ikrzKZ7miawcXdCvHKVm%2FjpxWbvKb1UWDyJlL7oNp7CTHgLejQR0QYax17zG46Q%3D%3D&numOfRows=10&pageSize=1&pageNo=1&startPage=1'

    # recentAcceptUri : 최근 접수 의안 목록 / recentPassUri : 최근 통과 의안 목록
    # 서버 구축용 uri로 변경하세요
    recentAcceptUri = 'http://apis.data.go.kr/9710000/BillInfoService/getRecentRceptList?serviceKey=81X0zTkpezfhufKJUndC9%2FRZIdYNmpQznY%2BrF%2B92eKA04rYuKZj7B6kfSIwSDvwBjPRClZRMQ2vRk19eYyp57A%3D%3D&numOfRows=10&pageSize=10&pageNo=1&startPage=1'
    recentPassUri = 'http://apis.data.go.kr/9710000/BillInfoService/getRecentPasageList?serviceKey=81X0zTkpezfhufKJUndC9%2FRZIdYNmpQznY%2BrF%2B92eKA04rYuKZj7B6kfSIwSDvwBjPRClZRMQ2vRk19eYyp57A%3D%3D&numOfRows=10&pageSize=10&pageNo=1&startPage=1'

    acceptItems = getXMLData(recentAcceptUri)
    passItems = getXMLData(recentPassUri)

    return render_template('index.html', acceptItems=acceptItems['items']['item'], passItems=passItems['items']['item'])


@app.route('/search/<string:keyword>')
def search(keyword):
    uri = 'http://apis.data.go.kr/9710000/BillInfoService/getBillInfoList?serviceKey=p7UBJeNZxl1cDhlLLsZT3H0ikrzKZ7miawcXdCvHKVm%2FjpxWbvKb1UWDyJlL7oNp7CTHgLejQR0QYax17zG46Q%3D%3D&numOfRows=999&pageSize=999&pageNo=1&startPage=1'

    xmlData = getXMLData(uri)

    for x in range(999):
        if keyword == xmlData[x]['billname']:
            return xmlData[x]

    return render_template('500.html')


@app.route('/congressman/<string:name>')
def congressman(name):
    uri = 'http://apis.data.go.kr/9710000/NationalAssemblyInfoService/getMemberCurrStateList?serviceKey=D%2FiJQ8nHK7VOJpnJoTTt%2F234%2FUsP8ujCvSRKfw60Z%2FXk0JJfUDr5FrUWAurDfQsgV7uxMKd2Sh0u0YMnAYXs9w%3D%3D&numOfRows=999&pageSize=999&pageNo=1&startPage=1'

    xmlData = getXMLData(uri)
    print(xmlData['items']['item'][0]['empNm'] == name)

    for x in range(999):
        if name == xmlData['items']['item'][x]['empNm']:
            return render_template('peopledetail.html', item=xmlData['items']['item'][x])
            # return xmlData['items']['item'][x]

    return render_template('500.html')


@app.route('/peopledetail')
def peopledetail():
    return render_template('peopledetail.html')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)

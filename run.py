# -*- coding: utf-8 -*-
from flask import Flask, render_template
from bs4 import BeautifulSoup
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
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

	return render_template('index.html', acceptItems = acceptItems['items']['item'], passItems = passItems['items']['item'])

@app.route('/top')
def top():
	uri = 'hello'

	return 'Top'

@app.route('/bill/<string:id>')
def informationBill(id):
	uri = 'hello'

	return id

@app.route('/search/<string:keyword>')
def search(keyword):
	uri = 'hello'

	return keyword

@app.route('/congressman/<string:name>')
def congressman(name):
	uri = 'hello'

	return name

@app.route('/detail')
def post():
    return render_template('detail.html')

@app.route('/peoplelist')
def peoplelist():
    return render_template('peoplelist.html')

@app.route('/peopledetail')
def peopledetail():
    return render_template('peopledetail.html')

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000, debug=True)

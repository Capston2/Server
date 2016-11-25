# -*- coding: utf-8 -*-
from flask import Flask, render_template
from bs4 import BeautifulSoup
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
import requests
from json import dumps
import xmltodict

app = Flask(__name__)

@app.route("/")
def hello():
	uri = 'http://apis.data.go.kr/9710000/BillInfoService/getBillInfoList?ServiceKey=p7UBJeNZxl1cDhlLLsZT3H0ikrzKZ7miawcXdCvHKVm%2FjpxWbvKb1UWDyJlL7oNp7CTHgLejQR0QYax17zG46Q%3D%3D&numOfRows=10&pageSize=1&pageNo=1&startPage=1'

	try:
		response = requests.get(uri)
	except:
		return 'HTTP GET Error!'

	text = response.text.encode('utf-8')
	soup = BeautifulSoup(text, 'lxml')
	items = soup.findAll('items')

	print(items[0])
	print("JSON")
	jsonString = xmltodict.parse(str(items[0]), encoding='utf-8')
	print(jsonString)

	return render_template('index.html', items=items)

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8001, debug=True)

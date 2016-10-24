from flask import Flask
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route("/")
def hello():
	uri = 'http://apis.data.go.kr/9710000/BillInfoService/getBillInfoList?ServiceKey=p7UBJeNZxl1cDhlLLsZT3H0ikrzKZ7miawcXdCvHKVm%2FjpxWbvKb1UWDyJlL7oNp7CTHgLejQR0QYax17zG46Q%3D%3D&numOfRows=10&pageSize=10&pageNo=1&startPage=1'

	try:
		response = requests.get(url)
		text = response.text
	except:
		return 'Error'

	soup = BeautifulSoup(text, 'lxml')

	titles = soup.find_all('div', 'mem_name')
	for title in titles:
		print(title)
	return soup

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8000, debug=True)
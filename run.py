from flask import Flask, render_template
import requests
import xmltodict

app = Flask(__name__)

server_key = 'D%2FiJQ8nHK7VOJpnJoTTt%2F234%2FUsP8ujCvSRKfw60Z%2FXk0JJfUDr5FrUWAurDfQsgV7uxMKd2Sh0u0YMnAYXs9w%3D%3D'

@app.route('/')
def main():
    recent_recept_list_cnt = 5
    recent_pasage_list_cnt = 5

    recent_recept_list_url = 'http://apis.data.go.kr/9710000/BillInfoService/getRecentRceptList?serviceKey=%s&numOfRows=%d&pageSize=%d&pageNo=1&startPage=1' % (server_key, recent_recept_list_cnt, recent_recept_list_cnt)
    recent_pasage_list_url = 'http://apis.data.go.kr/9710000/BillInfoService/getRecentPasageList?serviceKey=%s&numOfRows=%d&pageSize=%d&pageNo=1&startPage=1' % (server_key, recent_pasage_list_cnt, recent_pasage_list_cnt)

    recent_recept_list_xml = requests.get(recent_recept_list_url).content
    recent_pasage_list_xml = requests.get(recent_pasage_list_url).content

    recent_recept_list_dict = xmltodict.parse(recent_recept_list_xml)
    recent_pasage_list_dict = xmltodict.parse(recent_pasage_list_xml)

    recent_recept_list = []
    recent_pasage_list = []

    for k in recent_recept_list_dict['response']['body']['items']['item']:
        recent_recept_list.append(list(k.values()))

    for k in recent_pasage_list_dict['response']['body']['items']['item']:
        recent_pasage_list.append(list(k.values()))

    return render_template('index.html', receptItems=recent_recept_list, passItems=recent_pasage_list)

@app.route('/bill/<id>')
def bill_detail(id):
    bill_detail_info_url = 'http://apis.data.go.kr/9710000/BillInfoService/getBillReceiptInfo?serviceKey=%s&bill_id=%s' % (server_key, id)

    bill_detail_info_xml = requests.get(bill_detail_info_url).content

    bill_detail_info_dict = xmltodict.parse(bill_detail_info_xml)

    bill_detail_info = bill_detail_info_dict['response']['body']['item']['receipt']

    return render_template('detail.html', billInfo=bill_detail_info)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
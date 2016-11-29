from flask import Flask, render_template

from bs4 import BeautifulSoup
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

    if recent_recept_list_dict['response']['header']['resultCode'] != '00':
        return render_template('500.html'), 500
    if recent_pasage_list_dict['response']['header']['resultCode'] != '00':
        return render_template('500.html'), 500

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
    bill_petition_member_url = 'http://apis.data.go.kr/9710000/BillInfoService/getBillPetitionMemberList?serviceKey=%s&bill_id=%s' % (server_key, id)

    bill_detail_info_xml = requests.get(bill_detail_info_url).content
    bill_petition_member_xml = requests.get(bill_petition_member_url).content

    bill_detail_info_dict = xmltodict.parse(bill_detail_info_xml)
    bill_petition_member_dict = xmltodict.parse(bill_petition_member_xml)

    if bill_detail_info_dict['response']['header']['resultCode'] != '00':
        return render_template('500.html'), 500
    if bill_petition_member_dict['response']['header']['resultCode'] != '00':
        return render_template('500.html'), 500

    bill_detail_info = bill_detail_info_dict['response']['body']['item']['receipt']

    bill_petition_member_list = []
    for k in bill_petition_member_dict['response']['body']['items']['item']:
        if (k['gbn1'] == '의안'):
            if ([k['memName'], k['polyNm']] not in bill_petition_member_list):
                bill_petition_member_list.append([k['memName'], k['polyNm']])

    bill_summary = bill_summary_crawler('PRC_R1M6R1J1R2K9Y1B8A0J4Z2K1L3M0C0').split('\n')

    return render_template('detail.html', billId=id, billInfo=bill_detail_info, billPetitionMembers=bill_petition_member_list, billSummary=bill_summary)

@app.route('/congressman/<page>')
def get_congressman_list(page):
    congressman_cnt = 8

    congressman_list_url = 'http://apis.data.go.kr/9710000/NationalAssemblyInfoService/getMemberCurrStateList?ServiceKey=%s&numOfRows=%d&pageNo=%s' % (server_key, congressman_cnt, page)
    congressman_list_xml = requests.get(congressman_list_url).content
    congressman_list_dict = xmltodict.parse(congressman_list_xml)

    if congressman_list_dict['response']['header']['resultCode'] != '00':
        return render_template('500.html'), 500

    numOfRows = int(congressman_list_dict['response']['body']['numOfRows'])
    totalCount = int(congressman_list_dict['response']['body']['totalCount'])

    numOfPages = round(totalCount / numOfRows + 0.5)
    congressmanList = congressman_list_dict['response']['body']['items']['item']

    return render_template('peoplelist.html', curPage=page, numOfPages=numOfPages, congressmanList=congressmanList)


def bill_summary_crawler(bill_id):
    url = 'http://likms.assembly.go.kr/bill/billDetail.do?billId='+str(bill_id)
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'lxml')

    return soup.find(id='summaryContentDiv').text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
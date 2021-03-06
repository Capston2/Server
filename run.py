from flask import Flask, render_template, request

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

    if bill_petition_member_dict['response']['body']['items']:
        for k in bill_petition_member_dict['response']['body']['items']['item']:
            if (k['gbn1'] == '의안'):
                if ([k['memName'], k['polyNm']] not in bill_petition_member_list):
                    bill_petition_member_list.append([k['memName'], k['polyNm']])

    bill_summary = bill_summary_crawler(id).split('\n')

    return render_template('detail.html', billId=id, billInfo=bill_detail_info, billPetitionMembers=bill_petition_member_list, billSummary=bill_summary)

@app.route('/congressman/<page>')
def get_congressman_list(page):
    congressman_cnt = 12

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

@app.route('/congressman/detail/<name>')
def get_congressman_detail(name):
    congressman_list_url = 'http://apis.data.go.kr/9710000/NationalAssemblyInfoService/getMemberCurrStateList?ServiceKey=%s&numOfRows=999&pageNo=1' % (server_key)
    congressman_list_xml = requests.get(congressman_list_url).content
    congressman_list_dict = xmltodict.parse(congressman_list_xml)

    if congressman_list_dict['response']['header']['resultCode'] != '00':
        return render_template('500.html'), 500

    congressman_list = []
    for k in congressman_list_dict['response']['body']['items']['item']:
        if k['empNm'] == name:
            congressman_list.append(k)

    congressman_detail_info_url = 'http://apis.data.go.kr/9710000/NationalAssemblyInfoService/getMemberDetailInfoList?serviceKey=%s&numOfRows=1&pageNo=1&dept_cd=%s&num=%s' % (server_key, congressman_list[0]['deptCd'], congressman_list[0]['num'])
    congressman_detail_info_xml = requests.get(congressman_detail_info_url).content
    congressman_detail_info_dict = xmltodict.parse(congressman_detail_info_xml)

    if congressman_detail_info_dict['response']['header']['resultCode'] != '00':
        return render_template('500.html'), 500

    congressman_detail_info = congressman_detail_info_dict['response']['body']['item']

    return render_template('peopledetail.html', congressmanPicture=congressman_list[0]['jpgLink'], congressmanDetailInfo=congressman_detail_info)


def bill_summary_crawler(bill_id):
    url = 'http://likms.assembly.go.kr/bill/billDetail.do?billId='+str(bill_id)
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'lxml')

    if soup.find(id='summaryContentDiv'):
        return soup.find(id='summaryContentDiv').text
    else:
        return ''

@app.route('/search', methods=['POST'])
def search() :
    bill_search_list_cnt = 5
    keyword = request.form['keyword']

    bill_search_url = 'http://apis.data.go.kr/9710000/BillInfoService/getBillInfoList?serviceKey=%s&numOfRows=%s&pageNo=1&bill_name=%s'  % (server_key, bill_search_list_cnt, keyword)
    bill_search_list_xml = requests.get(bill_search_url).content
    bill_search_list_dict = xmltodict.parse(bill_search_list_xml)

    if bill_search_list_dict['response']['header']['resultCode'] != '00':
        return render_template('500.html'), 500

    congressman_list_url = 'http://apis.data.go.kr/9710000/NationalAssemblyInfoService/getMemberCurrStateList?ServiceKey=%s&numOfRows=999&pageNo=1' % (
    server_key)
    congressman_list_xml = requests.get(congressman_list_url).content
    congressman_list_dict = xmltodict.parse(congressman_list_xml)

    if congressman_list_dict['response']['header']['resultCode'] != '00':
        return render_template('500.html'), 500

    congressman_list = []
    for k in congressman_list_dict['response']['body']['items']['item']:
        if k['empNm'] == keyword:
            congressman_list.append(k)

    bill_search_List = []
    if bill_search_list_dict['response']['body']['items']:
        bill_search_List = bill_search_list_dict['response']['body']['items']['item']

    return render_template('searchresult.html', billList = bill_search_List, congressmanList = congressman_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

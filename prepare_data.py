## global list
import re
import requests
import pandas as pd
import numpy as np
import json

name_of_country = []
info = []
list_flag = []
list_capital = []
list_HeadGoverment = []
list_info = []
list_map = []
links = []


def GET_LINK():
    url = "https://www.britannica.com/topic/list-of-countries-1993160"
    html_data = requests.get(url).text
    #name = re.findall(r'<a href="https://www.britannica.com/place/(.*?)" ',str(html_data))
    regx_link = re.findall(
        r'<a href="(https://www.britannica.com/place/(.*?))" ', str(html_data))

    for ele in regx_link:
        link = ele[0]
        links.append(link)
    print("Prepare Links successful")


def GET_FLAGURL(req):
    # GET FLAG URL
    # flag 2 แบบ Flag flag ทำให้ไม่ matched เลยใช้แค่ (_lag)
    linkFlag = re.findall('<img loading="lazy" src="(.*?lag.*?)"', req)
    if(linkFlag):
        list_flag.append(linkFlag[0])
    else:
        linkFlag = re.findall('<img loading="lazy" src="(.*?FLAG.*?)"', req)
        if(linkFlag):
            list_flag.append(linkFlag[0])
        else:
            # ใช้กับประเทศ South Sudan เพราะใน link ไม่มีคำว่า flag เลย
            linkFlag = re.findall('<img loading="lazy" src="(.*?)"', req)
            list_flag.append(linkFlag[1])


def GET_CAPITAL(req):
    nameOfCapital = re.findall('<a href="/place/.*?>(.*?)</a>', req)
    if(nameOfCapital):
        list_capital.append(nameOfCapital[0])
    else:
        nameOfCapital = re.findall(
            '<dt class="d-inline">Capital:</dt>\n\t\t\t\t<dd class="d-inline">\n\t\t\t\t\t<span class="fact-item">(.*?)<', req)
        if(nameOfCapital):
            list_capital.append(nameOfCapital[0])
        else:
            list_capital.append("NAN")


def GET_INFO(req):
    rawInfo = re.findall('<p class="topic-paragraph".*?>(.*)</p>', req)
    if(rawInfo != []):
        SumInfo = ''
        for i in range(len(rawInfo)):
            cleanInfo = re.sub('<.*?>', '', rawInfo[i])  # remove html tag
            SumInfo += cleanInfo  # sum all info
        list_info.append(SumInfo)
    else:
        print("error")


list_prefix = ['President: ', 'Prime Minister: ',
               'Prime Minister:', 'Premier: ', 'King: ', 'Supreme Leader']


def GET_DIRECTOR(req):
    # ใช้ได้กับชื่อที่เป็น tag span ไม่ matched กับ ชื่อที่เป็น tag a
    HeadOf = re.findall(
        'Head.*?Government.*:</dt>\n\t\t\t\t<dd class="d-inline">\n\t\t\t\t\t<span class="fact-item">(.*?)<', req)
    # ถ้า HeadOf ดึงข้อมูลมาได้แค่ prefix จะไม่เข้าเงื่อนไข
    if(HeadOf != [] and HeadOf[0] not in list_prefix):
        list_HeadGoverment.append(HeadOf[0])
    else:
        # ใช้กับชื่อที่มี tag a >> prefix + name
        pre = re.findall(
            'Head.*?Government:</dt>\n\t\t\t\t<dd class="d-inline">\n\t\t\t\t\t<span class="fact-item">(.*?)<', req)  # prefix
        name = re.findall(
            'Head.*?Government:</dt>\n\t\t\t\t<dd class="d-inline">\n\t\t\t\t\t<span class="fact-item">.*?: <a href=".*?>(.*?)<', req)  # name
        if(HeadOf != [] and pre[0] != '' and name[0] != ''):
            headname = pre[0]+name[0]
            list_HeadGoverment.append(headname)
        else:
            # ประเทศ Vatican-City ไม่มีหัวข้อ HeadOf เลยเพิ่มชื่อจากที่หาในวิกิไป
            list_HeadGoverment.append("President: Giuseppe Bertello")


def GET_MAP(req):
    # re เช็ค link ที่มีคำว่า map หรือ Map
    linkmap = re.findall(
        '<img src="(https://cdn.britannica.com/.*?[m|M]ap-.*?)"', req)
    if(linkmap != []):
        # มีบางประเทศ re match ได้มาหลาย link แต่ส่วนใหญ่ตัวสุดท้ายใน list จะเป็น link map ที่ต้องการ
        list_map.append(linkmap[len(linkmap)-1])
    else:
        usaMap = re.findall(
            '<img src="(https://cdn.britannica.com/.*?The-United-States.*?)"', req)  # for USA
        if(usaMap):
            list_map.append(usaMap[len(usaMap) - 1])
        else:
            list_map.append("NaN")


def PROCESSING():
    # RESET LISTS

    for url in links:
        r = requests.get(url)
        req = r.text

        # GET NAME OF COUNTRY
        nameOfCountry = re.findall('.*<h1 class="mb-0">(.*)</h1>', req)
        if(nameOfCountry):
            name_of_country.append(nameOfCountry[0])

        # GET FLAG URL
            GET_FLAGURL(req)

        # GET CAPTITAL
            GET_CAPITAL(req)

        # GET DIRECTOR
            GET_DIRECTOR(req)

        # GET INFO
            GET_INFO(req)

        # GET MAP URL
            GET_MAP(req)
        else:
            nameList.append("NAN")

    print(len(list_flag), " flag Url")
    print(len(list_capital), " cappital")
    print(len(list_info), " info")
    print(len(list_HeadGoverment), "head of gov.")
    print(len(list_map), "map")

    print("Creating JSON FILES")
    name_df = pd.DataFrame(name_of_country, columns=["name"])
    capital_df = pd.DataFrame(list_capital, columns=["capital"])
    info_df = pd.DataFrame(list_info, columns=["info"])
    flagUrl_df = pd.DataFrame(list_flag, columns=["flagUrl"])
    sourceUrl_df = pd.DataFrame(links, columns=["sourceUrl"])
    headGoverment = pd.DataFrame(
        list_HeadGoverment, columns=["headOfGoverment"])
    mapUrl_df = pd.DataFrame(list_map, columns=["mapUrl"])
    pack = [name_df, capital_df, info_df, flagUrl_df,
            headGoverment, mapUrl_df, sourceUrl_df]
    country_data = pd.concat(pack, axis=1, join="inner")
    #
    json_str = country_data.to_json(orient='records')
    parsed = json.loads(json_str)

    with open("./database/data.json", "w", encoding="utf-8") as outfile:
        json.dump(parsed, outfile, ensure_ascii=False)
        print("Creating JSON FILES Sucessfully =========>")


def SCRAPING_PROCESS():

    GET_LINK()
    PROCESSING()


def read_data():
    with open("./database/data.json", encoding='utf-8') as f:
        data = json.load(f)
    return data

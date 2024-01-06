import time
from urllib import request
from http import cookiejar
import requests
from lxml import etree
import re
import random



url = "http://wrggk.whvcse.edu.cn/web/MyCourse.aspx"
random_url = random.randint(2923947, 2935043)

username = '20'
password = '03'

url_login = f"https://wrggk.whvcse.edu.cn/auth.aspx?action=login&username={username}&password={password}&callback=?&random=1234567"

print(url_login)

global SessionId
global UserAuthentication
cookie = cookiejar.CookieJar()
handler = request.HTTPCookieProcessor(cookie)
opener = request.build_opener(handler)
response = opener.open(url_login)

for item in cookie:
    if item.name == 'ASP.NET_SessionId':
        SessionId = item.value
    if item.name == 'UserAuthentication':
        UserAuthentication = item.value

cookies = {"UserAuthentication": f"UserName={username}", "ASP.NET_SessionId": f"{SessionId}"}

headers = {
    "Pragma": "no-cache", "Cache-Control": "no-cache",
    "Sec-Ch-Ua": "\"Google Chrome\";v=\"111\", \"Not(A:Brand\";v=\"8\", \"Chromium\";v=\"111\"",
    "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Sec-Fetch-Site": "cross-site", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6,zh-HK;q=0.5"
}
# 个人获取课程
response = requests.get(url, headers=headers, cookies=cookies, verify=False)
html = etree.HTML(response.text)
title = html.xpath("//div[@class='coursera-dashboard-course-listing-box-name']/a/text()")
title_id = html.xpath("//div[@class='coursera-dashboard-course-listing-box-links']/a[2]/@href")
cid_href = html.xpath(
    "//div/a[@class='enter coursera-dashboard-course-listing-box-go-button btn-flat btn-flat-success']/@href")
if title == None:
    print("当前无选择课程")
else:
    for i in range(0, len(title)):
        print(f"{i + 1}、{title[i]}")
    a = input("请选择需要刷的课程：")
    if a == "all":
        for x, y, z in zip(title_id, title, cid_href):
            title_id_x = re.findall(r"id=(.*)&cid", x)[0]
            cid_href_z = re.findall(r"&cid=(.*)", z)[0]

            course_url = "https://wrggk.whvcse.edu.cn/Web/CourseInfo.aspx?id={}&cid={}".format(title_id_x, cid_href_z)

            pid_href_response = requests.get(url, headers=headers, cookies=cookies, verify=False).text
            pid_href_response_html = etree.HTML(pid_href_response)
            pid_href = pid_href_response_html.xpath('//h4[@class="c-font-normal"]/a[1]/@href')
            # print(pid_href)

            print("{}:{}".format(y, course_url))
            response_cource = requests.get(course_url, headers=headers, cookies=cookies, verify=False)

            cource_html = etree.HTML(response_cource.text)
            begin = cource_html.xpath('//div[@class="c-col-no-left-padding"]/div[1]/a[1]/@href')
            # print(begin)
            ####输出视频网址
            view = "Viewer"
            count_view = 0
            for i in begin:
                if view in i:
                    # print(i)
                    mid_id = re.findall(r"mid=(.*)&courseClassId", i)
                    # print(mid_id)
                    # print(mid_id[0])
                    count_view += 1
                    data = {
                        'cpid': '{}'.format(mid_id[0]),
                        'bjtime': '1000',
                        'courseid': '{}'.format(title_id_x),
                        'stepid': '{}'.format(mid_id[0]),
                        'courseClassId': '{}'.format(cid_href_z),
                        't': '60'
                    }
                    shuake_url = "https://wrggk.whvcse.edu.cn/Viewer/timetop.aspx?cpid={}&bjtime=1000&courseid={}&stepid={}&courseClassId={}&t=60".format(
                        mid_id[0], title_id_x, mid_id[0], cid_href_z)
                    resp_shuake_url = requests.post(shuake_url, headers=headers, data=data, cookies=cookies,
                                                    verify=False)
                    time.sleep(1)
                    print("已经完成视频:{}".format(shuake_url))

            print("{}课程视频总共有{}个".format(y, count_view))
    else:
        for x, y, z in zip(title_id, title, cid_href):
            if a == y:
                title_id_x = re.findall(r"id=(.*)&cid", x)[0]
                cid_href_z = re.findall(r"&cid=(.*)", z)[0]

                course_url = "https://wrggk.whvcse.edu.cn/Web/CourseInfo.aspx?id={}&cid={}".format(title_id_x,
                                                                                                   cid_href_z)

                pid_href_response = requests.get(url, headers=headers, cookies=cookies, verify=False).text
                pid_href_response_html = etree.HTML(pid_href_response)
                pid_href = pid_href_response_html.xpath('//h4[@class="c-font-normal"]/a[1]/@href')
                # print(pid_href)

                print("{}:{}".format(y, course_url))
                response_cource = requests.get(course_url, headers=headers, cookies=cookies, verify=False)

                cource_html = etree.HTML(response_cource.text)
                begin = cource_html.xpath('//div[@class="c-col-no-left-padding"]/div[1]/a[1]/@href')
                # print(begin)
                ####输出视频网址
                view = "Viewer"
                count_view = 0
                for i in begin:
                    if view in i:
                        # print(i)
                        mid_id = re.findall(r"mid=(.*)&courseClassId", i)
                        # print(mid_id)
                        # print(mid_id[0])
                        count_view += 1
                        data = {
                            'cpid': '{}'.format(mid_id[0]),
                            'bjtime': '1000',
                            'courseid': '{}'.format(title_id_x),
                            'stepid': '{}'.format(mid_id[0]),
                            'courseClassId': '{}'.format(cid_href_z),
                            't': '60'
                        }
                        shuake_url = "https://wrggk.whvcse.edu.cn/Viewer/timetop.aspx?cpid={}&bjtime=1000&courseid={}&stepid={}&courseClassId={}&t=60".format(
                            mid_id[0], title_id_x, mid_id[0], cid_href_z)
                        resp_shuake_url = requests.post(shuake_url, headers=headers, cookies=cookies, data=data,
                                                        verify=False)
                        time.sleep(1)
                        # print("需要发送的视频网址:{}".format(shuake_url))
                        print("已完成的视频:{}".format(shuake_url))

                print("{}课程视频总共有{}个".format(y, count_view))
for x, y, z in zip(title_id, cid_href, title):
    title_id_x = re.findall(r"id=(.*)&cid", x)[0]
    cid_href_y = re.findall(r"&cid=(.*)", y)[0]
    course_url = "http://wrggk.whvcse.edu.cn/Web/CourseInfo.aspx?id={}&cid={}".format(title_id_x, cid_href_y)
    # 获取考试地址
    resp_course_url = requests.get(course_url, headers=headers, cookies=cookies, verify=False).text
    cource_html = etree.HTML(resp_course_url)
    total_url = 'http://wrggk.whvcse.edu.cn'
    CourseExam = 'CourseExam'
    exam_url = cource_html.xpath('//a/@href')
    for i in exam_url:
        if CourseExam in i:
            print(z)
            Exam_url = total_url + i
            id = re.findall(r"id=(.*)&sid", Exam_url)[0]
            sid = re.findall(r"&sid=(.*)&mid", Exam_url)[0]
            courseClassId = re.findall(r"&courseClassId=(.*)&chapterId", Exam_url)[0]
            pid = re.findall(r"&pid=(.*)", Exam_url)[0]
            resp_for_userid = requests.get(Exam_url, headers=headers, cookies=cookies, verify=False).text
            resp_for_userid_html = etree.HTML(resp_for_userid)
            userid_xpath = resp_for_userid_html.xpath('//div[@class="c-main-content-container"]/div/div[2]/iframe/@src')
            userid = re.findall(r'(?<=&userid=)\d{5}', userid_xpath[0])
            # 答案网址
            answer_url = 'http://wrggkk.whvcse.edu.cn//excute/DoPaper.aspx?classid={}&stepid={}&paperid={}&courseid={}&userid=80681&username=&examCountId=&times=1&view=1'.format(
                courseClassId, sid, pid, id)

            data = {
                'classid': '{}'.format(courseClassId),
                'stepid': '{}'.format(sid),
                'paperid': '{}'.format(pid),
                'courseid': '{}'.format(id),
                'userid': '80681',
                'username': '',
                'examCountId': '',
                'times': '1',
                'view': '1'
            }
            an_headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                "Cache-Control": "max-age=0",
                "Connection": "keep-alive",
                "Cookie": "ASP.NET_SessionId=vz0aeab5p5hehmmisskrdi0t",
                "Host": "wrggkk.whvcse.edu.cn",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 Edg/105.0.1343.33"
            }
            at = 'http://wrggkk.whvcse.edu.cn//excute/DoPaper.aspx?classid=758&stepid=12684&paperid=af30b149-6106-40d9-9f13-a634d306d335&courseid=1006&userid=87217&examCountId=&times=1&username='
            resp_answer_url = requests.post(url=at, data=data, headers=headers, cookies=cookies, verify=False)
            print(answer_url)

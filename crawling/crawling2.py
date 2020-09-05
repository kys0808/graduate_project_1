import urllib.request
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# 웹 애플리케이션의 테스트를 자동화하기 위한 프레임 워크
# 손으로 마우스 클릭해서 데이터를 검색하고 스크롤링 할 수 있다

import time
# 중간마다 sleep를 걸어야 한다.

binary = 'chromedriver.exe'
# 크롬 웹 브라우저를 열기 위한 크롬 드라이버
# 팬텀 js를 이용하면 백그라운드로 실행 할 수 있음.

browser = webdriver.Chrome(binary)
browser.get("https://search.naver.com/search.naver?where=image&amp;sm=stb_nmr&amp;")
# 네이버의 이미지 검색 url
elem = browser.find_element_by_id("nx_query")
# nx_query는 네이버 이미지 검색에 해당하는 input창 id
elem.send_keys("우레탄 볼라드")
elem.submit()
# 스크롤링( 스크롤을 내리는 동작)을 반복할 횟수
for i in range(1, 8):
    browser.find_element_by_xpath("//body").send_keys(Keys.END)
    # 웹창을 클릭 후 END키를 누르는 동작
    # 브라우저 아무데서나 END키 누른다고 페이지가 내려가지 않음
    # body를 활성화한 후 스크롤 동작
    time.sleep(5)
    # 이미지가 로드 되는 시간 5초
    # 로드가 되지 않은 상태에서 자장하기 되면 No image로 뜸.
time.sleep(5)
# 네트워크의 속도를 위해 걸어둔 sleep
html = browser.page_source
# 크롬 브라우저에서 현재 불러온 소스 코드를 가져옴

soup = BeautifulSoup(html,'html.parser')
# beautiful soup을 사용해서 html 코드를 검색할 수 있도록 설정

def fetch_list_url():
    # 이미지를 url이 있는 img 태그의 img클래스로 감
    params = []
    imgList = soup.find_all(class_="_img")
    print(imgList)
    for img in imgList:
        # params 리스트 변수에 images url을 담음
        params.append(img["src"])
    return params

def fetch_detail_url():
    params = fetch_list_url()
    print(params)
    print(len(params))
    a = 1
    for p in params:
        # 다운받을 폴더경로 입력
        urllib.request.urlretrieve(p,  '../yolo/crawl_img/'+ str(a) + ".jpg")
        print("{} complete" .format(a))
        a = a + 1

fetch_detail_url()
# 브라우저 창 닫기
browser.quit()
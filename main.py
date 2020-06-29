from flask import Flask, render_template, request
app = Flask(__name__,static_folder="static")

import requests
from bs4 import BeautifulSoup

@app.route('/')

def hello():
    
    list_daum_woman, list_daum_woman_href, list_daum_man, list_daum_man_href, list_daum_womann, list_daum_womann_href, list_daum_mann, list_daum_mann_href = daum()

    list_today, list_today_href = today()   
    
    list_clien, list_clien_href = clien()

    return render_template("index.html",
                           daumone = list_daum_woman , 
                           daumone_href = list_daum_woman_href ,
                           daumone_len = len(list_daum_woman) ,

                           daumtwo = list_daum_man ,
                           daumtwo_href = list_daum_man_href ,
                           daumtwo_len = len(list_daum_man) ,

                           daumthree = list_daum_womann ,
                           daumthree_href = list_daum_womann_href ,
                           daumthree_len = len(list_daum_womann) , 

                           daumfour = list_daum_mann ,   
                           daumfour_href = list_daum_mann_href ,
                           daumfour_len = len(list_daum_mann) ,

                           today = list_today , 
                           today_href = list_today_href ,
                           today_len = len(list_today)
                           )
                           #clien = list_clien, clien_href = list_clien_href
                           

# @app.route('/today')
# def today():

#   list_today = get_today()

#   return ''

def daum():

  req = requests.get('https://news.daum.net/ranking/age')
  soup = BeautifulSoup(req.text, 'html.parser')

  list_daum_woman = []
  list_daum_woman_href = []
  list_daum_man= []
  list_daum_man_href= []
  list_daum_womann = []
  list_daum_womann_href= []
  list_daum_mann = []
  list_daum_mann_href= []
  

  for i in soup.select("#mArticle > div.rank_news > div.item_age.item_20s > div.rank_female > ol > li"):
      list_daum_woman.append(i.find("a").text)
      list_daum_woman_href.append(i.find("a")["href"])


  for i in soup.select("#mArticle > div.rank_news > div.item_age.item_20s > div.rank_male > ol > li"):
      list_daum_man.append(i.find("a").text)
      list_daum_man_href.append(i.find("a")["href"])

  for i in soup.select("#mArticle > div.rank_news > div.item_age.item_30s > div.rank_female > ol > li"):
      list_daum_womann.append(i.find("a").text)
      list_daum_womann_href.append(i.find("a")["href"])

  for i in soup.select("#mArticle > div.rank_news > div.item_age.item_30s > div.rank_male > ol > li"):
      list_daum_mann.append(i.find("a").text)
      list_daum_mann_href.append(i.find("a")["href"])

  return list_daum_woman, list_daum_woman_href, list_daum_man, list_daum_man_href, list_daum_womann, list_daum_womann_href, list_daum_mann, list_daum_mann_href



def today():

    req = requests.get('http://www.todayhumor.co.kr/board/list.php?table=bestofbest')

    soup = BeautifulSoup(req.text, 'html.parser')

    list_today = []
    list_today_href = []

    # scrap_result = soup.select("body > div.whole_box > div > div > table > tbody > tr")

    for i in soup.find_all("td", class_="subject") :
        list_today.append(i.text)
        list_today_href.append("http://www.todayhumor.co.kr/"+i.find("a")["href"])
           
    # scrap_result = list(scrap_result)

    # for element in scrap_result:
    #     if element.find('a') is not None:
    #       list_today.append(element.find('a').attrs['href'])
    #       list_today.append(element.find('a').text)
      
    return list_today, list_today_href #함수로 만들어서 에러가 났었음. 

def clien():

    req = requests.get('https://www.clien.net/service/recommend')

    soup = BeautifulSoup(req.text, 'html.parser')

    list_clien = []
    list_clien_href = []

    for i in soup.find_all("span", class_="subject_fixed") :
        list_clien.append(i.text)
        # list_clien_href.append("https://www.clien.net"+i["href"])
    
    return list_clien, list_clien_href



@app.route('/result', methods=['POST'])
def result():
    
    keyword = request.form['input1']
    page = request.form['input2']

    # https://search.daum.net/search?nil_suggest=btn&w=news&DA=PGD&cluster=y&q=%EC%95%88%EB%85%95&p=2

    # https://search.daum.net/search?nil_suggest=btn&w=news&DA=PGD&cluster=y&q=%EC%95%88%EB%85%95&p=1

    daum_list = []

    for i in range(1, int(page) + 1):

        req = requests.get("https://search.daum.net/search?nil_suggest=btn&w=news&DA=PGD&cluster=y&q="+ keyword +"&p=" + page)

        soup = BeautifulSoup(req.text, 'html.parser')

        for i in soup.find_all("a", class_="f_link_b"):
           daum_list.append(i.text)


    

    return render_template("result.html", daum_list = daum_list)

if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
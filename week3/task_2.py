import urllib.request as req
import bs4
import csv
		
complete_post_data = []

def getData(url):
	
	#建立一個 Request 物件，附加 Request Headers 的資訊（以模仿真實使用者）
	request=req.Request(url, headers={
		"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
		"cookie":"over18=1"
	})
	#用 request 物件打開網址
	with req.urlopen(request) as response:
		data=response.read().decode("utf-8") #經過read和decode之後的request，會是字串型態的網頁原始碼（就像在瀏覽器按右鍵「檢查」看到的東西）

	#解析原始碼，取得每篇文章的標題(利用 beautifulsoup)
	import bs4
	root=bs4.BeautifulSoup(data,"html.parser") #建立beatifulsoup物件，參數一：網頁原始碼，參數二：html.parser為python內建html解析器，結合 beautifulsoup 能將網頁原始碼轉換為標籤樹
	titles = root.find_all("div", class_="title") #轉換成標籤樹後，就可用 element 尋找網頁內容。尋找所有 class="title"的 div 標籤。
	likes = root.find_all("div", class_="nrec")
	
	for title, like in zip(titles, likes):

		if title.a != None: #如果標題包含 a 標籤（沒有被刪除），印出來 #!=是不等於的意思
			post_title = title.a.string
			article_url = "https://www.ptt.cc" + title.a['href']
			article_request = req.Request(article_url, headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
                "cookie": "over18=1"
            })
			with req.urlopen(article_request) as article_response:
				article_data = article_response.read().decode("utf-8")
				article_root = bs4.BeautifulSoup(article_data, "html.parser")
				meta_values = article_root.find_all("span", class_="article-meta-value")
				if len(meta_values) >= 4:
					post_time = meta_values[3].string
				else:
					post_time = ""
					
		if like.span != None:
			like_count = like.span.string
		else:
			like_count = ""
		complete_post_data.append([post_title, like_count, post_time])

	#抓取上一頁的連結
	nextLink = root.find("a", string="‹ 上頁") #找到內文是‹ 上頁的 a 標籤
	return nextLink["href"] #將找到的上一頁 url return 到呼叫函式處。["href"] 是存取該超連結 <a> 標籤的 href 屬性。beautifulsoup 產生的標籤是「類字典物件」，所以可以用類似 dict[key] 的方法取得值。

#抓取一個頁面的標題
pageURL = "https://www.ptt.cc/bbs/Lottery/index.html"

count = 0
while count<3:
	pageURL = "https://www.ptt.cc"+getData(pageURL)
	count+=1

with open("article.csv", mode="w", newline="", encoding="utf-8") as lottery_board_file:
	writer = csv.writer(lottery_board_file)
	for single_data in complete_post_data:
	    writer.writerow(single_data)


	
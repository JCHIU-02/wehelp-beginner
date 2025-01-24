import urllib.request as req
import bs4
import csv
		
complete_post_data = []

def getData(url):
	
	request=req.Request(url, headers={
		"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
		"cookie":"over18=1"
	})
	with req.urlopen(request) as response:
		data=response.read().decode("utf-8")

	import bs4
	root=bs4.BeautifulSoup(data,"html.parser")
	titles = root.find_all("div", class_="title")
	likes = root.find_all("div", class_="nrec")
	
	for title, like in zip(titles, likes):

		if title.a != None:
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

	nextLink = root.find("a", string="‹ 上頁")
	return nextLink["href"]


pageURL = "https://www.ptt.cc/bbs/Lottery/index.html"

count = 0
while count<3:
	pageURL = "https://www.ptt.cc"+getData(pageURL)
	count+=1

with open("article.csv", mode="w", newline="", encoding="utf-8") as lottery_board_file:
	writer = csv.writer(lottery_board_file)
	for single_data in complete_post_data:
	    writer.writerow(single_data)


	

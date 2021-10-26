from django.shortcuts import render

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from Water import models


def main(request):
	return render(request, 'index.html')


def POST_crawl(request):
	keyword = request.POST["title"]
	text = {"name": "", "water": ""}

    # 使用者讀取資料庫的資料(如果有的話)
	if models.water.objects.get(name=keyword):
		unit = models.water.objects.get(name=keyword)
		text["name"] = unit.name
		text["water"] = unit.water
		print('Cached data!')
		return render(request, 'result.html', locals())

	# 水利署網頁
	url = "https://fhy.wra.gov.tw/ReservoirPage_2011/StorageCapacity.aspx"

	options = Options()
	# 關閉瀏覽器跳出訊息
	prefs = {
		'profile.default_content_setting_values':
			{
				'notifications' : 2
			}
	}
	options.add_experimental_option('prefs', prefs)
	options.add_argument("--headless")            # 不開啟實體瀏覽器背景執行
	options.add_argument("--incognito")           # 開啟無痕模式


	driver = webdriver.Chrome("chromedriver", options=options) # 你的本地爬蟲瀏覽器位置

	driver.get(url)
	sel = driver.find_element_by_id('ctl00_cphMain_gvList')
	pool = driver.find_elements_by_xpath("//*[contains(text(), \'" + keyword + "\')]/following-sibling::td")
	print(pool[0].get_attribute('innerHTML'))

	text["name"] = keyword
	text["water"] = pool[0].get_attribute('innerHTML')

	# 爬好的資料儲存在資料庫
	try:
		unit = models.water.objects.get(name=text["name"])
		unit.water = text["water"]
		unit.save()
		print('Updated!')
	except:
		unit = models.water.objects.create(name=text["name"], water=text["water"])
		unit.save()
		print('Created!')

	# 把爬蟲完的資訊送去前端
	return render(request, 'result.html', locals())
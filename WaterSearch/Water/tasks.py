from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from Water import models


def regular_crawl():
    keyword_list = ['石門水庫', '翡翠水庫', '寶山第二水庫', '永和山水庫', '明德水庫', '鯉魚潭水庫', '德基水庫', '石岡壩', '霧社水庫', '日月潭水庫', '集集攔河堰', '湖山水庫', '仁義潭水庫', '白河水庫', '烏山頭水庫', '曾文水庫', '南化水庫', '阿公店水庫', '高屏溪攔河堰', '牡丹水庫']

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
	
    for keyword in keyword_list:
        pool = driver.find_elements_by_xpath("//*[contains(text(), \'" + keyword + "\')]/following-sibling::td")
        print(pool[0].get_attribute('innerHTML'))
        
        try:
            unit = models.water.objects.get(name=keyword)
            unit.water = pool[0].get_attribute('innerHTML')
            unit.save()
            print('Updated!')
        except:
            unit = models.water.objects.create(name=keyword, water=pool[0].get_attribute('innerHTML'))
            unit.save()
            print("Created!")
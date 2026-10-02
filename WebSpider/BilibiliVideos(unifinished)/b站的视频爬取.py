from DrissionPage import ChromiumPage
import requests


page = ChromiumPage()

page.get('http://bilibili.com')
page.wait(2)
page.ele('@class=nav-search-input').input('影视飓风')
page.wait(2)
page.ele('@class=nav-search-btn').click()
page.wait(2)
print(page.eles('@class=v-img bili-video-card__cover')[0])
# page.eles('@class=v-img bili-video-card__cover')[0]



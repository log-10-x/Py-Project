from lxml import etree
# import xpath
import requests


home_url = 'https://haowallpaper.com/'
headers = {
    'useragent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36'
    }

response = requests.get(url=home_url, headers=headers)
response.encoding = 'utf-8'

tree = etree.HTML(response.text)

print(response.text)
# print(tree)

video_urls = tree.xpath('//div[@class="home-container"]//video/@src')
video_names = tree.xpath('//div[@class="home-container"]//video/@title')

for zipped in zip(video_urls, video_names):
    with open(f'wallpaper/{zipped[1]}.mp4', 'wb') as f:
        response = requests.get(url=zipped[0], headers=headers)
        f.write(response.content)

picture_urls = tree.xpath('//div[@class="home-container"]//img/@src')
picture_names = tree.xpath('//div[@class="home-container"]//img/@title')

for zipped in zip(picture_urls, picture_names):
    # print(zipped[0])
    with open(f'wallpaper/{zipped[1]}.jpg', 'wb') as f:
        response = requests.get(url=zipped[0], headers=headers)
        f.write(response.content)



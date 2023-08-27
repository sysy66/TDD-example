from selenium import webdriver
from selenium.webdriver.firefox.options import Options
options = Options()
options.add_argument("-profile")
options.add_argument("/home/caolv/snap/firefox/common/.cache/mozilla/firefox/45s3kzyu.default")
browser = webdriver.Firefox(options=options)

browser.get('http://localhost:8000')
assert 'Django' in browser.title

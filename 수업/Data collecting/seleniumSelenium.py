from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from requests import Session, get

driver = Chrome(r'./news/chromedriver.exe')
driver.get('https://www.naver.com/')
driver.find_element(By.XPATH, '//body//div[@id="account")//a')
# for _ in driver.find_element(By.XPATH, '//ul[@class="panel_wrap"]//input[@class="input_text"]'):
#     print(_.tag_name, _.get_attribute('id'))

session = Session()

for _ in driver.get.cookies():
    session.cookies.set(_['name'], _['value'])


for k, v in session.cookies.get_dict().items():
  driver.add_cookie({'name':k, 'value':v})

driver.find_element(By.CSS_SELECTOR, '#gnb_name2 + .gnb_btn_login').click()
driver.implicitly_wait(10)
driver.find_element(By.CSS_SELECTOR, '.gnb_btn_login').get_attribute('href')
driver.find_element(By.CSS_SELECTOR, '#gnb_my_layer').click()

wait = WebDriverWait(driver, timeout=10)
wait.until(expected_conditions.element_to_be_clickable(By.CSS_SELECTOR, '#gnb_my_layer'))
#wait.until_not()   # 원하는 기능이 로드가 끝날때까지만 기다릴 수 있다.

# tab 이름들
driver.window_handles
# 마지막 탭으로 이동
driver.switch_to.window(driver.window_handles[-1])

# 페이지의 html driver.page_source

iframe = driver.find_element(By.CSS_SELECTOR, '#mainFrame')
driver.switch_to.frame(iframe)
driver.find_element(By.CSS_SELECTOR, 'body').text
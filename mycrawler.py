from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import pickle






# 自動管理 ChromeDriver
service = Service(ChromeDriverManager().install())

# 啟動瀏覽器
options = webdriver.ChromeOptions()
#options.add_argument("--start-maximized")  # 啟動時最大化
# 啟動瀏覽器
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # 啟動時最大化
#options.add_argument("--headless")  # 啟用無頭模式
options.add_argument("--disable-gpu")  # 若系統是 Windows，建議禁用 GPU（防止某些情況下出錯）
options.add_argument("--no-sandbox")  # 解決某些環境中的權限問題（例如 Linux）
options.add_argument("--disable-dev-shm-usage")  # 避免共享內存不足的問題（在容器環境中有用）

driver = webdriver.Chrome(service=service, options=options)





# driver.get("https://www.facebook.com/?locale=zh_TW")  # 請換成你的網站網址
# time.sleep(2)


# email = "fred.yah@mars-deg.com"
# password = "Fb@19840913"


# driver.find_element(By.ID, "email").send_keys(email)
# driver.find_element(By.ID, "pass").send_keys(password)
# driver.find_element(By.NAME, "login").click()

# time.sleep(20)

# with open("facebook_cookies.pkl", "wb") as f:
#     pickle.dump(driver.get_cookies(), f)


driver.get("https://www.facebook.com/?locale=zh_TW")
time.sleep(2)


with open("cache.pkl", "rb") as f:
    cookies = pickle.load(f)
    for cookie in cookies:
        driver.add_cookie(cookie)



driver.get("https://www.facebook.com/settings")
time.sleep(20)

input("按 Enter 鍵退出...")

driver.quit()
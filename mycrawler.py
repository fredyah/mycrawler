import os
import time
import requests
import pickle
import io

import pyperclip
import pyautogui

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import random
import csv
from selenium.common.exceptions import TimeoutException

# ---------------------------
# 函式 1: 下載並返回 pickle 資料 (cookies)
# ---------------------------
def getPKL():
    """
    從 GitHub 上下載 cache.pkl 檔案，並以 BytesIO 形式返回。
    """
    url = "https://github.com/fredyah/mycrawler/raw/refs/heads/main/cache.pkl"
    response = requests.get(url)
    if response.status_code == 200:
        return io.BytesIO(response.content)
    else:
        raise ValueError(f"下載失敗，狀態碼: {response.status_code}")

def get_random_picture(current_path):
    pictures_dir = os.path.join(current_path, 'pictures')
    picture_files = [f for f in os.listdir(pictures_dir) if f.lower().endswith(('jpg', 'jpeg', 'png'))]
    if picture_files:
        mypicture = os.path.join(pictures_dir, random.choice(picture_files))
        
    else:
        mypicture = None
        print("❌ 沒有找到任何個人頭像圖片")

    return mypicture

def get_random_background(current_path):
    backgrounds_dir = os.path.join(current_path, 'backgrounds')
    background_files = [f for f in os.listdir(backgrounds_dir) if f.lower().endswith(('jpg', 'jpeg', 'png'))]
    if background_files:
        myBackGround = os.path.join(backgrounds_dir, random.choice(background_files))
        
    else:
        myBackGround = None
        print("❌ 沒有找到任何個人頭像圖片")

    return myBackGround


def get_random_introduction(current_path):
    introduction_dir = os.path.join(current_path, 'introductions')
    introduction_files = [f for f in os.listdir(introduction_dir) if f.lower().endswith(('csv'))]
    if introduction_files:
        for introduction in introduction_files:
            myintroductions = os.path.join(introduction_dir, introduction)
            with open(myintroductions, mode='r', newline='', encoding='utf-8') as file:
                # 使用 csv.reader 讀取檔案內容
                csv_reader = csv.reader(file)
                
                # 將檔案內容轉換為 list
                data_list = list(csv_reader)
            myintroduction = random.choice(data_list)
        
    else:
        introduction_files = None
        print("❌ 沒有找到任何個人頭像圖片")

    return myintroduction



# ---------------------------
# 類別：包含瀏覽器初始化，以及上傳大頭貼的流程
# ---------------------------
class FacebookBot:
    def __init__(self, headless=False):
        """
        初始化瀏覽器（ChromeDriver）。
        可根據需求，將 headless 設為 True 或 False。
        """
        # 自動管理 ChromeDriver
        service = Service(ChromeDriverManager().install())

        # 瀏覽器選項
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        if headless:
            options.add_argument("--headless")

        # 啟動瀏覽器
        self.driver = webdriver.Chrome(service=service, options=options)

    def login_with_cookies(self, pkl_bytes):
        """
        透過 pickle 中的 cookies 直接登入 Facebook。
        pkl_bytes: 由 getPKL() 返回的 BytesIO 物件
        """
        cookies = pickle.load(pkl_bytes)

        # 先開啟 Facebook 首頁
        self.driver.get("https://www.facebook.com/?locale=zh_TW")
        time.sleep(1)

        # 載入 cookies
        for cookie in cookies:
            self.driver.add_cookie(cookie)

        # 再次載入，讓 cookies 生效
        self.driver.get("https://www.facebook.com/?locale=zh_TW")
        time.sleep(1)

    def upload_picture(self, picture_path):
        """
        上傳大頭貼的流程：
        1. 前往個人頁面
        2. 點擊「更新大頭貼照」
        3. 點擊「上傳相片」
        4. 用 pyperclip + pyautogui 輸入檔案路徑
        5. 點擊「儲存」
        """
        driver = self.driver

        # 前往個人頁面
        driver.get("https://www.facebook.com/me/")
        time.sleep(1)

        # 點擊「更新大頭貼照」
        try:
            avatar_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[contains(@aria-label, "更新大頭貼照")]')))
            avatar_button.click()
            time.sleep(1)
        except Exception as e:
            print("找不到更新大頭像按鈕:", e)
            return

        # 點擊「上傳相片」
        try:
            upload_option = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "上傳相片")]')))
            upload_option.click()
            time.sleep(1)
        except Exception as e:
            print("找不到上傳相片選項:", e)
            return

        # 用 pyperclip + pyautogui 輸入檔案路徑
        try:
            pyperclip.copy(picture_path)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter', presses=2)
            time.sleep(1)
        except Exception as e:
            print("輸入檔案路徑失敗:", e)
            return

        # 點擊「儲存」
        try:
            save_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[contains(@aria-label, "儲存")]')))
            save_button.click()
            time.sleep(1)
        except Exception as e:
            print("找不到儲存按鈕:", e)

    def quit(self):
        """
        關閉瀏覽器。
        """
        self.driver.quit()


    def uploadBackground(self, picture_path):
        driver = self.driver
        driver.get("https://www.facebook.com/me/")
        try:
            # 這裡的 XPath 可能會變動，建議用瀏覽器開發者工具確認最新的元素定位方式
            avatar_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[contains(@aria-label, "新增封面相片") or contains(@aria-label, "編輯封面相片")]')))
            avatar_button.click()
            time.sleep(1)
        except Exception as e:
            print("找不到新增封面相片按鈕:", e)
            return

        try:
            upload_option = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "上傳相片")]')))
            upload_option.click()
            time.sleep(1)
        except Exception as e:
            print("找不到上傳相片選項:", e)
            return

        try:
            pyperclip.copy(picture_path)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter', presses=2)
            time.sleep(1)
        except Exception as e:
            print("輸入失入:", e)
            return

        try:
            save_button = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//*[contains(@aria-label, "儲存變更")]')))
            if len(save_button) > 1:
                for buttons in save_button:
                    try:
                        buttons.click()  # 第 2 個按鈕
                        time.sleep(1)
                    except Exception as e:
                        print("這個是假按鍵:", e)
            else:
                print("找不到第二個 '儲存變更' 按鈕")
                save_button.click()
                time.sleep(1)
        except Exception as e:
            print("找不到儲存按鈕:", e)



    def updateMyIntroduction(self, myIntroduction):
        driver = self.driver
        driver.get("https://www.facebook.com/me/")
        try:
            # 這裡的 XPath 可能會變動，建議用瀏覽器開發者工具確認最新的元素定位方式
            avatar_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[contains(@aria-label, "新增個人簡介") or contains(@aria-label, "編輯個人簡介")]')))
            avatar_button.click()
            time.sleep(1)
        except Exception as e:
            print("找不到新增封面相片按鈕:", e)
            return


        try:
            textarea = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//textarea[@aria-label='輸入個人簡介']")))
            textarea.send_keys(Keys.CONTROL + "a")  # 選取全部內容 (Mac 使用 COMMAND)
            textarea.send_keys(Keys.BACKSPACE)      # 刪除
            textarea.send_keys(myIntroduction)
        except Exception as e:
            print("找不到輸入個人簡介位置:", e)
            return


        # 點擊「儲存」
        try:
            save_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[contains(@aria-label, "儲存")]')))
            save_button.click()
            time.sleep(1)
        except Exception as e:
            print("找不到儲存按鈕:", e)

        try:
            share_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[contains(@aria-label, "立即分享")]')))
            share_button.click()
            time.sleep(1)
        except Exception as e:
            print("找不到儲存按鈕:", e)



    def newPost(self):
        driver = self.driver
        driver.get("https://www.facebook.com/me/")
        try:
            # 這裡的 XPath 可能會變動，建議用瀏覽器開發者工具確認最新的元素定位方式
            avatar_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "在想些什麼？")]')))
            avatar_button.click()
            time.sleep(1)
        except Exception as e:
            print("找不到發新動態按鈕:", e)
            return
        
        try:
            textarea = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[contains(@aria-label, "在想些什麼？")]')))
            textarea.send_keys('我都笑翻了!!\nhttps://www.youtube.com/watch?v=L3V7nu5wqa4')
            time.sleep(5)
        except Exception as e:
            print("找不到輸入位置:", e)
            return

        # 點擊「儲存」
        try:
            save_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "發佈")]')))
            save_button.click()
            time.sleep(5)
        except Exception as e:
            print("找不到儲存按鈕:", e)

        try:
            # 這裡的 XPath 可能會變動，建議用瀏覽器開發者工具確認最新的元素定位方式
            goodJob_buttons = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//*[contains(@aria-label, "讚")]')))
            goodJob_buttons[0].click()
            time.sleep(2)
        except Exception as e:
            print("找不到讚按鍵:", e)



    def shareNewPost(self):
        driver = self.driver
        try:
            # 這裡的 XPath 可能會變動，建議用瀏覽器開發者工具確認最新的元素定位方式
            share_buttons = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//*[contains(@aria-label, "傳送給朋友或在個人檔案上發佈。")]')))
            share_buttons[0].click()
            time.sleep(1)
        except Exception as e:
            print("找不到分享按鍵:", e)


        try:
            textarea = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[contains(@aria-label, "留個話吧⋯⋯")]')))
            textarea.send_keys('這也太好笑了吧!!')
        except Exception as e:
            print("找不到輸入位置:", e)
            return


        try:
            # 這裡的 XPath 可能會變動，建議用瀏覽器開發者工具確認最新的元素定位方式
            group_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@aria-label="統一分享工作表中可用的「分享位置」選項清單。"]//*[contains(text(), "社團")]')))
            group_button.click()
            time.sleep(1)
        except Exception as e:
            print("找不到群組按鍵:", e)
            return

        try:
            # 這裡的 XPath 可能會變動，建議用瀏覽器開發者工具確認最新的元素定位方式
            target_group_buttons = WebDriverWait(driver, 30).until(EC.presence_of_all_elements_located((By.XPATH, '//*[contains(text(), "我的測試社團")]')))
            target_group_buttons[-1].click()
            time.sleep(1)
        except Exception as e:
            print("找不到目標社團:", e)

        try:
            # 這裡的 XPath 可能會變動，建議用瀏覽器開發者工具確認最新的元素定位方式
            submit_buttons = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "發佈")]')))
            submit_buttons.click()
            time.sleep(1)
        except Exception as e:
            print("找不到發佈按鍵:", e)


    def public_or_unPublic(self):
        driver = self.driver
        driver.get("https://www.facebook.com/settings/?tab=posts")

        try:
            element = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "只限本人")]')))
            myStatus = "所有人"
        except TimeoutException:
            myStatus = "只限本人"

        try:
            # 這裡的 XPath 可能會變動，建議用瀏覽器開發者工具確認最新的元素定位方式
            set_status_buttons = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "誰可以查看你之後的貼文？")]')))
            set_status_buttons.click()
            time.sleep(2)
        except Exception as e:
            print("找不到設定是否公開按鍵:", e)

        try:
            # 這裡的 XPath 可能會變動，建議用瀏覽器開發者工具確認最新的元素定位方式
            set_status_buttons = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "{}")]'.format(myStatus))))
            set_status_buttons.click()
            time.sleep(1)
        except Exception as e:
            print("找不到設定是否公開按鍵:", e)

        try:
            submit_set_status = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[contains(@aria-label, "儲存")]')))
            submit_set_status.click()
        except Exception as e:
            print("找不到完成按鍵:", e)
            return

# ---------------------------
# 主程式：示範如何使用
# ---------------------------
if __name__ == "__main__":
    # 1. 取得目前路徑，並組合圖片路徑
    current_path = os.getcwd()
    # 2. 下載並載入 cookies
    pkl_data = getPKL()
    bot = FacebookBot(headless=False)  # 如需無頭模式可設 headless=True
    bot.login_with_cookies(pkl_data)


    #for i in range(3):
    myPicture = get_random_picture(current_path)
    myBackground = get_random_background(current_path)
    myInterDuction = get_random_introduction(current_path)[0]



    # 3. 建立 FacebookBot 實例，登入並上傳大頭貼
    bot.public_or_unPublic()
    time.sleep(5)
    bot.upload_picture(myPicture)
    time.sleep(5)
    bot.uploadBackground(myBackground)
    time.sleep(5)
    bot.updateMyIntroduction(myInterDuction)
    time.sleep(5)
    bot.newPost()
    time.sleep(5)
    bot.shareNewPost()

    # 4. 結束
    time.sleep(10000000)
    bot.quit()






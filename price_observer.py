import os
import sys
import json
import time
import requests
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()
api_key = os.getenv('steam_api_key')
uid = os.getenv('steam_user_id')
itad_key = os.getenv('ITAD_api_key')

class WishListGameInfo:

    def get_wish_list_app_ids(self):
        driver = webdriver.Chrome()
        wishlist_url = "https://store.steampowered.com/wishlist/profiles/76561199064613136/"
        driver.get(wishlist_url)
        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'pOyXxbQoV38-')))

        wishlist_games_elements = driver.find_elements(By.CLASS_NAME, 'pOyXxbQoV38-')
        self.wishlist_games_urls = []
        for i in wishlist_games_elements:
            self.wishlist_games_urls.append(i.get_attribute('href'))
        driver.quit()
        self.app_ids = []
        for j in range(len(self.wishlist_games_urls)):
            self.app_ids.append(self.wishlist_games_urls[j].split('/')[4])
        return self.app_ids

    def get_app_details(self):
        self.wishlist_apps_detail = []
        app_detail_url = "https://store.steampowered.com/api/appdetails"
        for i in range(len(self.app_ids)):
            r = requests.get(app_detail_url, params={"appids": self.app_ids[i], "cc": "jp", "l": "japanese"}, timeout=30).json()
            node = r.get(str(self.app_ids[i]), {})
            if not node["success"]:
                return None
            app_data = node["data"].copy()
            app_price = app_data.get("price_overview")
            app_detail = {}
            app_detail.update({
                "name": app_data.get("name"),
                "header_image": app_data.get("header_image"),
            })
            if not app_data["is_free"]:
                if app_price["discount_percent"] != 0:
                    app_detail.update({"price_initial": app_price.get("initial_formatted"),
                                "price_display": app_price.get("final_formatted"),
                                })
                else:
                    app_detail.update({"price_display": app_price.get("final_formatted")})
            else:
                app_detail.update({"price_final": "￥0"})
            self.wishlist_apps_detail.append(app_detail)
            time.sleep(1)
        return self.wishlist_apps_detail
    
wishlist = WishListGameInfo()
wishlist.get_wish_list_app_ids()
wishlist.get_app_details()
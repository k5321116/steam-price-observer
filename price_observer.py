import json
import requests
import sys
import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

api_key = config.api_key
uid = config.uid

def GetOwnedGames(api_key, uid):
    url = "http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={}&steamid={}&format=json".format(
        api_key, uid
    )
    r = requests.get(url)
    if r.status_code != 200: 
        print(f"Status Code: {r.status_code}")
        print(f"Response Text: {r.text}")
        print('所持しているゲームの取得中にエラーが発生しました。')
        sys.exit()
    else:    
        data = json.loads(r.text)
        return data["response"]
    
def GetPlayerSummaries(api_key, uid):
    url = "http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}&steamids={}&format=json".format(
        api_key, uid
    )
    r = requests.get(url)
    if r.status_code != 200: 
        print(f"Status Code: {r.status_code}")
        print(f"Response Text: {r.text}")
        print('player summariesの取得中にエラーが発生しました。')
        sys.exit()
    else:    
        data = json.loads(r.text)
        return data["response"]
    
def GetMyWishListGames():
    driver = webdriver.Chrome()
    wishlist_url = "https://store.steampowered.com/wishlist/profiles/76561199064613136/"
    driver.get(wishlist_url)
    wait = WebDriverWait(driver, 30)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'pOyXxbQoV38-')))

    wishlist_games_elements = driver.find_elements(By.CLASS_NAME, 'pOyXxbQoV38-')
    wishlist_games_urls= []
    for i in wishlist_games_elements:
        wishlist_games_urls.append(i.get_attribute('href'))
    driver.quit()
    app_ids = []
    for j in range(len(wishlist_games_urls)):
        app_ids.append(wishlist_games_urls[j].split('/')[4])
    return app_ids

def GetMyWishListGamePrice()

owned_games = GetOwnedGames(api_key, uid)
games = owned_games['games']
owned_games_number = len(games)
player_summaries = GetPlayerSummaries(api_key, uid)

#print(owned_games_number)
#print(player_summaries['players'][0]['personaname']) 

app_ids = GetMyWishListGames()
print(app_ids)
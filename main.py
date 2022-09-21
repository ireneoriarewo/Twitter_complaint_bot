from csv import DictReader
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

chrome_driver_path = "FILE PATH"
s = Service(chrome_driver_path)

MIN_SPEED = 20

class InternetSpeedTwitterBot:
    def __init__(self, driver_path):
        self.s = Service(chrome_driver_path)
        self.driver = webdriver.Chrome(service=self.s)
        self.driver.maximize_window()
        self.up = 0
        self.down = 0

    def document_initialised(self, driver):
        return self.driver.execute_script("return initialised")

    def get_cookies_value(self, file):
    #copy and paste cookies to a csv file, if cookies are loaded properly, the signing in process would not be necessary
        with open(file) as f:
            self.dict_reader = DictReader(f)
            self.list_of_dicts = list(self.dict_reader)
        return self.list_of_dicts

    def get_internet_speed(self):

        self.driver.get('https://www.speedtest.net/')

        sleep(5)
        go_button = self.driver.find_element(By.CSS_SELECTOR, ".start-button a")
        go_button.click()

        sleep(60)
        self.up = self.driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text
        self.down = self.driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div[3]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span').text
        print(f"up:{self.up}\ndown: {self.down}")

    def tweet_at_provider(self):
        self.driver.get('https://twitter.com/')
        cookies = self.get_cookies_value('cookies.csv')
        for n in cookies:
            self.driver.add_cookie(n)
        self.driver.refresh()
        sleep(7)

        tweet_button = self.driver.find_element(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/header/div/div/div/div[1]/div[3]/a')
        tweet_button.send_keys(Keys.ENTER)

        sleep(2)

        text = f"@AirtelNigeria most of the time the network is really bad, i'm currently browsing at {self.down}Mbps"
        self.tweet = self.driver.find_element(By.CSS_SELECTOR, "div.notranslate.public-DraftEditor-content[aria-label='Tweet text']").send_keys(text)


        try:
            self.tweet.send_keys(text)
        except AttributeError:
            pass

        sleep(5)
        self.post = self.driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div/div[1]/div/div/div/div/div[2]/div[3]/div/div/div[2]/div[4]')
        self.post.click()



bot = InternetSpeedTwitterBot(chrome_driver_path)
bot.get_internet_speed()
bot.tweet_at_provider()

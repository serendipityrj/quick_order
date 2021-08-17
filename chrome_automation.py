from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common import desired_capabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import datetime
from selenium.webdriver import ActionChains
import winsound


chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_driver = "C:\\Users\\xiaoyu_shang\\Work\\Workspace\\env\\chromedriver.exe" 
desired_capabilities = DesiredCapabilities.CHROME
desired_capabilities['pageLoadStrategy'] = 'eager'

driver = webdriver.Chrome(chrome_driver, options=chrome_options)
f = open('log.log','a')

def monitor():
    if not 'taobao' in driver.current_url:
        print('Please open and log into Taobao')
        f.write(datetime.datetime.now().strftime('%Y%m%d %H%M%S' + ' '+ '[ERROR] - Open Chrome First\n'))
        return 1
    elif 'login' in driver.current_url:
        login()
        return 0
    else:
        driver.switch_to.window(driver.window_handles[0])
        # print('switch to Taobao')
        try:
            fav = driver.find_element_by_id('J_SiteNavFavor')
            # print(fav)
            fav.click()
            if 'login' in driver.current_url:
                login()
                return 0
            else:
                fav_items = driver.find_elements_by_class_name('fav-item')
                for item in fav_items:
                    title = item.find_element_by_xpath(".//a[@class='img-item-title-link']")
                    if 'PS5' in title.text:
                        try:
                            kd = item.find_element_by_xpath(".//div/span[@class='knockdown-tips']")
                            print('下架中...')
                            return 0
                        except Exception as e:
                            # print('No such Element Found')
                            # print('Product is available')
                            try:
                                # send_message()
                                # print('GOGOGO')
                                place_order(item)
                                f.write(datetime.datetime.now().strftime('%Y%m%d %H%M%S' + ' '+ '[SUCCESSFUL] - Product is available\n'))
                                return 1
                            except:
                                f.write(datetime.datetime.now().strftime('%Y%m%d %H%M%S' + ' '+ '[WARNING] - Place Order Failed\n'))
                                return 1
        except Exception as e:
            f.write(datetime.datetime.now().strftime('%Y%m%d %H%M%S' + ' '+ '[ERROR] - Page Error\n'))
            return 1

def run():
    try:
        stop = 0
        while(stop == 0):
            stop = monitor()
            time.sleep(10)
    except:
        f.close()

def send_message():
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(0.5)
    chats = driver.find_elements_by_xpath("//div[@class='info']//span[1]")
    # print(chats)
    for c in chats:
        print(c.text)
        if c.text== 'leia':
            c.click()
            break
    text_area = driver.find_element_by_xpath("//PRE[@id='editArea']")
    text_area.clear()
    text_area.send_keys("PS5 上架，去抢购")
    submit_button = driver.find_element_by_xpath("//A[@class='btn btn_send']")
    submit_button.click()
    
def place_order(product):
    product.click()
    driver.switch_to.window(driver.window_handles[1])
    colors = driver.find_element_by_class_name('tb-sku').find_elements_by_xpath(".//ul//li")
    for color in colors:
        if 'WB' in color.text:
            color.click()
            submit = driver.find_element_by_id('J_LinkBuy')
            submit.click()
            order = driver.find_element_by_class_name('go-btn')
            order.click()
            break

def drag(slider, track):
    ActionChains(driver).click_and_hold(slider).perform()
    for x in track:
        ActionChains(driver).move_by_offset(xoffset=x,yoffset=0).perform()
    time.sleep(0.5)
    ActionChains(driver).release().perform()


def simulate_track(distance):
    track=[]
    # 当前位移
    current=0
    # 减速阈值
    mid=distance*4/5
    # 计算间隔
    t=0.2
    # 初速度
    v=1
    while current<distance:
        if current<mid:
            # 加速度为2
            a=4
        else:
            # 加速度为-2
            a=-3
        v0=v
        # 当前速度
        v=v0+a*t
        # 移动距离
        move=v0*t+1/2*a*t*t
        # 当前位移
        current+=move
        # 加入轨迹
        track.append(round(move))
        return track

def login():
    name = driver.find_element_by_id('fm-login-id')
    name.clear()
    name.send_keys('18601110959')

    password = driver.find_element_by_id('fm-login-password')
    password.clear()
    password.send_keys('shangSXY19870907')
    submit = driver.find_element_by_xpath("//div[@class='fm-btn']//button")
    submit.click()
    time.sleep(2)
    if 'login' in driver.current_url:
        try:
            slider = driver.find_element_by_id('nc_1_n1z')
            drag(slider, simulate_track(259))
            time.sleep(10)
        except:
            f.write(datetime.datetime.now().strftime('%Y%m%d %H%M%S' + ' '+ '[ERROR] - Cant Find Slider\n'))

def play_alert():
    winsound.Beep(1440, 500)


run()

# https://login.taobao.com/member/login.jhtml?from=taobaoindex&f=top&style=&sub=true&redirect_url=https%3A%2F%2Fshoucang.taobao.com%2Fitem_collect_n.htm%3Fspm%3Da1z0k.7628869.1997525053.1.441a596fEPFUB0
# 300-42 + 1 = 259
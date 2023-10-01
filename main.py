from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import json
import config
import requests


def func():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome()
    driver.get('https://tanki.su/auth/oid/new/?next=/ru/daily-check-in/')
    sleep(5)
    
    login = driver.find_element(By.XPATH, '//*[@id="id_login"]')
    if login.is_displayed:
        login.send_keys(config.login)
        sleep(0.33)
    
    password = driver.find_element(By.XPATH, '//*[@id="id_password"]')
    if password.is_displayed:
        password.send_keys(config.password)
        sleep(0.33)
    
    checkbox = driver.find_element(By.XPATH, '//*[@id="jsc-remember-input-ba4f-d87b-"]/fieldset/label')
    if not checkbox.is_selected():
        checkbox.click()
        
    submit = driver.find_element(By.XPATH, '//*[@id="jsc-submit-button-df85-abc3-"]/button')
    if submit.is_displayed:
        submit.click()
    
    if not driver.find_element(By.XPATH, '//*[@id="jsc-captcha-input-9471-a0ad-"]').is_displayed():
        pass
    else:
        while not driver.find_element(By.XPATH, '//*[@id="jsc-captcha-input-9471-a0ad-"]').is_displayed():
            print('Таймаут 5 сек')
            sleep(5)
        else:
            print('Обнаружена капча')
            sleep(1)
            image_url = driver.find_element(By.XPATH, '//*[@id="js-basic-auth-captcha"]/div[1]/div[1]/img').get_attribute('src')
            response = requests.get(image_url)
            if response.status_code == 200:
                with open('captcha.jpg', 'wb') as f:
                    f.write(response.content)
                print("Изображение успешно скачано и сохранено.")
                code = input ('Код с капчи: ')
                driver.find_element(By.XPATH, '//*[@id="id_captcha"]').send_keys(code)
                sleep(0.33)
            else:
                print("Не удалось скачать изображение.")
    
    id_code = input('Введите одноразовый пароль: ')
    sleep (2)
    driver.find_element(By.XPATH, '//*[@id="id_code"]').send_keys(id_code)
    driver.find_element(By.XPATH, '//*[@id="jsc-submit-button-dd27-cbef-"]/button').click()
    input()
    sleep (5)
    if driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[4]/div[1]').is_displayed:
        print('Найден')
        driver.find_element(By.XPATH, '//*[@id="root"]/div[2]/div[4]/div[1]').click()
    else:
        print('Ничего не нашел')
    input()
    
func()  

import time
import selenium
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def test_prep(func):
    def wrapper(driver, val, currency_list):
        start_time = time.time()
        driver.get('https://qa.giam.finance/cabinet/invoices')
        wait = WebDriverWait(driver, 600)
        try:
            login = driver.find_element(By.ID, 'username')
            login.clear()

            pswd = driver.find_element(By.ID, "password")
            pswd.clear()

            login.send_keys('tyutyunnikalisha@gmail.com')
            pswd.send_keys('Q123123qqq')

            driver.find_element(By.CSS_SELECTOR, "button").click()
            print(f"Тестируемое значение  ({val}):")
            for currency in currency_list:
                func(driver, currency, val)


        except selenium.common.exceptions.NoSuchElementException:
            print(f'Тестируемое значение:  ({val}):')
            for coin in currency_list:
                print(bool(driver, coin, val))
        print("%s seconds " % (time.time() - start_time))
        print("______________________________________")
    return wrapper


@test_prep
def test_incorrect_gold_by(driver, currency, val):

    driver.get('https://qa.giam.finance/cabinet/token-sale')
    time.sleep(1)
    driver.find_element(By.CLASS_NAME, currency).click()
    value = driver.find_element(By.CSS_SELECTOR, 'input')
    value.send_keys(val)
    value.send_keys(Keys.DELETE)
    time.sleep(1)

    # time.sleep(5)
    try:
        driver.find_element(By.ID, 'buy_gold_btn').click()
        # skip = driver.find_elements(By.CLASS_NAME,'warning-popup')
        driver.find_element(By.CLASS_NAME, 'btns-wrap').click()
        time.sleep(2)
        driver.find_element(By.CSS_SELECTOR, 'button').click()
        time.sleep(5)
        res = driver.current_url
        if res == 'https://qa.giam.finance/cabinet/invoices':
            print(currency)
            print('Fail(Request was sent(Min))')
            return False
        elif (driver.find_element(By.CLASS_NAME, 'error_message')).text == 'Can not create a invoice':
            print(currency)
            print('OK (Can not create a invoice)')
            return True

    except selenium.common.exceptions.ElementNotInteractableException:
        driver.find_element(By.ID, 'request_gold_btn').click()
        driver.find_element(By.CSS_SELECTOR, 'button').click()
        time.sleep(2)
        res = driver.find_element(By.CLASS_NAME, 'success-popup')
        if res.text == 'Request was sent.':
            print(currency)
            print('Fail(Request was sent(Min))')
            return False
        elif (driver.find_element(By.CLASS_NAME, 'error_message')).text == 'Can not create a invoice':
            print(currency)
            print('OK (Can not create a invoice)')
            return True


currency_list = ["RUB", "UAH", "TMT", "MNT"]
# coin_list = ["EUR", 'XAF', "XOF", "RWF", "SLL", "GHS", "AOA", "RUB", "UAH", "TMT", "MNT"]

driver = webdriver.Chrome()
# #1 Ввод числа в экспоненциальном виде +
val = 'e45'
test_incorrect_gold_by(driver, val, currency_list)

# #2 Ввод большого числа +
val = '12030432414324000000'
test_incorrect_gold_by(driver, val, currency_list)

# #3 Ввод числа меньше минимального от 0 до 10 +
val = '5'
test_incorrect_gold_by(driver, val, currency_list)

# #4 Ввод отрицательно числа +
val = '-14'
test_incorrect_gold_by(driver, val, currency_list)

# #5 Ввод нули +
val = '000000000'
test_incorrect_gold_by(driver, val, currency_list)

#6 Ввод пустого поля
val = ''
test_incorrect_gold_by(driver, val, currency_list)

#7 Ввод точки '.'
val = '.'
test_incorrect_gold_by(driver, val, currency_list)
print(('End tests'))
driver.quit()


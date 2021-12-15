import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


def test_prep(func):
    def wrapper(a, b):
        driver = webdriver.Chrome()
        start_time = time.time()
        driver.get('https://qa.giam.finance/login')
        element = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.TAG_NAME, "html")))

        login = driver.find_element(By.ID, 'username')
        login.clear()

        pswd = driver.find_element(By.ID, "password")
        pswd.clear()

        login.send_keys(a)
        pswd.send_keys(b)

        driver.find_element(By.CSS_SELECTOR, "button").click()
        func(driver, login, pswd, start_time)

    return wrapper


@test_prep
def test_incorrect_input(driver, login, pswd, start_time):
    time.sleep(1)
    error = driver.find_element(By.CLASS_NAME, "error_message")
    # print(error.text)
    if error.text == 'Invalid credentials.':
        driver.quit()
        print("%s seconds -" % (time.time() - start_time))
        print(('Ok'))
        return True
    else:
        driver.quit()
        print("%s seconds -" % (time.time() - start_time))
        print(('FAIL'))
        return False


@test_prep
def test_correct_input(driver, login, pswd, start_time):
    time.sleep(1)
    # print(driver.current_url)
    if driver.current_url == 'https://qa.giam.finance/cabinet/dashboard':
        driver.quit()
        print("%s seconds -" % (time.time() - start_time))
        print(('Ok'))

        return True
    else:
        driver.quit()
        print("%s seconds -" % (time.time() - start_time))
        print(('FAIL'))
        return False


@test_prep
def test_empty_input(driver, login, pswd, start_time):
    time.sleep(1)
    if driver.current_url == 'https://qa.giam.finance/login':
        try:
            error = driver.find_element(By.CLASS_NAME, "error_message")
            print("%s seconds -" % (time.time() - start_time))
            print(('FAIL'))
        except:
            driver.quit()
            print("%s seconds -" % (time.time() - start_time))
            print(('Ok'))

            return True

# CORRECT
print(bool(test_correct_input('tyutyunnikalisha@gmail.com', 'Q123123qqq'))) #Ввод корректной почты и корректного пароля
print(bool(test_correct_input('alex567da', 'Q123123qqq'))) #Ввод корректного логина и корректного пароля

# INCORRECT
print(bool(test_incorrect_input('alex@outlook.com', 'Q123123qqq'))) #Ввод некорректного почты и корректного пароля
print(bool(test_incorrect_input('tyutyunnikalisha@gmail.com', 'q123123qqq')))# Ввод корректного почты и некорректного пароля
print(bool(test_incorrect_input('alex567da', '123123qqq')))# Ввод корректного логина и некорректного пароля
print(bool(test_incorrect_input('ale67da', 'Q123123qqq')))# Ввод некорректного логина и корректного пароля
print(bool(test_incorrect_input('leskdjf', '123123qqq')))# Ввод некорректного логина и некорректного пароля

# EMPTY
print(bool(test_empty_input('', 'Q123123qqq')))# Пустое поле логи
print(bool(test_empty_input('alex567da', '')))# Пустое поле пароль
print(bool(test_empty_input('', '')))# Оба поля пустые
print('END TESTS')

# parallel bot 1.1.0 using firefox instead of chrome
# v1.2.0 added login function and change the login if failed first
# v1.3.0 multi bot (it can run 48+ sessions)
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.chrome.service import Service
import time
import datetime
# import socket
import concurrent.futures

# third_aktet = socket.gethostbyname(socket.gethostname()).split('.')[2]
# url_server = f'http://198.18.96.{third_aktet}:3000/'
# url_server = 'http://10.10.20.31:3000/'
username1 = "operator1"
username2 = "operator2"


def logToFile(message: str, scriptName='multiSender.py'):
    date = datetime.datetime.now()
    dateStr = date.strftime('%Y-%m-%d')
    dateTimeStr = date.strftime('%Y-%m-%d_%H-%M-%S')
    with open(f'C:\Temp\LOGS_Debugger_Scripts_{dateStr}.log', 'a') as f:
        f.write(f'{dateTimeStr}: IN - {scriptName} LOGS: {message}\n')
    print(f'{dateTimeStr}: {message}\n')


def check_server(driver, url_server):
    flag = False
    while not flag:
        try:
            driver.get(url_server)
        except Exception:
            logToFile(f"Sender: Wow, something went wrong with your rocketchat server!!!Wait for 1 min... server: {url_server} ")
            time.sleep(60)
        else:
            flag = True


def login(driver, username, password):
    """Function to handle the login process."""
    username_elem = driver.find_element(By.NAME, 'username')
    username_elem.clear()
    username_elem.send_keys(username)

    password_elem = driver.find_element(By.NAME, "password")
    password_elem.clear()
    password_elem.send_keys(password)
    password_elem.send_keys(Keys.ENTER)

    # Wait for the page to load
    time.sleep(5)

    # Check for error message
    try:
        error_message = driver.find_element(By.CSS_SELECTOR, ".rcx-box.rcx-box--full.rcx-callout__children").text
        if "User not found or incorrect password" in error_message:
            return False
    except Exception:
        pass

    return True


def sender(url_server):
    """CREATE DRIVER"""
    options = webdriver.FirefoxOptions()
    options.add_argument("--mute-audio")
    driver = webdriver.Firefox(options=options)  # webdriver.Chrome(service=Service(PATH), options=options)
    check_server(driver, url_server)
    time.sleep(5)   # necessary pause!!
    """LOGIN"""
    if not login(driver, f"{username1}@rct.local", "Admin1Admin1"):
        login(driver, username1, "Admin1Admin1")
        time.sleep(5)  # necessary pause!!

    """SENDING"""
    channels = driver.find_elements(By.XPATH, "//a[contains(@href, '/channel/')]")
    for channel in channels:
        if '/general' in channel.get_property('href'):
            channel.click()
    time.sleep(5)
    while True:
        textarea_elem = driver.find_element(By.NAME, 'msg')
        textarea_elem.send_keys("Connection check, are you connected ?")
        textarea_elem.send_keys(Keys.ENTER)
        logToFile("Sent: <Connection check...> waiting for 1 min")
        time.sleep(60)


def answer(url_server):
    """CREATE DRIVER"""
    options = webdriver.FirefoxOptions()
    options.add_argument("--mute-audio")
    driver = webdriver.Firefox(options=options)  # webdriver.Chrome(service=Service(PATH), options=options)
    check_server(driver, url_server)
    time.sleep(5)  # necessary pause!!
    """LOGIN"""
    if not login(driver, f"{username2}@rct.local", "Admin1Admin1"):
        login(driver, username2, "Admin1Admin1")
        time.sleep(5)  # necessary pause!!
    """ANSWERING"""
    channels = driver.find_elements(By.XPATH, "//a[contains(@href, '/channel/')]")
    for channel in channels:
        if '/general' in channel.get_property('href'):
            channel.click()
    time.sleep(5)
    while True:
        message = driver.find_element(By.XPATH,
                                      "//div[contains(@class, 'rc-scrollbars-track')]//preceding::div[contains(@class, 'rcx-css-gln5p7')][1]")
        textarea_elem = driver.find_element(By.NAME, 'msg')
        if message.text == "Connection check, are you connected ?":
            textarea_elem.send_keys("Yes, I'm here")
            textarea_elem.send_keys(Keys.ENTER)
            logToFile("Sent: <Yes, I'm here>")


def mainDeploySender(octet, index):
    halfIp = '198.18.96.'
    if index == 1:
        url_server = f'http://{halfIp + str(octet)}:3000/'
        sender(url_server)
    elif index == 2:
        time.sleep(30)  # necessarily to wait until sender() will execute first message
        url_server = f'http://{halfIp + str(octet)}:3000/'
        answer(url_server)
    else:
        logToFile("wrong value operator")


def mainTestSender(octet, index):
    halfIp = '10.10.20.'
    if index == 1:
        url_server = f'http://{halfIp + str(octet)}:3000/'
        sender(url_server)
    elif index == 2:
        time.sleep(30)  # necessarily to wait until sender() will execute first message
        url_server = f'http://{halfIp + str(octet)}:3000/'
        answer(url_server)
    else:
        logToFile("wrong value operator")


def twiceSender(octet, isDeploy=True):
    listOfOctetsIndexed = [(octet, 1), (octet, 2)]
    if isDeploy:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            time.sleep(1)
            executor.map(lambda p: mainDeploySender(*p), listOfOctetsIndexed)
    else:
        with concurrent.futures.ThreadPoolExecutor() as executor:
            time.sleep(1)
            executor.map(lambda p: mainTestSender(*p), listOfOctetsIndexed)


def parallelMainSender(listOfOctets):  # TODO: remake for testing version multi sender

    with concurrent.futures.ThreadPoolExecutor() as executor:
        time.sleep(2)
        executor.map(twiceSender, listOfOctets)


# parallelMainSender([31])

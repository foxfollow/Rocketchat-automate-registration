# Auto registration for RC 1.0.0
# Parallel registration 1.1.0
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
# import socket
import concurrent.futures

# third_aktet = socket.gethostbyname(socket.gethostname()).split('.')[2]
# url_server = f'http://198.18.96.{third_aktet}:3000/'
# domainIP = f'10{third_aktet}....'  TODO: changeip
# url_server = f'http://10.10.20.{third_aktet}:3000/'
domainIP = '10.10.20.30'
domain = 'rct.local'
domainDN = 'DC=rct,DC=local'
domainUser = f'CN=Administrator,CN=Users,{domainDN}'
domainPassword = 'Admin1Admin1'
url_server_setup = 'setup-wizard/1'

myMail = "s.g.d3f0ld@gmail.com"


# myMail = "h.training.scpc@gmail.com"


def check_server(driver, url):
    flag = False
    while not flag:
        try:
            driver.get(url)
        except Exception:
            print(f"Wow, something went wrong with your rocketchat server!!!Wait for 1 min... for server {url} ")
            time.sleep(60)
        else:
            flag = True


def checkUrlAndNavigate(driver, url_server):
    while True:
        current_url = driver.current_url
        if 'setup' in current_url:
            print(f"In setup. Waiting for 30 seconds...(server: {url_server}")
            time.sleep(30)
        else:
            print(f"Not in setup. Going to settings for server {url_server}")
            driver.get(f'{url_server}admin/settings/Accounts')
            break


def doSendKeys(driver, byWhat, ID, keys):
    some_elem = driver.find_element(byWhat, ID)
    some_elem.clear()
    some_elem.send_keys(keys)
    return some_elem


def selectInSpan(driver, labelName, selectedName, isDiv=False):
    if isDiv:
        button = driver.find_element(By.XPATH, f'//div[@name="{labelName}"]')
    else:
        label = driver.find_element(By.XPATH, f'//label[text()="{labelName}"]')
        parent_div = label.find_element(By.XPATH, '..')  # get the parent div of the label

        button = parent_div.find_element(By.TAG_NAME, 'button')
    button.click()  # click the button

    div = driver.find_element(By.XPATH, f'//div[text()="{selectedName}"]')
    if isDiv:
        tmp = div.location_once_scrolled_into_view  # scroll to the div
        time.sleep(1)
    div.click()  # click the div


def checkBox(driver, rcxCss):
    div = driver.find_element(By.XPATH, f'//div[@class="rcx-box rcx-box--full rcx-css-{rcxCss}"]')
    checkbox = div.find_element(By.XPATH, './/i[@class="rcx-box rcx-box--full rcx-check-box__fake"]')
    checkbox.click()  # click the checkbox


def openBar(driver, title):
    div = driver.find_element(By.XPATH,
                              f"//div[contains(@class, 'rcx-box rcx-box--full rcx-box--animated rcx-accordion-item__bar') and .//h1[contains(text(), '{title}')]]")
    div.click()


def swipeButton(driver, label, text):
    label = driver.find_element(By.XPATH,
                                f"//label[@for='{label}' and contains(text(), '{text}')]")
    label.click()


def tmpLogin(driver, username, password):
    """Function to handle the login process."""
    username_elem = driver.find_element(By.ID, 'username')
    username_elem.clear()
    username_elem.send_keys(username)

    password_elem = driver.find_element(By.ID, "password")
    password_elem.clear()
    password_elem.send_keys(password)
    password_elem.send_keys(Keys.ENTER)

    # Wait for the page to load
    time.sleep(3)


def closeWindow(driver):
    try:
        time.sleep(1)
        # Find the button with the specified class
        button = driver.find_element(By.XPATH, "//button[contains(@class, 'rcx-box rcx-box--full rcx-button--small-square rcx-button--square rcx-button--icon rcx-button rcx-css-trljwa rcx-css-lma364')]")

        # Find the <i> element within the button and click it
        icon = button.find_element(By.XPATH, ".//i")
        icon.click()

    except:
        print("Button not found.")


def registration(driver, url_server):
    """Step 1, registration."""
    doSendKeys(driver, By.NAME, 'fullname', 'chat-admin')

    doSendKeys(driver, By.NAME, 'username', 'chat-admin')

    doSendKeys(driver, By.NAME, 'email', myMail)

    password_elem = doSendKeys(driver, By.NAME, 'password', 'P@ssw0rd')
    password_elem.send_keys(Keys.ENTER)
    # tmpLogin(driver, "chat-admin", "P@ssw0rd")
    # Wait for the page to load
    time.sleep(3)  # TODO: change to 5
    """Step 2, registration. Organization Info"""
    doSendKeys(driver, By.NAME, 'organizationName', 'test')

    # Assuming driver is initialized and navigated to the page
    selectInSpan(driver, "Organization industry", "Education")
    selectInSpan(driver, "Organization size", "1-10 people")
    selectInSpan(driver, "country", "Worldwide", isDiv=True)

    time.sleep(2)
    button = driver.find_element(By.XPATH, '//button[@type="submit" and text()="Next"]')
    button.click()  # click the button
    # Wait for the page to load
    time.sleep(3)   # TODO: change to 5
    """Step 3, registration. Enter cloud email"""
    doSendKeys(driver, By.NAME, 'email', myMail)

    checkBox(driver, "1twlfbd")
    checkBox(driver, "1o321ni")

    button = driver.find_element(By.XPATH, '//button[@type="submit" and text()="Register"]')
    button.click()  # click the button
    time.sleep(5)

    """Step 4, registration. Waiting email confirm"""
    checkUrlAndNavigate(driver, url_server)
    time.sleep(1)   # Before save

    print(f"waiting for letter accept for server {url_server}")


def settings(driver):
    time.sleep(1)
    closeWindow(driver)

    openBar(driver, 'Two Factor Authentication')

    swipeButton(driver,
                "Accounts_TwoFactorAuthentication_Enabled",
                "Enable Two Factor Authentication")

    time.sleep(1)
    button = driver.find_element(By.XPATH, '//button[@type="submit" and text()="Save changes"]')
    button.click()
    time.sleep(1)


def ldap(driver, url_server):
    driver.get(f'{url_server}admin/settings/LDAP')
    time.sleep(3)
    closeWindow(driver)
    time.sleep(1)
    swipeButton(driver, 'LDAP_Enable', 'Enable')
    time.sleep(1)
    doSendKeys(driver, By.ID, "LDAP_Host", domainIP)

    swipeButton(driver, "LDAP_Reconnect", "Reconnect")
    swipeButton(driver, "LDAP_Login_Fallback", "Login Fallback")

    openBar(driver, 'Authentication')
    swipeButton(driver, 'LDAP_Authentication', 'Enable')
    time.sleep(1)
    doSendKeys(driver, By.ID, 'LDAP_Authentication_UserDN', domainUser)
    time.sleep(1)
    doSendKeys(driver, By.ID, 'LDAP_Authentication_Password', domainPassword)
    time.sleep(1)

    """Changing tab to Users Search"""
    button = driver.find_element(By.XPATH, "//button[contains(text(), 'User Search')]")
    button.click()
    time.sleep(2)
    # swipeButton(driver, 'LDAP_Find_User_After_Login', 'Find')
    # time.sleep(1)
    openBar(driver, "Search Filter")
    time.sleep(1)
    doSendKeys(driver, By.ID, 'LDAP_BaseDN', domainDN)
    time.sleep(1)

    """Changing tab to Data Sync"""
    button = driver.find_element(By.XPATH, "//button[contains(text(), 'Data Sync')]")
    button.click()
    time.sleep(2)
    swipeButton(driver, 'LDAP_Merge_Existing_Users', "Merge")
    time.sleep(1)
    doSendKeys(driver, By.ID, 'LDAP_Default_Domain', domain)

    time.sleep(1)   # Before save
    button = driver.find_element(By.XPATH, '//button[@type="submit" and text()="Save changes"]')
    button.click()
    time.sleep(1)   # Before save


def main(third_aktet):
    url_server = f'http://10.10.20.{third_aktet}:3000/'     # TODO: change url
    """CREATE DRIVER"""
    options = webdriver.FirefoxOptions()
    options.add_argument("--mute-audio")
    driver = webdriver.Firefox(options=options)

    check_server(driver, url_server + url_server_setup)
    time.sleep(5)  # necessary pause!! TODO: Change to 5

    registration(driver, url_server)
    settings(driver)
    # tmpLogin(driver, "chat-admin", "P@ssw0rd") # only if server has already setuped first step
    ldap(driver, url_server)
    print(f"End script success for server {url_server}")


def parallelMain():
    # listOfIps = [31, 32, 33, 34, 35, 36, 37, 38, 39, 40]
    listOfIps = ["32", "33"]

    with concurrent.futures.ThreadPoolExecutor() as executor:

        executor.map(main, listOfIps)


print("hello")
parallelMain()
print("script ended")

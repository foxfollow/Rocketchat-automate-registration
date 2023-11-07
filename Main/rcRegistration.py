# Auto registration for RC 1.0.0
# Parallel registration 1.1.0
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import datetime
import concurrent.futures

# third_aktet = socket.gethostbyname(socket.gethostname()).split('.')[2]
# url_server = f'http://198.18.96.{third_aktet}:3000/'
# url_server = f'http://10.10.20.{third_aktet}:3000/'

domainDefault = 'rct.local'  # Do not change!
domainPassword = 'SCP.Admin1'
url_server_setup = 'setup-wizard/'


def logToFile(message: str, scriptName='rcRegistration.py'):
    date = datetime.datetime.now()
    dateStr = date.strftime('%Y-%m-%d')
    dateTimeStr = date.strftime('%Y-%m-%d_%H-%M-%S')
    with open(f'C:\Temp\LOGS_Debugger_Scripts_{dateStr}.log', 'a') as f:
        f.write(f'{dateTimeStr}: IN {scriptName} LOGS: {message}\n')
    logToFile(f'{dateTimeStr}: {message}\n')


def getValues(isDeploy, thirdOctet):
    strOctet = str(thirdOctet)
    if not isDeploy:
        variables = {
            'serverIP': f'10.10.20.{strOctet}',
            'domainIP': '10.10.20.30',
            'domainDN': 'DC=rct,DC=local',
            'domainUser': f'CN=Administrator,CN=Users,DC=rct,DC=local',
            'myMail': "s.g.d3f0ld@gmail.com"
        }
    else:
        if int(thirdOctet) < 10:
            zeroOctet = "0" + strOctet
        else:
            zeroOctet = strOctet
        variables = {
            'serverIP': f'198.18.96.{strOctet}',
            'domainIP': f'10.122.{strOctet}.113',
            'domainDN': f'DC=spectrum,DC={zeroOctet},DC=power,DC=cc23',
            'domainUser': f'CN=SCPAdmin,CN=Users,DC=spectrum,DC={zeroOctet},DC=power,DC=cc23',
            'myMail': "h.training.scpc@gmail.com"
        }
    return variables


def check_server(driver, url):
    flag = False
    maxTimeSec = 0
    # while not flag and maxTimeSec < 10800:    # if we want max time 3 hours
    while not flag:
        try:
            driver.get(url)
        except Exception:
            logToFile(f"Wow, something went wrong with your rocketchat server!!!Wait for 1 min... for server {url} ")
            time.sleep(60)
            maxTimeSec += 60
        else:
            flag = True


def checkUrlAndNavigate(driver, url_server):
    while True:
        current_url = driver.current_url
        if 'setup' in current_url:
            logToFile(f"In setup. Waiting for 30 seconds...(server: {url_server}")
            time.sleep(30)
        else:
            logToFile(f"Not in setup. Going to settings for server {url_server}")
            driver.get(f'{url_server}admin/settings/Accounts')
            break


def doSendKeys(driver, byWhat, ID, keys):
    time.sleep(0.5)
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
        div.location_once_scrolled_into_view
        time.sleep(1)
    div.click()  # click the div


def checkBox(driver, checkBoxName):
    # div = driver.find_element(By.XPATH, f'//div[@class="rcx-box rcx-box--full rcx-css-{rcxCss}"]')
    # div = driver.find_element(By.XPATH, f'//div[@name="{}"]')
    # label = driver.find_element(By.NAME, f"{checkBoxName}")
    # find the checkbox using its name
    # checkbox = driver.find_element(By.NAME, "agreement")
    #
    # # use JavaScript to click on the checkbox
    # driver.execute_script("arguments[0].click();", checkbox)
    checkbox = driver.find_element(By.NAME, checkBoxName)

    # create an ActionChains instance
    actions = ActionChains(driver)

    # move to the checkbox element, then move a bit to the right and down, and click
    actions.move_to_element(checkbox).move_by_offset(2, 2).click().perform()


def openBar(driver, title):
    div = driver.find_element(By.XPATH,
                              f"//div[contains(@class, 'rcx-box rcx-box--full rcx-box--animated rcx-accordion-item__bar') and .//h2[contains(text(), '{title}')]]")
    div.click()


def swipeButton(driver, label, text):
    label = driver.find_element(By.XPATH,
                                f"//label[@for='{label}' and contains(text(), '{text}')]")
    label.click()


def tmpLogin(driver, username, password):
    """Function to handle the login process."""
    username_elem = driver.find_element(By.NAME, 'username')
    username_elem.clear()
    username_elem.send_keys(username)

    password_elem = driver.find_element(By.NAME, "password")
    password_elem.clear()
    password_elem.send_keys(password)
    password_elem.send_keys(Keys.ENTER)

    # Wait for the page to load
    time.sleep(3)


def closeWindow(driver, recurse=False):
    try:
        time.sleep(5)
        # Find the button with the specified class
        button = driver.find_element(By.XPATH,
                                     "//button[contains(@class, 'rcx-box rcx-box--full rcx-button--small-square rcx-button--square rcx-button--icon rcx-button rcx-css-trljwa rcx-css-lma364')]")

        # Find the <i> element within the button and click it
        icon = button.find_element(By.XPATH, ".//i")
        icon.click()

    except:
        logToFile(f"Button not found. for {driver.current_url}")
        if not recurse:
            closeWindow(driver, recurse=True)


def registration(driver, url_server, isDeploy, thirdOctet):
    variables = getValues(isDeploy, thirdOctet)
    """Step 1, registration."""
    if driver.current_url == url_server + url_server_setup + "1":
        doSendKeys(driver, By.NAME, 'fullname', 'chat-admin')

        doSendKeys(driver, By.NAME, 'username', 'chat-admin')

        doSendKeys(driver, By.NAME, 'email', variables['myMail'])

        password_elem = doSendKeys(driver, By.NAME, 'password', 'P@ssw0rd')
        password_elem.send_keys(Keys.ENTER)
        # tmpLogin(driver, "chat-admin", "P@ssw0rd")
        # Wait for the page to load
        time.sleep(5)

    """Step 2, registration. Organization Info"""
    if driver.current_url == url_server + url_server_setup + "2":
        doSendKeys(driver, By.NAME, 'organizationName', 'test')

        # Assuming driver is initialized and navigated to the page
        selectInSpan(driver, "Organization industry", "Education")
        selectInSpan(driver, "Organization size", "1-10 people")
        selectInSpan(driver, "country", "Worldwide", isDiv=True)

        time.sleep(1)
        # button = driver.find_element(By.XPATH, '//button[@type="submit" and text()="Next"]')  # for RC v6.3.7
        button = driver.find_element(By.XPATH, "//button[normalize-space()='Next']")  # for RC v6.4.2
        button.click()
        # Wait for the page to load
        time.sleep(5)

    """Step 3, registration. Enter cloud email"""
    if driver.current_url == url_server + url_server_setup + "3":
        doSendKeys(driver, By.NAME, 'email', variables['myMail'])

        checkBox(driver, "updates")
        checkBox(driver, "agreement")
        time.sleep(2)
        # button = driver.find_element(By.XPATH, '//button[@type="submit"]')
        button = driver.find_element(By.XPATH, "//button[normalize-space()='Register']")  # for RC v6.4.2
        button.click()  # click the button
        time.sleep(5)

    """Step 4, registration. Waiting email confirm"""
    logToFile(f"Waiting for letter accept for server {url_server}")
    checkUrlAndNavigate(driver, url_server)
    time.sleep(1)  # Before save


def settings(driver):
    time.sleep(5)
    closeWindow(driver)

    openBar(driver, 'Two Factor Authentication')

    swipeButton(driver,
                "Accounts_TwoFactorAuthentication_Enabled",
                "Enable Two Factor Authentication")

    time.sleep(2)
    button = driver.find_element(By.XPATH, "//button[normalize-space()='Save changes']")  # for RC v6.4.2
    button.click()
    time.sleep(2)


def ldap(driver, url_server, isDeploy, thirdOctet):
    variables = getValues(isDeploy, thirdOctet)
    driver.get(f'{url_server}admin/settings/LDAP')
    time.sleep(3)
    closeWindow(driver)
    time.sleep(1)
    swipeButton(driver, 'LDAP_Enable', 'Enable')
    time.sleep(1)
    doSendKeys(driver, By.ID, "LDAP_Host", variables['domainIP'])

    swipeButton(driver, "LDAP_Reconnect", "Reconnect")
    swipeButton(driver, "LDAP_Login_Fallback", "Login Fallback")

    openBar(driver, 'Authentication')
    swipeButton(driver, 'LDAP_Authentication', 'Enable')
    time.sleep(1)
    doSendKeys(driver, By.ID, 'LDAP_Authentication_UserDN', variables['domainUser'])
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
    doSendKeys(driver, By.ID, 'LDAP_BaseDN', variables['domainDN'])
    time.sleep(1)

    """Changing tab to Data Sync"""
    button = driver.find_element(By.XPATH, "//button[contains(text(), 'Data Sync')]")
    button.click()
    time.sleep(2)
    swipeButton(driver, 'LDAP_Merge_Existing_Users', "Merge")
    time.sleep(1)
    doSendKeys(driver, By.ID, 'LDAP_Default_Domain', domainDefault)

    time.sleep(1)  # Before save
    button = driver.find_element(By.XPATH, "//button[normalize-space()='Save changes']")  # for RC v6.4.2
    button.click()
    time.sleep(1)  # Before save


def mainRegistration(thirdOctet, isDeploy=True):
    variables = getValues(isDeploy, thirdOctet)
    urlServer = f'http://{variables["serverIP"]}:3000/'
    """CREATE DRIVER"""
    options = webdriver.FirefoxOptions()
    options.add_argument("--mute-audio")
    driver = webdriver.Firefox(options=options)

    check_server(driver, urlServer + url_server_setup + "1")
    time.sleep(5)  # necessary pause!!

    # check if server is registered already
    if driver.current_url == urlServer + "home":
        tmpLogin(driver, "chat-admin", "P@ssw0rd")
        time.sleep(2)
        # closeWindow(driver)
        driver.get(urlServer + url_server_setup + '1')
        time.sleep(2)
        if driver.current_url == urlServer + "home":
            driver.close()
            logToFile(f"already registered on {urlServer}")
            return

    # run registration only if "setup-wizard" in url
    if url_server_setup in driver.current_url:
        registration(driver, urlServer, isDeploy, thirdOctet)
        # tmpLogin(driver, "chat-admin", "P@ssw0rd")  # only for test
        checkUrlAndNavigate(driver, urlServer)
        settings(driver)
        ldap(driver, urlServer, isDeploy, thirdOctet)
        logToFile(f"End script success for server {urlServer}")
    time.sleep(5)
    driver.close()
    logToFile(f"closed registration session on {urlServer}")


def parallelMainRegistration(listOfIps):
    if listOfIps is None:
        logToFile("Please provide list of IPs")
        return
    with concurrent.futures.ThreadPoolExecutor() as executor:
        time.sleep(2)
        executor.map(mainRegistration, listOfIps)

# parallelMainRegistration([33])

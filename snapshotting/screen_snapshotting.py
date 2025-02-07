from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from colorama import Fore, Style
import sys
sys.path.append('snapshotting')

def setup_driver(browser_name):
    if browser_name == "chrome":
        service = ChromeService(ChromeDriverManager().install())
        options = ChromeOptions()
        options.add_argument('--headless=new')
        driver = webdriver.Chrome(service=service, options=options)

    elif browser_name == "firefox":
        service = FirefoxService(GeckoDriverManager().install())
        options = FirefoxOptions()
        options.add_argument('-headless')
        driver = webdriver.Firefox(service=service, options=options)

    elif browser_name == "edge":
        service = EdgeService(EdgeChromiumDriverManager().install())
        options = EdgeOptions()
        options.add_argument('--headless=new')
        driver = webdriver.Edge(service=service, options=options)

    elif browser_name == "safari":
        options = webdriver.SafariOptions()
        driver = webdriver.Safari(options=options)

    elif browser_name == "opera":
        from config_processing import read_config
        config_values = read_config()
        service = ChromeService(ChromeDriverManager().install())
        options = ChromeOptions()
        options.add_argument('--headless=new')
        options.binary_location = config_values['opera_browser_path']
        driver = webdriver.Chrome(service=service, options=options)
    else:
        raise ValueError("Unsupported browser")
    driver.set_window_size(1920, 1080)
    return driver

def take_screenshot(browser_name, url, screenshot_path):
    try:
        print(Fore.GREEN + f"Starting {browser_name} browser in headless mode..." + Style.RESET_ALL)
        driver = setup_driver(browser_name)
        print(Fore.GREEN + f"Going to {url}" + Style.RESET_ALL)
        driver.get(url)
        print(Fore.GREEN + "Taking screenshot..." + Style.RESET_ALL)
        driver.save_screenshot(screenshot_path)
        driver.quit()
        print(Fore.GREEN + f"Screenshot successfully saved in report folder" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Error appeared: {str(e)}" + Style.RESET_ALL)
        if 'driver' in locals():
            driver.quit()

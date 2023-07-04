from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def main():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.google.com/search?q=my+current+location")
    element = driver.find_element(By.CLASS_NAME, "aiAXrc")
    text = element.text
    driver.quit()
    return print(text)
    
if __name__ == "__main__":
    main()


#___________pip install selenium
#___________python test10.py
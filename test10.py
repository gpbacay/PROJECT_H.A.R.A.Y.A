from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def main():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://www.google.com/search?q=my+current+location")
    element1 = driver.find_element(By.CLASS_NAME, "aiAXrc")
    element2 = driver.find_element(By.CLASS_NAME, "fMYBhe")
    text1 = element1.text
    text2 = element2.text
    driver.quit()
    return print(text1 + ", " + text2)
    
if __name__ == "__main__":
    main()


#___________pip install selenium
#___________python test10.py
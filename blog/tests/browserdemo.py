import time
from selenium import webdriver


driver = webdriver.Chrome('C:\\my-projects\\python\\learning-flask\\blog\\tests\\drivers\\chromedriver') # noqa
driver.get('http://localhost:5000/home')

print(driver.title)

time.sleep(20)
driver.quit()

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import openpyxl
import pandas as pd
#url

url = "https://gigate.com/search?options%5Bprefix%5D=none&options%5Bprefix%5D=last&pf_p_price=1000%3A3000&q=laptop&template=&type=product"

driver = webdriver.Chrome()
driver.get(url)

# making the dicts
laptop_names = []
laptop_prices = []

item_containers = driver.find_elements(By.CLASS_NAME ,  "boost-pfs-filter-product-bottom-inner")

page_num = 1
# main loop
while True:
    item_containers = driver.find_elements(By.CLASS_NAME, "boost-pfs-filter-product-bottom-inner")


    # for loop for item_containers
    for item_container in item_containers:

        item_name = item_container.find_element(By.CLASS_NAME , "boost-pfs-filter-product-item-title")
        print(item_name.text)

        # getting the text even if its on sale

        # if its not on sale
        try:
            item_price = item_container.find_element(By.CLASS_NAME , "boost-pfs-filter-product-item-regular-price")
            print(item_price.text)

            step1 = item_price.text.replace(",", "")
            item_price_str = step1.replace("SR", "")
            item_price_num = int(item_price_str)
            laptop_prices.append(item_price_num)
            laptop_names.append(item_name.text)
            print(item_price_num)

        # if its on sale

        except:
            item_price = item_container.find_element(By.CLASS_NAME , "boost-pfs-filter-product-item-sale-price")
            step1 = item_price.text.replace(",", "")
            item_price_str = step1.replace("SR", "")
            item_price_num = int(item_price_str)
            laptop_prices.append(item_price_num)
            laptop_names.append(item_name.text)

    try:
        next_btn = driver.find_element(By.XPATH, f"//li/a[text()='{page_num + 1}']")
        next_btn.click()
        page_num += 1
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "boost-pfs-filter-product-bottom-inner")))


    except:
        print("Pages finished")
        break

df = pd.DataFrame({
    'Laptop_name':laptop_names ,
    'Laptop_price':laptop_prices ,
})
df.to_excel('laptops_store.xlsx', index=False)

sleep(4)

driver.quit()



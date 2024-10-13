from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from PIL import Image
import requests
import time
import io

PATH = "/Users/bolang/Downloads/chromedriver_mac_arm64/chromedriver"
s = Service(PATH)
wd = webdriver.Chrome()


def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

    except Exception as e:
        print("failed: ", e)

    print("Success")


def get_images_from_google(driver, delay, max_images, url):
    def scroll_down(scroll_driver):
        scroll_driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    driver.get(url)

    image_urls = set()
    skips = 0

    while len(image_urls) + skips < max_images:
        scroll_down(driver)

        thumbnails = driver.find_elements(By.CLASS_NAME, "srp")

        for img in thumbnails[len(image_urls) + skips:max_images]:
            try:
                img.click()
                time.sleep(delay)
            except Exception as e:
                print(e)
                continue

            images = driver.find_elements(By.CLASS_NAME, "srp EIlDfe")
            for image in images:
                image_link = image.get_attribute("src")

                if image_link in image_urls:
                    max_images += 1
                    skips += 1
                    break

                if image_link and "http" in image_link:
                    image_urls.add(image_link)
                    print(f"Found {len(image_urls)}")

    return image_urls


URL = "https://www.google.com/search?sca_esv=82ce2834e599ed72&sxsrf=ADLYWIIaXHsES-ypjTT_ouIO1r9fZmzpHg:1728779837853&q=cats&udm=2&fbs=AEQNm0A-5VTqs5rweptgTqb6m-Eb3TvVcv4l7eCyod9RtZW9874wvsYjTfpwMQKGHqKPG-IB7j9flyfH28tJSLVuVdcT1tesPpIhTR_8sOQ3FQrQWiVTfWhoIplDgGh5JzUv9F4u3riMB636EHR41DrkNY_uSRk347tLZsVeJqqyuWPTyXrtg-EYkFQYZqw6rWM1khGHS26HrYFGhj2QeE1uCS-2MrLbBw&sa=X&ved=2ahUKEwjZ-IThjoqJAxVaLUQIHQbVMG8QtKgLegQIHhAB&biw=872&bih=765&dpr=1.1"
urls = get_images_from_google(wd, 2, 1, URL)


for i, img_url in enumerate(urls):
    download_image("/Users/bolang/Projects/Side-Bias/imgs/", img_url, str(i) + ".jpg")

wd.quit()

__author__ = 'valerio cosentino'

from selenium import webdriver
import hashlib
import loremipsum
import random
import time
from PIL import Image
import pytesseract
import radar

WEB_DRIVER_PATH = "./chromedriver.exe"
TARGET_URL = "http://resumize.me/"
MAIL = "https://www.mailinator.com/v2/inbox.jsp?zone=public&query="
driver = webdriver.Chrome(executable_path=WEB_DRIVER_PATH)
#pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files (x86)\\Tesseract-OCR\\tesseract'

TESTS = 100

def verify_email(email):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.get(MAIL + email)
    rest()

    found = [div for div in driver.find_elements_by_tag_name("div") if "resumize.me" in div.text.lower()]
    while not found:
        driver.refresh()
        rest()
        found = [div for div in driver.find_elements_by_tag_name("div") if "resumize.me" in div.text.lower()]

    found[0].click()
    rest()
    body = driver.find_element_by_id("msgpane")
    if body:
        driver.switch_to.frame(driver.find_element_by_id("msg_body"))
        content = driver.find_element_by_tag_name("html")
        link = content.text.split("http://")[1].strip()
        driver.get("http://" + link)
        rest()
        driver.close()
        ## try to automatically recognize the text in the image
        # print "ah-ah"
        # driver.get_screenshot_as_file('./mailinator.png')
        # img = Image.open('./mailinator.png')
        # text = pytesseract.image_to_string(img, lang="eng")

    driver.switch_to.window(driver.window_handles[0])


def register_new_account():
    rest()
    #find create account button
    found = [a for a in driver.find_elements_by_tag_name("a") if "create an account" in a.text.lower()]
    if found:
        found[0].click()
        #generate fake credentials
        name = loremipsum.generate_sentence()[2][:20].strip()
        email = hashlib.sha224(name).hexdigest()[:64] + "@mailinator.com"
        pwd = loremipsum.generate_sentence()[2][:10].strip()

        print "name: " + name + " -- email: " + email + " -- pwd: " + pwd

        #send them to the corresponding fields
        inputs = driver.find_elements_by_tag_name("input")
        inputs[0].send_keys(name)
        inputs[1].send_keys(email)
        inputs[2].send_keys(pwd)

        #register
        click_button("sign")
        verify_email(email)


def click_button(name, pos=0):
    found = [b for b in driver.find_elements_by_tag_name("button") if name in b.text.lower()]
    if found:
        found[pos].click()
        rest()


def rest():
    time.sleep(random.randint(3, 5))


def professional_area():
    form = driver.find_element_by_tag_name("form")
    areas = form.find_elements_by_tag_name("div")
    selection = areas[random.randint(0, len(areas)-1)]
    selection.click()
    click_button("save professional")


def personal_info():
    inputs = driver.find_elements_by_tag_name("input")
    job_title = loremipsum.generate_sentence()[2][:10].strip()
    headline = loremipsum.generate_sentence()[2][:15].strip()
    phone = "".join(([str(abs(ord(t) - 96)) for t in loremipsum.generate_sentence()[2][:10].strip()]))[:10]
    birth = radar.random_datetime(start='1912-01-01', stop='2017-07-07').strftime('%d/%m/%Y')
    description = loremipsum.generate_paragraph()[2][:100].strip()

    inputs[1].send_keys(job_title)
    inputs[2].send_keys(headline)
    inputs[4].send_keys(phone)
    inputs[5].send_keys(birth)
    driver.find_element_by_tag_name("textarea").send_keys(description)

    click_button("next")


def languages():
    click_button("new language")

    rest()
    forms = [f for f in driver.find_elements_by_class_name("form-group") if "spoken" in f.text.lower() or "written" in f.text.lower() or "reading" in f.text.lower()]
    for f in forms:
        selected = f.find_elements_by_tag_name("div")[random.randint(0, 4)]
        selected.click()

    lang = ["Latin", "Italian", "English", "Spanish"]
    input = driver.find_elements_by_tag_name("input")[0]
    input.send_keys(lang[random.randint(0, len(lang)-1)])
    click_button("next")


def education():
    click_button("new education")

    inputs = [i for i in driver.find_elements_by_tag_name("input")]

    institute = loremipsum.generate_sentence()[2][:15].strip()
    course = loremipsum.generate_sentence()[2][:15].strip()
    description = loremipsum.generate_paragraph()[2][:100].strip()
    period = radar.random_datetime(start='1912-01-01', stop='2012-07-07').strftime('%d/%m/%Y')
    to = radar.random_datetime(start='2012-07-08', stop='2017-07-07').strftime('%d/%m/%Y')

    inputs[0].send_keys(institute)
    inputs[1].send_keys(course)
    driver.find_element_by_tag_name("textarea").send_keys(description)
    inputs[2].send_keys(period)
    inputs[4].send_keys(to)

    click_button("next")


def certification():
    click_button("new certification")
    inputs = [i for i in driver.find_elements_by_tag_name("input")]

    title = loremipsum.generate_sentence()[2][:15].strip()
    authority = loremipsum.generate_sentence()[2][:15].strip()
    issued = radar.random_datetime(start='1980-07-08', stop='2017-07-07').strftime('%d/%m/%Y')

    inputs[0].send_keys(title)
    inputs[1].send_keys(authority)
    inputs[2].send_keys(issued)

    for i in range(random.randint(1, 5)):
        rest()
        click_button("add a new", -1)
        rest()
        container = driver.find_elements_by_class_name("fields-container")[-1]
        inputs = [i for i in container.find_elements_by_tag_name("input")]

        title = loremipsum.generate_sentence()[2][:15].strip()
        authority = loremipsum.generate_sentence()[2][:15].strip()
        issued = radar.random_datetime(start='1980-07-08', stop='2017-07-07').strftime('%d/%m/%Y')

        inputs[0].send_keys(title)
        inputs[1].send_keys(authority)
        inputs[2].send_keys(issued)

    click_button("next")


def professional_experience():
    click_button("next")


def color_schema():
    options = driver.find_elements_by_class_name("color-scheme-name")
    options[random.randint(0, len(options)-1)].click()
    click_button("download")


def filling_data():
    rest()
    professional_area()
    rest()
    personal_info()
    rest()
    languages()
    rest()
    education()
    rest()
    certification()
    rest()
    professional_experience()
    rest()
    color_schema()


def main():
    driver.maximize_window()

    for i in range(0, TESTS):
        driver.get(TARGET_URL)
        register_new_account()
        filling_data()

    driver.close()

if __name__ == "__main__":
    main()

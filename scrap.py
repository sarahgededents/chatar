from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import datetime
import re

#opts = FirefoxOptions()
#opts.add_argument("--headless")
driver = webdriver.Firefox()#options=opts)
driver.get("https://www.pmu.fr/turf/11092021/r1/c3/")  # TODO : change url to automatically get the quinte of the day

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.WelcomeStep__DiscardButton-sc-18c5grd-0'))).click()  # popup cookies

driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div[2]/div[2]/div/div[1]/div/div/div[2]/a').click()  # course quinté

nombre_chevaux = int(re.search('(\d+) partants', driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div[1]/div/div/div/div[2]/div/div[4]/div').text).group(1))

'''
npartant = []
for c in range(nombre_chevaux):
    print(driver.find_element_by_xpath(f'/html/body/div[1]/div[3]/div/div[1]/div/div/div/div[4]/div[2]/div[3]/div[{c+1}]/div/div[2]/div/div[2]/div/div[3]').text)
    if driver.find_element_by_xpath(f'/html/body/div[1]/div[3]/div/div[1]/div/div/div/div[4]/div[2]/div[3]/div[{c+1}]/div/div[2]/div/div[2]/div/div[3]').text:
        npartant.append(c+1)
# pas les memes Xpath si c'est des NP
/html/body/div[1]/div[3]/div/div[1]/div/div/div/div[4]/div[2]/div[3]/div[2]/div/div[2]/div/div[2]/div/div[3]/div
/html/body/div[1]/div[3]/div/div[1]/div/div/div/div[4]/div[2]/div[3]/div[14]/div/div[2]/div/div[2]/div/div[3]/div
/html/body/div[1]/div[3]/div/div[1]/div/div/div/div[4]/div[2]/div[3]/div[15]/div[1]/div[2]/div/div[2]/div/div
/html/body/div[1]/div[3]/div/div[1]/div/div/div/div[4]/div[2]/div[3]/div[15]
'''

infos_cheval = {}
for cheval in range(nombre_chevaux):
    if cheval == 0:
        driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div[1]/div/div/div/div[4]/div[2]/div[3]/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/a').click()  # cheval 1
    else:
        driver.find_element_by_xpath(f'/html/body/div[1]/div[3]/div/div[1]/div/div/div[1]/div/div[2]/div/div/div/div/div[{cheval+1}]').click()
    total = int(WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[3]/div/div[1]/div/div/div[1]/div/div[2]/div/main/div/div/div[1]/div[1]/div/div[1]/div/div[1]"))).text)
    first = int(WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[3]/div/div[1]/div/div/div[1]/div/div[2]/div/main/div/div/div[1]/div[1]/div/div[1]/ul/li[1]/div[1]"))).text)  # 1st
    sec_third = int(WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[3]/div/div[1]/div/div/div[1]/div/div[2]/div/main/div/div/div[1]/div[1]/div/div[1]/ul/li[2]/div[1]"))).text)  # 2nd and 3rd
    course_score = {}
    for c in range(3):
        try:
            jour_course = driver.find_element_by_xpath(f'/html/body/div[1]/div[3]/div/div[1]/div/div/div[1]/div/div[2]/div/main/div/div/div[2]/div[{c+1}]/div[1]/div/ul/li[1]/div[1]').text
            year_course = driver.find_element_by_xpath(f'/html/body/div[1]/div[3]/div/div[1]/div/div/div[1]/div/div[2]/div/main/div/div/div[2]/div[{c+1}]/div[1]/div/ul/li[1]/div[2]').text
            date_course = datetime.datetime.strptime(f'{jour_course} {year_course}', "%d %b %Y").date()
            score_course = re.search('(\d+)', driver.find_element_by_xpath(f'/html/body/div[1]/div[3]/div/div[1]/div/div/div[1]/div/div[2]/div/main/div/div/div[2]/div[{c+1}]/div[1]/div/ul/li[3]/div').text)
            if score_course:
                score_course = int(score_course.group(1))
            else:
                score_course = 0

            npartants = int(re.search('(\d+) partants', driver.find_element_by_xpath(f'/html/body/div[1]/div[3]/div/div[1]/div/div/div[1]/div/div[2]/div/main/div/div/div[2]/div[{c+1}]/div[1]/div/ul/li[2]/div[3]/span[3]').text).group(1))

            course_score[f'course{c+1}'] = { 'date': date_course, 'arrivee': score_course, 'partants': npartants }
        except:
            break
    infos_cheval[cheval+1] = { 'total': total, 'nwin': first, 'npodium': sec_third, 'past_run': course_score }
#print(infos_cheval)
driver.close()

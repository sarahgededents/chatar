from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import datetime
import re

print('Gathering PMU info\n---------------------------------------------')

date = input("Please enter a date: (format ddmmyyyy) ")


def check_date(d):
    pattern = re.compile("^[0-3][0-9][0-1][0-9][0-9][0-9][0-9][0-9]$")
    if not d:
        return d
    while not pattern.match(d):
        d = input("Please enter a date: (format ddmmyyyy) ")
    return f'{d}/'


date = check_date(date)

delay = 5
opts = FirefoxOptions()
opts.add_argument("--headless")
browser = webdriver.Firefox(options=opts)
print(f"https://www.pmu.fr/turf/{date}")
browser.get(f"https://www.pmu.fr/turf/{date}")  # get runs of the day

WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.WelcomeStep__DiscardButton-sc-18c5grd-0'))).click()  # popup cookies
for i in range(3):
    browser.find_element_by_xpath('/html/body/div[1]/div[4]/div/div[1]/button').click()  # skip tutorial

browser.find_element_by_xpath('/html/body/div[1]/div[4]/div/div[2]/div/div[1]/div/div/div[2]/a').click()  # quinté of the day

p = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div/div[1]/div/div/div/div[2]/div/div[4]/div'))).text  # get number of starters
nhorses = int(re.search('(\d+) partants', p).group(1))

nstart = []
for c in range(nhorses):
    try:
        NP = browser.find_element_by_xpath(f'/html/body/div[1]/div[3]/div/div[1]/div/div/div/div[4]/div[2]/div[3]/div[{c+2}]/div/div[2]/div/div[2]/div/div[3]').text  # if xpath correct, then, this horse will start
    except:
        nstart.append(c+1)

horse_info = {}
for horse in range(nhorses):
    if horse == 0:
        browser.find_element_by_xpath('/html/body/div[1]/div[3]/div/div[1]/div/div/div/div[4]/div[2]/div[3]/div[2]/div/div[2]/div/div[1]/div[1]/div/div[1]/a').click()  # horse 1
    else:
        browser.find_element_by_xpath(f'/html/body/div[1]/div[3]/div/div[1]/div/div/div[1]/div/div[2]/div/div/div/div/div[{horse+1}]').click()  # other horses
    nruns = int(WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[3]/div/div[1]/div/div/div[1]/div/div[2]/div/main/div/div/div[1]/div[1]/div/div[1]/div/div[1]"))).text)
    first = int(WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[3]/div/div[1]/div/div/div[1]/div/div[2]/div/main/div/div/div[1]/div[1]/div/div[1]/ul/li[1]/div[1]"))).text)  # 1st
    sec_third = int(WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[3]/div/div[1]/div/div/div[1]/div/div[2]/div/main/div/div/div[1]/div[1]/div/div[1]/ul/li[2]/div[1]"))).text)  # 2nd and 3rd
    run_info = {}
    for c in range(3):
        try:
            run_dm = browser.find_element_by_xpath(f'/html/body/div[1]/div[3]/div/div[1]/div/div/div[1]/div/div[2]/div/main/div/div/div[2]/div[{c+1}]/div[1]/div/ul/li[1]/div[1]').text
            run_year = browser.find_element_by_xpath(f'/html/body/div[1]/div[3]/div/div[1]/div/div/div[1]/div/div[2]/div/main/div/div/div[2]/div[{c+1}]/div[1]/div/ul/li[1]/div[2]').text
            run_date = datetime.datetime.strptime(f'{run_dm} {run_year}', "%d %b %Y").date()
            score_run = re.search('(\d+)', browser.find_element_by_xpath(f'/html/body/div[1]/div[3]/div/div[1]/div/div/div[1]/div/div[2]/div/main/div/div/div[2]/div[{c+1}]/div[1]/div/ul/li[3]/div').text)
            if score_run:
                score_run = int(score_run.group(1))
            else:
                score_run = 0

            nstarters = int(re.search('(\d+) partants', browser.find_element_by_xpath(f'/html/body/div[1]/div[3]/div/div[1]/div/div/div[1]/div/div[2]/div/main/div/div/div[2]/div[{c+1}]/div[1]/div/ul/li[2]/div[3]/span[3]').text).group(1))  # get number of starters

            run_info[f'r{c+1}'] = { 'date': run_date, 'rank': score_run, 'n_starters': nstarters }
        except:
            break
    horse_info[horse+1] = { 'n_runs': nruns, 'n_victory': first, 'n_podium': sec_third, 'past_runs': run_info }

    print(f'horse number {horse+1}: {horse_info[horse+1]}')

browser.close()

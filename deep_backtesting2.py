# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 11:07:47 2022
@author: 52811
"""
#Load all required dependencies
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
import numpy as np

# Open ChromeDriver and navigate to page
driver = webdriver.Chrome()
url = "https://www.tradingview.com/#signin"
driver.maximize_window()
driver.get(url)

# Create the DataFrame where the best settings for each pair will be appended
results_df = pd.DataFrame(columns=['Symbol', 'R:R', 'SL %', 'Equal H/L', 'Net Profit', 'Max Drawdown', 'Avg Trade', 'Total Closed Trades', 'Percent Profitable', 'Profit Factor'])
results_df = results_df.set_index('Symbol')

# If looking for best settings for multiple pairs run the following line and input the numer of pairs
list_size = int(input("Enter number of pairs"))

#List the range of settings for each parameter for which the script will loop
e = np.arange(0.2, 0.6, 0.1) #Set First parameter range and step
e = np.round(e, 2).tolist()
sl = np.arange(0.25, 2.25, 0.25) #Set Second Parameter range and step size
sl = np.round(sl, 2).tolist()
sl.insert(0, 0.15)
r = np.arange(2, 7.5, 0.5) #Set Third Parameter range and step size
r = np.round(r, 2).tolist()

#Create an array with all the combinations of paramter's settings
parameters = [[i, j, k] for i in e for j in r for k in sl] 
driver.find_element("xpath", "//*[text()='Deep Backtesting']/parent::div/span/input").click()
for k in range(1, list_size, 1):
    #Set Dates Range to backtest for (First Available day to Today)
    pair = driver.find_element("xpath", '//button[@id="header-toolbar-symbol-search"]/div').text #Get the symbol name
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Generate report']/parent::button/parent::div/div/div[1]"))).click() #Set first date
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Select the first available day']/parent::button"))).click() #select first available day
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Generate report']/parent::button/parent::div/div/div[3]"))).click()#Set second date
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Select today']/parent::button"))).click() #Select today
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Generate report']/parent::button"))).click() #Click Generate Report
    WebDriverWait(driver, 60).until(EC.text_to_be_present_in_element((By.XPATH, "//div[text()='Net Profit']"), "Net Profit")) #Wait for Net Profits stats to show up
    
    #Set first parameter combination before starting loop
    driver.find_element("xpath", "(//*[text()='Equal High/Low Strategy 3'])[2]/parent::div/div[2]/button").click() #Get into strategy Settings
    WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "(//div[text()='R:R']/parent::div/following-sibling::div/div/span/span/input)[1]"))) #Wait for strategy settings to show up
    driver.find_element("xpath", "(//div[text()='Equal H/L distance %']/parent::div/following-sibling::div/div/span/span/input)[1]").click() #Go to first parameter
    webdriver.ActionChains(driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(f"{parameters[0][0]}").send_keys(Keys.ENTER).perform() #Set first Parameter
    driver.find_element("xpath", "(//div[text()='R:R']/parent::div/following-sibling::div/div/span/span/input)[1]").click() #Go to second parameter
    webdriver.ActionChains(driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(f"{parameters[0][1]}").send_keys(Keys.ENTER).perform() #Set second parameter
    driver.find_element("xpath", "(//div[text()='SL']/parent::div/following-sibling::div/div/span/span/input)[1]").click() #Go to third parameter
    webdriver.ActionChains(driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(f"{parameters[0][2]}").send_keys(Keys.ENTER).perform() #Set third parameter
    webdriver.ActionChains(driver).key_down(Keys.ESCAPE).perform()#Exit strategy settings
    webdriver.ActionChains(driver).key_down(Keys.ESCAPE).perform()#Exit strategy settings
    WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Generate report']"))).click() #Get new stats for the specified parameters
    WebDriverWait(driver, 60).until(EC.text_to_be_present_in_element((By.XPATH, "//*[text()='Net Profit']"), "Net Profit"))# Wait for stats to show up

    # Create arrays for each of the DataFrame's Columns
    E = []
    R = []
    sl_percent = []
    profit = []
    dd = []
    symbols = []
    avg_trade = []
    number_of_trades = []
    win_rate = []
    pf = []
    e_param = parameters[0][0]
    r_param = parameters[0][1]
    sl_param = parameters[0][2]

    p_text = driver.find_element("xpath", "//*[text()='Net Profit']/parent::div/parent::div/div[2]/div[2]").text
    dd_text = driver.find_element("xpath", "//*[text()='Max Drawdown']/parent::div/parent::div/div[2]/div[2]").text
    avg_text = driver.find_element("xpath", "//*[text()='Avg Trade']/parent::div/parent::div/div[2]/div[2]").text

    wait = WebDriverWait(driver, 5, 0.5, ignored_exceptions=[StaleElementReferenceException])
    
    #Loop through each combination, get stats and append each stat to its corresponding array
    for i in range(1, len(parameters) + 1):
        driver.find_element("xpath", "(//*[text()='Equal High/Low Strategy 3'])[2]/parent::div/div[2]/button").click()
        if parameters[i][0] != e_param:
            driver.find_element("xpath", "(//div[text()='Equal H/L distance %']/parent::div/following-sibling::div/div/span/span/input)[1]").click()
            webdriver.ActionChains(driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(f"{parameters[i][0]}").send_keys(Keys.ENTER).perform()
        if parameters[i][1] != r_param:
            driver.find_element("xpath", "(//div[text()='R:R']/parent::div/following-sibling::div/div/span/span/input)[1]").click()
            webdriver.ActionChains(driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(f"{parameters[i][1]}").send_keys(Keys.ENTER).perform()
        if parameters[i][2] != sl_param:
            driver.find_element("xpath", "(//div[text()='SL']/parent::div/following-sibling::div/div/span/span/input)[1]").click()
            webdriver.ActionChains(driver).key_down(Keys.CONTROL).send_keys("a").key_up(Keys.CONTROL).send_keys(f"{parameters[i][2]}").send_keys(Keys.ENTER).perform()
        webdriver.ActionChains(driver).key_down(Keys.ESCAPE).perform()
        webdriver.ActionChains(driver).key_down(Keys.ESCAPE).perform()
        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Generate report']/parent::button"))).click()
        WebDriverWait(driver, 60).until(EC.text_to_be_present_in_element((By.XPATH, "//*[text()='Net Profit']"), "Net Profit"))

        profit.append(wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()='Net Profit']/parent::div/parent::div/div[2]/div[2]"))).text) #Append Net Profit

        dd.append(wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()='Max Drawdown']/parent::div/parent::div/div[2]/div[2]"))).text) #Append Max Drawdown

        avg_trade.append(wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()='Avg Trade']/parent::div/parent::div/div[2]/div[2]"))).text)#Append Average per Trade

        number_of_trades.append(wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()='Total Closed Trades']/parent::div/parent::div/div[2]/div[1]"))).text) #Append Total Trades

        win_rate.append(wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()='Percent Profitable']/parent::div/parent::div/div[2]/div[1]"))).text) #Append Win rate percent

        pf.append(wait.until(EC.visibility_of_element_located((By.XPATH, "//*[text()='Profit Factor']/parent::div/parent::div/div[2]/div[1]"))).text) #Append Profit Factor

        E.append(f"{parameters[i][0]}") #Append first parameter setting
        R.append(f"{parameters[i][1]}") #Append second parameter setting
        symbols.append(pair) #Append symbol name
        sl_percent.append(f"{parameters[i][2]}") #Append third parameter setting
        e_param = parameters[i][0]
        r_param = parameters[i][1]
        sl_param = parameters[i][2]

    #Prepare and clean data of all the stats for all the settings
    scenarios = []
    profit = [i.split("%")[0] for i in profit]
    profit = [i.replace('−', '-') for i in profit]
    profit = [i.replace(" ", "") for i in profit]
    dd = [i.split("%")[0] for i in dd]
    dd = [i.replace('−', '-') for i in dd]
    avg_trade = [i.split("%")[0] for i in avg_trade]
    avg_trade = [i.replace('−', '-') for i in avg_trade]
    win_rate = [i.split("%")[0] for i in win_rate]
    for e, r, s, p, d, sy, a, n, w, x in zip(E, R, sl_percent, profit, dd, symbols, avg_trade, number_of_trades, win_rate, pf):
        scenario = {'Symbol': sy, 'R:R': r, 'SL %': s, 'Equal H/L': e, 'Net Profit': p, 'Max Drawdown': d, 'Avg Trade': a, 'Total Closed Trades': n, 'Percent Profitable': w, 'Profit Factor': x}
        scenarios.append(scenario)
    #Create DataFrame
    df = pd.DataFrame(scenarios)
    
    #Specify each column name
    df['Net Profit'] = df['Net Profit'].astype(float)
    df['Max Drawdown'] = df['Max Drawdown'].astype(float)
    df['Avg Trade'] = df['Avg Trade'].astype(float)
    df['Total Closed Trades'] = df['Total Closed Trades'].astype(float)
    df['Percent Profitable'] = df['Percent Profitable'].astype(float) * .01
    df['Profit Factor'] = df['Profit Factor'].astype(float)
    df['R:R'] = df['R:R'].astype(float)
    #Create Expectancy column
    df['Expectancy'] = (df['R:R'] * .5 * df['Percent Profitable']) - (0.5 * (1 - df['Percent Profitable']))
    # df= df[df['Max Drawdown']<10]
    # df= df[df['Percent Profitable']>.35]
    
    #Sort by Expactancy Descending
    df = df.sort_values(by=['Expectancy'], ascending=False)
    
    #Get the Settings with the Highest Expectancy
    df = df.reset_index(drop=True)
    df = df.iloc[:1]
    df = df.set_index('Symbol')
    
    #Append these settings to the results Dataframe
    results_df = pd.concat([results_df,df], ignore_index=False)
    time.sleep(2)
    
    #Go to next symbol
    driver.find_element(By.CSS_SELECTOR,'body').send_keys(Keys.DOWN)
    WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "(//canvas)[1]"))).get_attribute("width")
    try:
        wait.until_not(EC.text_to_be_present_in_element((By.XPATH, "//*[@class='reports-content']//em[text()='Net Profit']/parent::div/p/span"), f"{p_text}"))
    except:
        time.sleep(1)
    print(f"Scanning done on {pair}, moving on to the next")
    time.sleep(1)

#Save settings to an Excel Spreashsheet

df.to_excel('btc_deep2.xlsx')

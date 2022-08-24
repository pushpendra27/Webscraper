import os
import pandas as pd
import pandas as pd
import matplotlib.pyplot as plt
import sys
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.firefox import GeckoDriverManager
import shutil
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile


if __name__ == '__main__':

    browser_name = "chrome"

    if browser_name == "chrome":

        user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
        """opt = Options()
          opt.add_argument("--headless")
          options.headless = True
          driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=opt)
          driver=webdriver.Chrome()"""

        options = webdriver.ChromeOptions()
        #options.add_argument('--headless')
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-gpu")
        #options.add_argument('--user-data-dir=</home/pushpendra/.config/google-chrome/default>')
        options.add_argument('--profile-directory=Default')
        #driver = webdriver.Chrome(chrome_options=options)
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        # `      user_agent=driver.execute_script("return navigator.userAgent;")
        driver.implicitly_wait(5)
    elif browser_name == "firefox":

        options = webdriver.FirefoxOptions()
        # options.headless = True

        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
        currentProfilePath = driver.capabilities["moz:profile"]
        print("CurrentProfilePath:", currentProfilePath)
        profileStoragePath = "/tmp/abc"

        shutil.copytree(currentProfilePath, profileStoragePath, ignore_dangling_symlinks=True)
        driver = webdriver(executable_path="/home/pushpendra/.wdm/drivers/geckodriver/linux64/v0.29.1",
                           firefox_profile=FirefoxProfile(profileStoragePath))

    else:
        print("_____Please Enter Correct Browser Name Before Move Further____" + browser_name)
  
    # Register the drive
    driver.get('https://opentender.eu/start')
    print(driver.title)
    time.sleep(10)
    txt=driver.find_elements_by_xpath('//div[@class="container-left-6"]/ul/li/a')
    #print(txt)
    txt1=driver.find_elements_by_xpath('//div[@class="container-left-6"]/ul/li/div')
    #print(txt1)

    present_tenders=[]

    length=len(driver.find_elements_by_xpath('//div[@class="container-left-6"]/ul/li'))
    print("Content Length",length)


    for i in range(length):
        temporary_data={'Country_Name':txt[i].text,
                        'Tender_Count':txt1[i].text}
        
        present_tenders.append(temporary_data)
    #print(present_tenders)

    
    #Using Pandas for storing data
    df_data=pd.DataFrame(present_tenders)
    print(df_data)

    #Storing Data in CSV format
    df_data.to_csv('all_the_present_tenders.csv',index=False)
    print("CSV File Created")


    # reading the database
    data = pd.read_csv("all_the_present_tenders.csv")
 
    # Bar chart with day against tip
    plt.bar(data['Country_Name'], data['Tender_Count'])
 
    plt.title("Bar Chart")
         
    # Setting the X and Y labels
    plt.xlabel('Country')
    plt.ylabel('Tender')
 
    # Adding the legends
    plt.show()

    
    
    driver.close()
    driver.quit()

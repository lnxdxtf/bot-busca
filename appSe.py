from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from os import path
import json

#local binario universal
main_folder = path.join(path.expanduser("~"), r"AppData\Local\Mozilla Firefox\firefox.exe")
options = Options()
#local binario local
#r"C:\Users\gabri\AppData\Local\Mozilla Firefox\firefox.exe"
options.binary_location = main_folder
#declarar o driver



class appBot():
    def __init__(self):
        self.driver = webdriver.Firefox(options=options,executable_path=r"geckodriver.exe")

    def buscar(self):
        driver = self.driver
        driver.get("https://webscraper.io/test-sites/e-commerce/allinone/product/545")
        computer_Li = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]/div/div/ul/li[2]/a")
        computer_Li.click()
        laptop_Li = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]/div/div/ul/li[2]/ul/li[1]/a")
        laptop_Li.click()
        print("Pegandos os produtos, aguarde")
        return self.getLinks()
    
    def getLinks(self):
        driver = self.driver
        descriptions = driver.find_elements_by_xpath("//div[@class='caption']")
        allLinks = {}
        prod = 0
        for description in descriptions:
            title = description.find_element_by_tag_name("a").text
            if (title.startswith("Lenovo")):
                #allLinks[description.text]= 'Product'
                prod=prod+1
                allLinks[f"{description.text}"] = ("Product"+str(prod))
                ##print(description.text,"\n\n")
        
        #print(allLinks)
        
         
        allLinks = json.dumps(allLinks,
                              indent=4)

        responseJson = json.loads(allLinks)
        print(type(responseJson))
        print('\n\n', responseJson)
        return responseJson
        
        

 

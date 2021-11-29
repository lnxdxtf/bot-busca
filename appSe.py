from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from os import path
import json
import time

from starlette import responses

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
        #acessar a página inicial
        self.driver.get("https://webscraper.io/test-sites/e-commerce/allinone/product/545")
        #encontrar e acessar os caminhos para os laptops/notebooks
        computer_Li = self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]/div/div/ul/li[2]/a")
        computer_Li.click()
        laptop_Li = self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]/div/div/ul/li[2]/ul/li[1]/a")
        laptop_Li.click()
        #chamar a função getLinks
        print("Pegandos os produtos, aguarde")
        return self.getLinks()
    
    def getLinks(self):
        #encontrar todos os elementos com a classe caption - porque essa é a classe das divs dos produtos mostrados lado a lado 
        productsContainers = self.driver.find_elements_by_xpath("//div[@class='caption']")
        allLinks = {} # dicionario  vazio para colocar os produtos com id, descriçao e valor (hd inicial/basico)
        productId = 0 #numerador do ID
        for productContainer in productsContainers: 
            title = productContainer.find_element_by_tag_name("a").get_attribute("title") #encontrar o title (nome do produto com que faz ref. para a sua página do produto)
            description = productContainer.find_element_by_class_name("description").text # encontrar a classe description e pegar o que está dentro(no caso a descrição do produto)
            if (title.startswith("Lenovo") and description.startswith("Lenovo")): #condição para verificar se o titulo do produto faz referencia a sua descrição
                price = productContainer.find_element_by_class_name("price").text #encontrar o preço do produto (classe)
                #allLinks[description.text]= 'Product'
                productId=productId+1 #incremento do id
                allLinks[f"Produto {title}"] = { #adicionando o produto ao dicionario com a chave 'produto' e valores _id, descrição e valor
                                                "_id":productId, 
                                                "descricao":description,
                                                "valor":price
                                                }
                ##print(description.text,"\n\n")
        #print(allLinks)
        #processo para transoformar o dicionário em json
        allLinks = json.dumps(allLinks,
                              indent=4)
        responseJson = json.loads(allLinks)
        #print(type(responseJson))
        #print('\n\n', responseJson)
        self.driver.quit()
        return responseJson
        
    def getPages(self, marca):
        marca = marca.title() #pegar o parametro de rota (marca do produto) e .title() para formatar a str pra começar com letra maiúscula
        #mesmo processo da função buscar()
        self.driver.get("https://webscraper.io/test-sites/e-commerce/allinone/product/545") 
        computer_Li = self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]/div/div/ul/li[2]/a")
        computer_Li.click()
        laptop_Li = self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]/div/div/ul/li[2]/ul/li[1]/a")
        laptop_Li.click()
        print("Pegando os links dos produtos")
        productsLinks = [] # lista para add os links de todos os produtos da marca
        #encontrar todos os elementos com a classe caption - porque essa é a classe das divs dos produtos mostrados lado a lado 
        productsContainers = self.driver.find_elements_by_xpath("//div[@class='caption']") 
        for productLink in productsContainers:
            link = productLink.find_element_by_tag_name("a").get_attribute("href") #buscar tag 'a' e pegar o que contém no atributo 'href'
            title = productLink.find_element_by_tag_name("a").get_attribute("title") #buscar tag 'a' e pegar o que contérm no atributo 'title'
            description = productLink.find_element_by_class_name("description").text # buscar a classe description e pegar o que contém dentro
            if (title.startswith(marca) and description.startswith(marca)): #verificar se a marca e a description fazem a mesma referencia do produto
                productsLinks.append(link) # add o link na lista de links
        # productsLinks = json.dumps(productsLinks)        
        # responseJson = json.loads(productsLinks)
        
        products = {} #dicionario vazio para add os produtos 
        productsId = 0 #numerador de id
        
        for link in productsLinks: #for link para acessar todas as páginas encontradas na lista de links (productslinks)
            hds = [] #lista de hds disponiveis
            prices = []# preços de cada hd (fazem referencia a posição do preço e hd)
            self.driver.get(link)#acessar cada pagina
            time.sleep(0.5)
            #encontrar o container que contem informaçoes do produto
            productContainer = self.driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[2]/div/div/div[2]") 
            #encontrar o xpath do titulo do produto
            productTitle = productContainer.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[2]/div/div/div[2]/div[1]/h4[2]").text
           #value = productContainer.find_element_by_class_name("price").text
           #encontrar a descrição do produto e pegar o que tem dentro
            descriptionProduct = productContainer.find_element_by_class_name("description").text
            productsId = productsId+1 #incrementar o id
            #encontrar o container com os botoes de hds 
            avaliableHdsContainer = productContainer.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[2]/div/div/div[2]/div[2]")
            #encontrar as tags buttom dos hds
            buttonsHDS = avaliableHdsContainer.find_elements_by_tag_name("button")
        
            for button in buttonsHDS:
                if button.get_attribute("value") == '1024':
                    break
                if button.is_enabled() == True: # condição para verificar se o botão está habilitado
                    button.click()#clicar no botao
                    #toda vez que os botoes dos hds são clicados os preços mudam
                    #encontrar a classe price e pegar o que tem dentro
                    value = productContainer.find_element_by_class_name("price").text
                    #adicionar os valores de preço de cada botão na lista
                    prices.append(value)
                    #adicionar os valores de hd de cada botao na lista
                    hds.append(button.get_attribute("value"))

               
                #add produtos no dicionario com titulo, descriçao, preços e seus hds disponiveis
                products[f'Product {productsId}'] = {
                                                            "title":productTitle,
                                                            "description":descriptionProduct,
                                                            "price": prices,
                                                            "HDs": hds
                                                            }

        time.sleep(2)
        #processo para transformar em json
        products = json.dumps(products)
        responseJson = json.loads(products)

        self.driver.quit()
        return responseJson



 

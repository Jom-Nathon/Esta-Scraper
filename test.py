from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import itertools as itertools
import pandas
import plot


def region_to_list():
    region = []
    with open('region_List.txt', encoding='utf8') as regionFile:
        for key,group in itertools.groupby(regionFile,lambda line: line.startswith('/\n')):
            if not key:
                region = list(group)
                region = list(map(lambda each:each.strip('/'), region))
                region = list(map(lambda each:each.strip('\n'), region))
                return region

def authLoop():
    return True
    #To be fill in with below codes

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

driverURL = 'https://asset.led.go.th/newbidreg/'

driver.get(driverURL)

capchaInputEle = driver.find_element(By.ID, 'pass')
provinceEle = driver.find_element(By.NAME, 'menu2')
prv2 = Select(provinceEle)
confirmEle = driver.find_element(By.ID, 'GFG_Button')

capchaEle = driver.find_element(By.XPATH, '/html/body/div[4]/div/div[1]/table/tbody/tr[1]/td[1]/strong/font/font')
capchaInputEle.send_keys(capchaEle.text)

# allPlotDropDown = driver.find_element(By.XPATH, '/html/body/div[4]/div/div[1]/div/div/div[3]/div/div[1]/table/tbody/tr/td[2]/div')
regionEle = driver.find_element(By.NAME, 'region_name')

region = region_to_list()

ActionChains(driver)\
    .send_keys_to_element(regionEle, region[0])\
    .send_keys(Keys.ENTER)\
    .perform()

confirmEle.click()


## TODO wait until next page come and then proceed without quitting
#https://asset.led.go.th/newbidreg/default.asp?search_asset_type_id=

print("redirecting...")
wait = WebDriverWait(driver, 10)
wait.until(lambda driver: driver.current_url != 'https://asset.led.go.th/newbidreg/')

allPlotEle = driver.find_element(By.XPATH, '//*[@id="box-table-a"]/table')

plotList = ['ชุดที่', 'ลำดับที่การขาย', 'หมายเลขคดี', 'ประเภททรัพย์', 'ไร่', 'งาน', 'ตารางวา', 'ราคาประเมิน', 'ตำบล', 'อำเภอ', 'จังหวัด']
p = []


for row in allPlotEle.find_elements(By.CSS_SELECTOR, 'tr'):
    p.clear()
    for cell in row.find_elements(By.CSS_SELECTOR, 'td'):
        p.append(cell.text)

    if len(p) > 9:
        size = [p[4], p[5], p[6]]
        testPlot = plot.Plot(p[0],p[1],p[2],p[3],size,p[7],p[8],p[9],p[10])
        # print(testPlot)
        # print(row.get_attribute('bgcolor'))

    if cell.get_attribute('bgcolor') != '#E74C3C' and row.get_attribute('bgcolor') == None :
        WebDriverWait(driver, 5).until(expected_conditions.element_to_be_clickable(row)).click()
        driver.switch_to.window(driver.window_handles[1])
        
        wait2 = WebDriverWait(driver, 2).until(expected_conditions.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[4]/div/div')))

        detailGeneral = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[4]/div/div')
        detailPrice1 = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[7]/div')
        detailPrice2 = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[8]')
        detailPicture = driver.find_element(By.ID, 'lightgallery')
        detailSaleSchedule = driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div[6]/div/table')

        print(detailGeneral.text)
        print(detailPrice1.text)
        print(detailPrice2.text)
        print(detailSaleSchedule.text)

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        
# for x in range(0, 9):
#     action.perform
#     print("This is loop number : " , x)
#     time.sleep(1.5)

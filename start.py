from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
import time
from bs4 import BeautifulSoup
import pandas as pd
import pyperclip as pc

PATH = "C:\chromedriver.exe"

driver = webdriver.Chrome(PATH)
driver.get("https://ecalc.ch/motorcalc.php")
action = ActionChains(driver)

#count=2
#selenium for filling inputs automatically
def login():
    element1 = driver.find_element_by_xpath('//*[@id="modalConfirmOk"]')
    element1.click()
    time.sleep(2)

    element2 = driver.find_element_by_xpath('//*[@id="headerRight"]/p/big/b/a')
    element2.click()
    time.sleep(2)

    input_username = driver.find_element_by_id('username')
    input_pwd = driver.find_element_by_id('password')


    input_username.send_keys("username")


    input_pwd.send_keys("pwd")


    login_btn = driver.find_element_by_xpath('//*[@id="myButton"]')
    login_btn.click()
    time.sleep(1)
    alert = driver.switch_to.alert
    alert.accept()
    #time.sleep(5)
    

    cookie_btn = driver.find_element_by_xpath('/html/body/div[3]/div')
    cookie_btn.click()
    time.sleep(5)



class start:
    def __init__(self,**kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
      

    def selenium_initiate(self):
        model_weight = driver.find_element_by_id('inGWeight')
        model_weight.send_keys(Keys.CONTROL,'a')
        model_weight.send_keys(Keys.DELETE)
        model_weight.send_keys(self.inGWeight) #8500
        time.sleep(1)

        model_weight_calc = driver.find_element_by_id('inGWeightCalc')
        selectobj = Select(model_weight_calc)
        selectobj.select_by_visible_text(self.inGWeightCalc) #w/o Battery
        time.sleep(1)

        wing_span = driver.find_element_by_id('inGWingSpan')
        wing_span.send_keys(Keys.CONTROL,'a')
        wing_span.send_keys(Keys.DELETE)
        wing_span.send_keys(self.inGWingSpan) #3000
        time.sleep(1)

        wing_area = driver.find_element_by_id('inGWingArea')
        wing_area.send_keys(Keys.CONTROL,'a')
        wing_area.send_keys(Keys.DELETE)
        wing_area.send_keys(self.inGWingArea) #105
        time.sleep(1)

        field_elevation = driver.find_element_by_id('inGElevation')
        field_elevation.send_keys(Keys.CONTROL,'a')
        field_elevation.send_keys(Keys.DELETE)
        field_elevation.send_keys(self.inGElevation) #914
        time.sleep(1)

        battery_cell_type = driver.find_element_by_id('inBCell')
        selectobj = Select(battery_cell_type)
        selectobj.select_by_visible_text(self.inBCell) #LiPo 10000mAh - 20/30C
        time.sleep(1)

        configuration = driver.find_element_by_id('inBS')
        configuration.send_keys(Keys.CONTROL,'a')
        configuration.send_keys(Keys.DELETE)
        configuration.send_keys(self.inBS) #6
        time.sleep(1)

        controller_type = driver.find_element_by_id('inEType')
        selectobj = Select(controller_type)
        selectobj.select_by_visible_text(self.inEType) #max 120A
        time.sleep(1) 

        motor_mfg_type = driver.find_element_by_id('inMManufacturer')
        selectobj = Select(motor_mfg_type)
        selectobj.select_by_visible_text(self.inMManufacturer) #Turnigy
        time.sleep(1)

        motor_mfg_timing = driver.find_element_by_id('inMType')
        selectobj = Select(motor_mfg_timing)
        selectobj.select_by_visible_text(self.inMType) #NTM PropDrive v2 5060-270 (270)
        time.sleep(1)

        diameter = driver.find_element_by_id('inPDiameter')
        diameter.send_keys(Keys.CONTROL,'a')
        diameter.send_keys(Keys.DELETE)
        diameter.send_keys(self.inPDiameter) #20
        time.sleep(1)

        pitch = driver.find_element_by_id('inPPitch')
        pitch.send_keys(Keys.CONTROL,'a')
        pitch.send_keys(Keys.DELETE)
        pitch.send_keys(self.inPPitch) #12
        time.sleep(1)

        temp = driver.find_element_by_id('inMKv')
        temp.click()
        temp.click()
        temp.send_keys(Keys.CONTROL,'a')
        temp.send_keys(Keys.CONTROL,'c')
        text2 = pc.paste()
        print(text2)
        time.sleep(1)

        calc = driver.find_element_by_xpath('//*[@id="theForm"]/table/tbody/tr[5]/td[17]/input')
        calc.click()
        time.sleep(5)

        DF=bsinit()
        time.sleep(5)
        return DF



#beautifulsoup to scrape the tables

def bsinit():
    df_dict = {}
    df_list=[]
    DF = bs4_initiate(df_dict,df_list,)
    return DF
    
def bs4_initiate(df_dict,df_list):
        
    Dark_Table1_3(df_dict,df_list)
    Dark_Table2(df_dict,df_list)
    Bright_Table(df_dict,df_list)
    
    DF = pd.concat(df_list)
    
    DF = DF.reindex(columns=["Label", "Unit", "Value"])
        #printing the tables
    '''
    for keys,values in df_dict.items(): 
        print('\n\n\t')
        print(keys)
        print('\n')
        print(values)
        '''
    
    motor_partial_load()
    return DF

    




#scraping white tables
def Bright_Table(df_dict,df_list):
    soup = BeautifulSoup(driver.page_source,'lxml')
    for i in range(0,3):
        Brighttable_finder = soup.find_all('td', class_ = 'outBright')[i]
        table_name = Brighttable_finder.find('strong').text.replace('\n', '').replace('\t','')
        trs = Brighttable_finder.find_all('tr')
        tablerow = []
        for tr in trs:
            spans = tr.find_all('span')
            tempspan = []
            for span in spans:
                
                each_span = span.text.replace('\n', '').replace('\t','')
                tempspan.append(each_span)       
            tablerow.append(tempspan)

        df = pd.DataFrame(tablerow,columns = ['Label','Value','Unit'])
        index_names = df[ (df['Value'] == 'oz') | (df['Value'] =='W/lb') | (df['Value'] =='lbf.ft') | (df['Value'] =='°F') | (df['Value'] =='mph') | (df['Value'] =='oz/W') | (df['Value'] =='oz/ft²') | (df['Value'] =='ft/min')].index
        df.drop(index_names, inplace = True)
        df_dict[table_name]=df
        df_list.append(df)
    


# Dark Table 1 and 3
def Dark_Table1_3(df_dict,df_list):
    soup = BeautifulSoup(driver.page_source,'lxml')
    for i in range(0,3,2):
        Darktable_finder = soup.find_all('td', class_ = 'outDark')[i]
        table_name = Darktable_finder.find('strong').text.replace('\n', '').replace('\t','')
        trs = Darktable_finder.find_all('tr')
        tablerow = []
        for tr in trs:
            spans = tr.find_all('span')
            tempspan = []
            for span in spans:
                
                each_span = span.text.replace('\n', '').replace('\t','')
                tempspan.append(each_span)       
            tablerow.append(tempspan)

        df = pd.DataFrame(tablerow,columns = ['Label','Value','Unit'])
        index_names = df[ (df['Value'] == 'oz') | (df['Value'] =='W/lb') | (df['Value'] =='lbf.ft') | (df['Value'] =='°F') | (df['Value'] =='mph') | (df['Value'] =='oz/W') | (df['Value'] =='oz/ft²') | (df['Value'] =='ft/min')].index
        df.drop(index_names, inplace = True)
        df_dict[table_name]=df
        df_list.append(df)
    
#dark table 2

def Dark_Table2(df_dict,df_list):
    soup = BeautifulSoup(driver.page_source,'lxml')
    i=0
    Darktable_finder = soup.find_all('td', class_ = 'outDark')[1]
    tablename_example = ["Motor @ Maximum","Wattmeter readings"]
    table_finder = Darktable_finder.find_all('table')
    for table in table_finder:
        trs = table.find_all('tr')
        tablerow = []
        for tr in trs:
            spans = tr.find_all('span')
            tempspan = []
            for span in spans:
                
                each_span = span.text.replace('\n', '').replace('\t','')
                tempspan.append(each_span)       
            tablerow.append(tempspan)  
        df = pd.DataFrame(tablerow,columns = ['Label','Value','Unit'])
        index_names = df[ (df['Value'] == 'oz') | (df['Value'] =='W/lb') | (df['Value'] =='lbf.ft') | (df['Value'] =='°F') | (df['Value'] =='mph') | (df['Value'] =='oz/W') | (df['Value'] =='oz/ft²') | (df['Value'] =='ft/min')].index
        df.drop(index_names, inplace = True)
        df_dict[tablename_example[i]]=df
        df_list.append(df)
        i=i+1
#| (df['Unit'] =='W/lb') | (df['Unit'] =='lbf.ft') | (df['Unit'] =='°F') | (df['Unit'] =='mph') | (df['Unit'] =='oz/W') | (df['Unit'] =='oz/ft²') | (df['Unit'] =='ft/min')
#big table
def motor_partial_load():
    soup = BeautifulSoup(driver.page_source,'lxml')
    mpl_table = soup.find('table', { "id" : "rpmTable" })
    
    count = len(mpl_table.find_all('tr'))
    tablerow = []
    for i in range(2,count):
        trs = mpl_table.find_all('tr')[i]
        
        tds = trs.find_all('td')
        temptd = []
        for td in tds:
            each_td = td.text.replace('\n', '').replace('\t','')
            temptd.append(each_td)
            
        tablerow.append(temptd)
        #print(tablerow)
    print(len(tablerow))
    
    df2 = pd.DataFrame(tablerow,columns = ['Propeller rpm', 'Throttle %', 'Current (DC) A', 'Voltage (DC) V', 'el. Power W', 'Efficiency %', 'Thrust g', 'Thrust oz	', 'Spec. Thrust g/W', 'Spec. Thrust oz/W', 'Pitch Speed km/h', 'Pitch Speed mph', 'Speed (level) km/h', 'Speed (level) mph', 'Motor Run Time (85%) min'])
    print(df2)
    df2.to_csv('MPL.csv')




















if __name__ == '__main__':
    limit = 2
    login()
    value1={'inGWeight': 9000,
        'inGWeightCalc': "incl. Drive",
        'inGWingSpan': 4000,
        'inGWingArea': "158.346",
        'inGElevation': 914,
        'inBCell': "Panasonic NCR18650GA - 3C/4C",
        'inBS': 6,
        'inEType': "max 120A",
        'inMManufacturer': "Turnigy",
        'inMType': "NTM PropDrive v2 5060-270 (270)",
        'inPDiameter': 20,
        'inPPitch': 12}
    val1 = start(**value1) 
    MAINDF = val1.selenium_initiate()

    MAINDF.to_csv('df1.csv')

    #val2 = start(**value1)
    #MAINDF2 = val2.selenium_initiate()
    #MAINDF2.to_csv('df2.csv')
    #values = MAINDF2["Value"]
    #MAINDF = MAINDF.join(values, how = 'left', lsuffix = '_left', rsuffix = '_right')
    #MAINDF['Value2']=values

    #MAINDF.to_csv('file1.csv')
   
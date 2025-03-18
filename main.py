import pandas as pd
import os
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
from dotenv import load_dotenv

def load_identity(path = ".env"):
    try:
        load_dotenv(path)

        user_name : str = os.getenv('USER_NAME')
        password : str = os.getenv('PASSWORD')
        
        return {"user_name": user_name, "password": password}
    
    except:
        return {"user_name": "", "password": ""}

def scrap(identity):
    urls = {
        'coop': "https://cse.hkust.edu.hk/ug/comp4910/Password_Only/2025-26/",
        'regular': "https://cse.hkust.edu.hk/ug/internship/?id=listjob"
    }
    
    res = requests.get(urls['coop'], auth=HTTPBasicAuth(identity['user_name'], identity['password']))
    soup = BeautifulSoup(res.text, 'html.parser')
    items = soup.find_all('tr')
    coop_df = pd.DataFrame([{
        'Job' : i.find('td').find_next_sibling('td').a.text,
        'Company' : i.find_all('td')[-1].text
    } for i in items[1:]])
    
    res = requests.get(urls['regular'], auth=HTTPBasicAuth(identity['user_name'], identity['password']))
    soup = BeautifulSoup(res.text, 'html.parser')
    items = soup.find_all('tr')
    regular_df = pd.DataFrame([{
        'Job' : i.find('td').find_next_sibling('td').a.text,
        'Company' : i.find_all('td')[-3].text,
        'Closing Date' : i.find_all('td')[-2].text,
        'Opening Date' : i.find_all('td')[-1].text
    } for i in items[1:]])
    
    return coop_df, regular_df

def export_spreadsheet(coop_df, regular_df, path = "CSE Intern.xlsx"):
    try:
        with pd.ExcelWriter(path) as writer:
            coop_df.to_excel(writer, sheet_name="Co-op", index=False)
            regular_df.to_excel(writer, sheet_name="Regular", index=False)
        print("Spreadsheet exported successfully")
    except:
        print("Error exporting spreadsheet")

def main():
    identity = load_identity()
    coop, regular = scrap(identity)
    export_spreadsheet(coop, regular)

if __name__ == "__main__":
    main()
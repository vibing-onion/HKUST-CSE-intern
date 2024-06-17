import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

url = "URL"
web = requests.get(url)
soup = BeautifulSoup(web.text, "html.parser")
job_content = soup.select("tbody")

job_title = job_content[0].select("a")
job_title = [tag.get_text() for tag in job_title]
company_title = job_title[1::2]
job_title = job_title[0::2]

start_end = job_content[0].find_all("td", {"class": "uk-text-nowrap"})
start_end = [tag.get_text() for tag in start_end]
start_end = [re.sub(r'[^0-9\-]', "", text) for text in start_end]
start = start_end[1::2]
end = start_end[0::2]

job_board = pd.DataFrame({"Company": company_title, "Position": job_title, "Start": start, "End": end})
job_board = job_board.set_index("Company").sort_values("Company")

def main():
    option = "1"
    while(option):
        if option == "1":
            print("\n\nCSE JOB BOARD:\n\nSort by: Company")
            print(job_board)
        if option == "2":
            print("\n\nCSE JOB BOARD:\n\nSort by: End of Application")
            print(job_board.sort_values("End"))
        if option != "1" and option != "2":
            print("Wrong Input")
        option = input("\n\nPlease Input a number:\n1: Sort by Company Name\n2: Sort by End of Application\n3: Quit")
        if option == "3":
            break

if __name__ == "__main__":
    main()
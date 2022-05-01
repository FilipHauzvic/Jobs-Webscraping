# Author: Filip Haužvic
# Licence: GPL-3
# Python 3.9

# Gets all job listings in a given region and list certain details
import sys
import re
from bs4 import BeautifulSoup
from requests_html import HTMLSession

usage = "python brigada.py [mesto]\n"

argc = len(sys.argv)
if argc > 2:
    print(f"Spatny pocet argumentu!\npouziti: {usage}")
    exit(1)

location = "prerov"
if argc == 2:
    location = sys.argv[1]

# Every page has 14 listings, so we have to increase the index by 14 every time we want to go to another page
index = 0
out = open("output.txt", "w", encoding="utf-8")

session = HTMLSession()
while True:
    url = f"https://www.fajn-brigady.cz/brigady/{location}/?s={index}"

    result_js = session.get(url)
    result_js.html.render()
    soup = BeautifulSoup(result_js.html.html, "html.parser")

# If there's no available listings, we break the current while loop and end the program
    unavailable = soup.find(text = re.compile('Bohužel jsme nenašli žádnou vhodnou nabídku'))

    if unavailable is None:
        result = soup.find("div", class_ = "posts")

        jobs = result.find_all("a", class_ = "vis")

        for job in jobs:
            job_url = job["href"]

            job_session = session.get(job_url)
            job_session.html.render()
            
            job_result = BeautifulSoup(job_session.html.html, "html.parser")

            job_name = job_result.find("h1")
            job_description = job_result.find("div", class_ = "main-wrapper").find("p")
            job_location = job_result.find("div", class_ = "col-md-6").find("tr").find_all("td")[1]
            job_requirements = job_result.find("div", class_ = "main-wrapper").find_all("p")[1]

            print(job_name + "\n")

            out.write("NAZEV: " + job_name.text.strip() + "\n")
            out.write("POPIS:\n" + job_description.text.strip() + "\n")
            out.write("POZADAVKY:\n" + job_requirements.text.strip() + "\n")
            out.write("LOKACE:\n" + job_location.text.strip() + "\n")
            out.write(f"ODKAZ: \n{job_url}")
            out.write("\n\n")

        index += 14
    else:
        out.write("Nebyla nalezena zadna nabidka")
        break

print("Vypis dokoncen\n")
out.close()
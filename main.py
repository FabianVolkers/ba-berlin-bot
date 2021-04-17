"""
Main file
"""
import re
from datetime import datetime

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

MONTHS = {
    "Januar": "January",
    "Februar": "February",
    "März": "March",
    "April": "April",
    "Mai": "May",
    "Juni": "June",
    "Juli": "July",
    "August": "August",
    "September": "September",
    "Oktober": "October",
    "November": "November",
    "Dezember": "December"
}

def parse_table(table):
    month_el = table.find_elements_by_class_name("month")[0]
    month = month_el.text
    [month, year] = month.split(" ")
    month = MONTHS[month]

    days_els = table.find_elements_by_tag_name("td")

    appointments = {}
    """
    appointments = {
        "2021-04-01": [
            "13:00": "Bürgeramt Schöneberg"
        ]
    }
    """

    for i, day_el in enumerate(days_els):
        if day_el.text == "" or day_el.text == " ":
            #del days_els[i]
            continue
        else:
            date = datetime.strptime(f"{day_el.text} {month} {year}", "%d %B %Y")
            appointments[date.strftime("%Y-%m-%d")] = "buchbar" == day_el.get_attribute("class")

    return appointments

def parse_appointments(day_el):
    day_el.click()


if __name__ == "__main__":
    options = webdriver.FirefoxOptions()
    #options.add_argument('-headless')
    driver = Firefox(
        executable_path='/usr/local/bin/geckodriver',
        options=options)

    driver.get("https://service.berlin.de/terminvereinbarung/termin/tag.php?termin=1&anliegen[]=120703&dienstleisterlist=122210,122217,327316,122219,327312,122231,327346,122238,122243,327348,122252,329742,122260,329745,122262,329748,122254,329751,122271,327278,122273,327274,122277,327276,122280,327294,122282,327290,122284,327292,122291,327270,122285,327266,122286,327264,122296,327268,150230,329760,122301,327282,122297,327286,122294,327284,122312,329763,122304,327330,122311,327334,122309,327332,122281,327352,122279,329772,122276,327324,122274,327326,122267,329766,122246,327318,122251,327320,327653,122257,330265,327322,122208,327298,122226,327300&herkunft=http%3A%2F%2Fservice.berlin.de%2Fdienstleistung%2F120703%2F")
    tables = driver.find_elements_by_tag_name("table")    

    appointments = {}
    for table in tables:
        appointments.update(parse_table(table))


    driver.find_elements_by_class_name("next")[0].click()
    table3 = driver.find_elements_by_tag_name("table")[1]
    appointments.update(parse_table(table3))

    print(appointments)

    driver.quit()


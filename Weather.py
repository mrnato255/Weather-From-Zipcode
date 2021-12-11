from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from pyzipcode import ZipCodeDatabase
import time

# Creates a set full of possible answers to the Y/N questions
yes = set(['yes','y', 'ye', 'Y', 'Yes', 'YES','yes ','y ', 'ye ', 'Y ', 'Yes ', 'YES '])
no = set(['no','n', 'N', 'No', 'NO', 'no ','n ', 'N ', 'No ', 'NO '])

# A function that takes the parsed data and formats it so it looks pretty
def format(is_parse, labels, answers):
    placeholder = False
    while placeholder == False:
        if is_parse in yes:
            for (DataLabel, DataAnswer) in zip(labels, answers):
                print(DataLabel.text + ": " + DataAnswer.text)
                time.sleep(1)
                placeholder = True
        elif is_parse in no: 
            placeholder = True
        else:
            is_parse = input("Please respond with \'y\' or \'n\' -> ")
            placeholder = False

# The reason these few lines exist, and why I chose weather.gov in the first place, is that the weather.gov URL has the latitude and longitude in it. My thinking was that
# if I can ask for someones zipcode, turn it into latitude and longitude, and shove it into the URL, I would be good. That's exactly what the code below does. It uses the 
# pyzipcode library to turn a zipcode into latitude and longitude and then inserts it into the URL for parsing.

# Asks the user for their zip code
yourzip = input("what's your zipcode? -> ")

# Uses the pyzipcode library to find the latitude and longitude from the users zipcode
lat = ZipCodeDatabase()[yourzip].latitude
lon = ZipCodeDatabase()[yourzip].longitude

# Inserts latitude and longitude into the url.
my_url = 'https://forecast.weather.gov/MapClick.php?lat=' + str(lat) + '&lon=' + str(lon) + '#.XGTPH1xKiUk'

# Opening up connection, grabbing the page.
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# html parsing
page_soup = soup(page_html, "html.parser")

# grabs all the specific chunks of html needed
Temp = page_soup.find("p", {"class":"myforecast-current-lrg"})
Desc = page_soup.find("p", {"class":"myforecast-current"})
WeekForecast = page_soup.find("div", {"id":"detailed-forecast-body"})
Data = page_soup.find("div", {"id":"current_conditions_detail"})

# prints the temp without the extra code
print("The temperature is " + Temp.text + " and the conditions are " + Desc.text)

# Days_labels and DayDescriptions_answers are two seperate lists. Days_labels takes all the b tags from the chunk of HTML called "WeekForecast" which contain the days in the seven day forecast
Days_labels = WeekForecast.find_all('b')
# DayDescriptions_answers takes the same chunk of HTML and filters it out into a list of only div tags with the class "col-sm-10 forecast-text". Those div tags contain the day descriptions
DayDescriptions_answers = WeekForecast.find_all("div", class_="col-sm-10 forecast-text")

# this is doing the same as Days_labels and DayDescriptions_answers. It's making a list with the b tags which contain the names (humidity, windspeed, etc.)
IndividualDataLabels = Data.find_all("b")
# this makes a list with the td tags which with no class (the td tags with a class have the data I grabbed above as children). This contains the actual data that coincides with the names.
IndividualDataAnswers = Data.find_all("td", attrs={'class': None})

# asks if the user would like some more data about the weather in their area
more_data = input("Would you like some more data about the weather? (Y/N) -> ")

# if the answer is in any way yes it combines the two lists using a for loop. If it's no then the program moves on
format(more_data, IndividualDataLabels, IndividualDataAnswers)

# asks if the user would like the seven day forecast for their area
Seven_Day_Forecast = input("Do you want the seven day forecast? (Y/N) ->")

# if the answer is in any way yes it combines the two lists using a for loop. If it's no then the program moves ends
format(Seven_Day_Forecast, Days_labels, DayDescriptions_answers)




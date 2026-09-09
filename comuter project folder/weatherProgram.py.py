# Weather Program for Little Elm's Nursery
# Importing necessary libraries
from tkinter import *
from time import *
from PIL import Image, ImageTk


import requests
import datetime 
import emoji



#---------------------------------------------------------------
# SUBPROGRAMS
#---------------------------------------------------------------

# subprograms for making weather Dictionary
# takes data from API
def get_weather_data(api_key, city = "London"):
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
  
    params = {
        "q":city,
        "appid":api_key,
        "units": "metric" }
        
    response = requests.get(BASE_URL,params=params)
    return response.json()
# Edited and Error checked 17/03/2026 

def exception_handler(api_key, city = 'London'):
    URL = "http://api.openweathermap.org/data/2.5/weather?"
  
    params = {
        "q":city,
        "appid":api_key,
        "units": "metric" }
        
    response = requests.get(URL,params=params)
    match response.status_code:
        case 400:
            print("Bad request\n The server could not understand the request due to invalid syntax")
        case 401:
            print("Unauthorized\n  invalid API key  ")
        case 403:
            print("Forbidden\n The server refused to fulfill the request")
        case 404:
            print("Not Found\n - City not found")
        case 500:
            print("Internal Server Error\n - Please try again later")
        case 502:
            print("Bad Gateway\n - Invalid response from server")
        case 503:
            print("Service Unavailable\n Server is down")
        case 504:
            print("Gateway Timeout\n  Server is not responding")


# creates dictionary with necessary weather data
def parse_weather_data(parse_data):
    weather_dictionary = {
    "main": parse_data['weather'][0]['main'],
    "description": parse_data['weather'][0]['description'],
    "temp": parse_data['main']['temp'],
    "feels_like": parse_data['main']['feels_like'],
    "humidity": parse_data['main']['humidity'],
    "wind_speed": parse_data['wind']['speed'],
    "sunrise": parse_data['sys']['sunrise'],
    "sunset": parse_data['sys']['sunset'],
    "timezone": parse_data['timezone']
    }

    return weather_dictionary
# Edited 18/03/2026 Error checked 18/03/2026


# calculate sunset and sunrise and time as digital and add to weather list
def calculations(weather_dictionary):

    # convert unix -> HH:MM
    def to_time(ts):
        return datetime.datetime.fromtimestamp(ts).strftime("%H:%M")
    
    weather_dictionary["sunrise"] = to_time(weather_dictionary["sunrise"])
    weather_dictionary["sunset"] = to_time(weather_dictionary["sunset"])

    return weather_dictionary


# Subprograms for different weather conditions and advice for the nursery
def generate_advice(weather_dictionary, trip):
    advice_string = ""
    number = 0
    safety_level = 0
    no_trip = 0
    indoor_play = 0

    # advice for dangerous main weather conditions
    match weather_dictionary["main"]:
        case "Thunderstorm":
            advice_string = advice_string + "The children must stay inside, There is a thundertorm,"
            number = number + 1
            safety_level = safety_level + 2
            no_trip = no_trip + 1
        case "Snow":
            advice_string = advice_string + "Close off slippery areas,"
            advice_string = advice_string + "Use grit/salt on walkways,"
            advice_string = advice_string + "Supervise closely to prevent slipping,"
            advice_string = advice_string + "Avoid snowball throwing (risk of ice injuries),"
            advice_string = advice_string + "Ensure children have waterproof boots,"
            no_trip = no_trip + 1
            number = number + 5
            safety_level = safety_level + 1
        case "Tornado":
            advice_string = advice_string + "Seek shelter in a room on the lowest floor. There is a tornado warning,"
            no_trip = no_trip + 1
            number = number + 1
            safety_level = safety_level + 5

    # Advice for different temperatures
    # below 5°C
    if weather_dictionary["temp"] < 5:
        advice_string = advice_string + "Limit outdoor play,"
        advice_string = advice_string + "Ensure children are properly dressed for the cold,"
        advice_string = advice_string + "Provide warm drinks and snacks,"
        advice_string = advice_string + "Check for ice,"
        number = number + 4

    # 5–10°C
    elif weather_dictionary["temp"] >=5 and weather_dictionary["temp"] <10:
        advice_string = advice_string + "Outdoor play allowed with coats,"
        advice_string = advice_string + "Shorter sessions recommended,"
        number = number + 2

    # 10–20°C
    elif weather_dictionary["temp"] >=10 and weather_dictionary["temp"] <20:
        advice_string = advice_string + "Normal outdoor play,"
        advice_string = advice_string + "Light layers recommended for clothing,"
        number = number + 2

    # 20–25°C
    elif weather_dictionary["temp"] >=20 and weather_dictionary["temp"] <25:
        advice_string = advice_string + "Encourage frequent water breaks throughout the day,"
        advice_string = advice_string + "Keep children in shaded areas during outdoor play,"
        advice_string = advice_string + "Dress children in loose breathable cotton clothing and their sun hats,"
        number = number + 3
    # 25°C+
    elif weather_dictionary["temp"] >=25 : 
        advice_string = advice_string + "Provide extra water stations,"
        advice_string = advice_string + "Cancel or shorten outdoor sessions,"
        advice_string = advice_string + "Move activities to shaded or indoor areas,"
        advice_string = advice_string + "Avoid vigorous play,"
        advice_string = advice_string + "Monitor children for signs of overheating (flushed skin/ tiredness/ irritability),"
        advice_string = advice_string + "Keep indoor rooms cool with ventilation or fans,"
        no_trip = no_trip + 1
        number = number + 6
        safety_level = safety_level + 1


    #Advice for humidity
    if weather_dictionary["humidity"] >= 70:
        advice_string = advice_string + "Keep rooms ventilated,"
        advice_string = advice_string + "Avoid heavy physical activity,"
        advice_string = advice_string + "Provide extra water,"
        no_trip = no_trip + 1
        number = number + 3


    # Advice for wind speed
    #Mild wind (1-25)
    if weather_dictionary['wind_speed'] < 25:
        advice_string = advice_string + "Secure loose outdoor toys,"
        advice_string = advice_string + "Avoid lightweight equipment (parachutes/ paper crafts),"
        advice_string = advice_string + "Keep children away from unstable structures,"
        number = number + 3
    #Strong wind (25–38 mph)
    elif weather_dictionary['wind_speed'] >= 25 and weather_dictionary['wind_speed'] < 39:
        advice_string = advice_string + "Restrict outdoor play,"
        advice_string = advice_string + "Check for falling branches or debris,"
        advice_string = advice_string + "Keep children away from fences, sheds, and trees,"
        number = number + 3
    #Gale‑force winds (39+ mph)
    elif weather_dictionary['wind_speed'] >= 39:
        advice_string = advice_string + "No outdoor play,"
        advice_string = advice_string + "Keep all children indoors,"
        advice_string = advice_string + "Close blinds/curtains if debris risk is high,"
        no_trip = no_trip + 1
        number = number + 3
        safety_level = safety_level + 1


    #Advice for rain
    #light rain
    if weather_dictionary['description'] == "light rain" or weather_dictionary['description'] =="moderate rain":
        advice_string = advice_string + "Use waterproof coats and hoods,"
        advice_string = advice_string + "Avoid muddy or waterlogged areas,"
        advice_string = advice_string + "Dry childrens clothes promptly,"
        number = number + 3
    #Heavy rain
    elif weather_dictionary['description'] == "heavy intense rain" or weather_dictionary['description'] == "shower rain":
        advice_string = advice_string + "move play indoors,"
        advice_string = advice_string + "check for flooding or pooling water,"
        advice_string = advice_string + "ensure all windows are checked,"
        no_trip = no_trip + 1
        number = number + 3

    # combined variables

    if trip == "yes" and no_trip != 0:
        advice_string = advice_string + "Outdoor trip is not recommended today due to the weather conditions,"
        number = number + 1
    elif trip == "yes" and no_trip == 0:
        advice_string = advice_string + "Outdoor trip is allowed today,"
        number = number + 1

    advice_string = advice_string + "The safety level is at: " + str(safety_level) + ","
    number = number + 1
    return advice_string, number


def advice_format(weather_dictionary, trip):
    advice = Tk()
    advice.geometry("480x330")
    advice.title("Little Elm's Nursery Weather Advice")
    advice.config(background="#E0CFFF")
    label = Label(advice, text="Weather Advice", font=('arial', 20, 'bold', 'underline'), fg='#8C59EB', bg='#E0CFFF')
    label.pack()
    label.place(x=144, y=13)

    #-------------------------------
    # leaf image
    #-------------------------------
    img = Image.open("leaf.png")
    img = img.resize((60, 60))
    leaf_icon = ImageTk.PhotoImage(img)
    Label(advice, image=leaf_icon, bg="#E0CFFF").place(x=20, y=0)
    Label(advice, image=leaf_icon, bg="#E0CFFF").place(x=400, y=0)

    advice_string, number = generate_advice(weather_dictionary, trip)
    coordinateY = 85

    # Adjust window height based on the number of advice lines
    if number > 8:
        height_increment = number - 8
        new_height = 330 + height_increment * 30
        new_height = str(new_height)
        geometry_string = "480x" + new_height
        advice.geometry(geometry_string)


    for i in range(number):
        advice_split = advice_string.split(",", 1)
        window_label = advice_split[0]
        instruction = Label(advice, text=window_label,
                            font=('arial', 10, 'bold'),
                            fg='#8C59EB', bg='#E0CFFF')
        instruction.place(x =19, y = coordinateY)
        coordinateY = coordinateY + 30
        advice_string = advice_split[1]
    advice.mainloop()


def update_time():
    time_string = strftime("%I:%M %p")
    time_label.config(text = time_string)

    day_string = strftime("%A")
    day_label.config(text = day_string)

    time_label.after(1000, update_time) 



def emojis(weather_dictionary):
    # Return the appropriate emoji based on weather conditions
    emoji = ""
    if weather_dictionary["main"] == "Thunderstorm":
        emoji = ":cloud_with_lightning_and_rain:"
        return emoji
    elif weather_dictionary["main"] == "Drizzle":
        emoji = ":sun_behind_rain_cloud:"
        return emoji
    elif weather_dictionary["main"] == "Rain":
        emoji = ":cloud_with_rain:"
        return emoji
    elif weather_dictionary["main"] == "Snow":
        emoji = ":snowflake:"
        return emoji
    elif weather_dictionary["main"] == "Mist" or weather_dictionary["main"] == "Fog" or weather_dictionary["main"] == "Smoke" or weather_dictionary["main"] == "Haze" or weather_dictionary["main"] == "Dust" or weather_dictionary["main"] == "Sand"or weather_dictionary["main"] == "Ash":
        emoji = ":dash:"  
        return emoji
    elif weather_dictionary["main"] == "Squall":
        emoji = ":wind_face:"
        return emoji
    elif weather_dictionary["main"] == "Tornado":
        emoji = "tornado"
        #return emoji
    elif weather_dictionary["main"] == "Clear":
        emoji = ":sun_with_face:"
        return emoji
    elif weather_dictionary["main"] == "Clouds":
        emoji = ":cloud:"
        return emoji


# Subprograms for making weather windows
#  making window + design
def weather_format(weather_dictionary):
    weather = Tk()
    weather.geometry("360x350")
    weather.title("Little Elm's Nursery Weather Forecast")
    weather.config(background = "#DEFFCF")


    # Time variable
    global  time_label 
    time_label = Label(weather,
                font = (' arial' , 25 , 'italic' , 'bold'),
                 fg = '#60CF57', bg = '#DEFFCF')
    time_label.place(x= 20, y = 25)
    # Date label
    global day_label 
    day_label= Label(weather,
                font = (' arial' , 23 , 'italic' , 'bold'),
                 fg = '#60CF57', bg = '#DEFFCF')
    day_label.place(x = 200, y = 25)


    update_time()

    # Title label
    label = Label(weather,
                  text = "Weather Forecast", 
                  font = ('arial', 10 , 'bold' ), 
                  fg = '#60CF57', bg = '#DEFFCF')
    label.place(x = 125,y = 0)


    # Weather emoji(example:sunny)
    emoji_label = Label(weather,
                        text = emoji.emojize(emojis(weatherDictionary)),
                        font = ("arial", 100),
                        bg = "#DEFFCF")
    emoji_label.place(x=19, y =80)

    # Main weather label(example:sunny)
    main_weather_label = Label(weather,
                               text = weatherDictionary["description"],
                               font = ('arial' , 25 , 'bold'),
                               fg = '#60CF57', bg = '#DEFFCF')
    main_weather_label.place(x =40,y=250)

    # temprature variable
    temperature = Label(weather,
                       text = "Temperature: " + str(weatherDictionary["temp"]) + "°C",
                       font = (' arial' , 10 ,'bold'),
                       fg = '#60CF57', bg = '#DEFFCF')
    temperature.place(x= 215, y = 85)

    # feels like variable
    feels_like = Label(weather,
                       text = "Feels Like: " + str(weatherDictionary["feels_like"]) + "°C",
                       font = (' arial' , 10 ,'bold'),
                       fg = '#60CF57', bg = '#DEFFCF')
    feels_like.place(x= 215, y =115)

    # Humidity Variable
    humidity = Label(weather,
                     text = "Humidity: " + str(weatherDictionary["humidity"]) + "%",
                     font = (' arial' , 10 ,'bold'),
                     fg = '#60CF57', bg = '#DEFFCF')
    humidity.place(x= 215, y = 145)

    # wind speed variable
    wind_speed = Label(weather,
                       text = "wind Speed: " + str(weatherDictionary["wind_speed"]) + "m/s",
                       font = (' arial' , 10 ,'bold'),
                       fg = '#60CF57', bg = '#DEFFCF')
    wind_speed.place(x= 215, y = 175)

    # sunset variable
    sunset = Label(weather,
                   text = "Sunset: " + str(weatherDictionary["sunset"]),
                   font = (' arial' , 10 ,'bold'),
                   fg = '#60CF57', bg = '#DEFFCF')
    sunset.place(x= 215, y = 205)

    # sunrise variable
    sunrise = Label(weather,
                    text = "Sunrise: " + str(weatherDictionary["sunrise"]),
                    font = (' arial' , 10 ,'bold'),
                    fg = '#60CF57', bg = '#DEFFCF')
    sunrise.place(x= 215, y = 235)

    weather.mainloop()




#----------------------------------------------------------------
# MAIN PROGRAM
#----------------------------------------------------------------
# data handling variables
api_key = "72d4bf7c6c2afdb4a01d28534f4921ac"
exception_handler(api_key)
parse_data = get_weather_data(api_key)
weather_dictionary = parse_weather_data(parse_data)
weatherDictionary = calculations(weather_dictionary)

# user oriented variables
weatherOrAdvice = input("Would you like the current weather forecast, Advice for the nursery or both? (Weather/Advice/Both)")
user_decision = weatherOrAdvice.lower()



# ~ Main ~
if user_decision == "weather":
    weather_format(weatherDictionary)

elif user_decision =="advice":
    # ask for trip information
    trip = input("Will there be an outdoor trip today?(yes/no) :")
    trip = trip.lower()
    if trip != 'yes' and trip != 'no':
        print("Invalid input, please try again.")
        exit()
    #output advice
    generate_advice(weatherDictionary,trip)
    advice_format(weatherDictionary,trip)
elif user_decision == "both":
    # ask for trip information
    trip = input("Will there be an outdoor trip today?(yes/no) :")
    trip = trip.lower()
    if trip != 'yes' and trip != 'no':
        print("Invalid input, please try again.")
        exit()
    # Display weather and advice
    print("After viewing the weather forecast, close the weather window to view the advice window.")
    print(weather_format(weatherDictionary))
    advice_format(weatherDictionary, trip)
else:
    print("Invalid input, please try again.")


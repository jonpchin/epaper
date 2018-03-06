# jonc
# 3/3/2018
# Fetches weather data to be displayed on epaper
from datetime import date
import time
import requests
import json
import epd2in7b
import Image
import ImageFont
import ImageDraw
import sys
import os
import urllib
from PIL import Image

def main():
    if len(sys.argv) >= 2:
        # Update from queries config file
        if sys.argv[1] == "--print":
            print("printing image array")
            #frame_black = epd.get_frame_buffer(Image.open('black.bmp'))
            #frame_red = epd.get_frame_buffer(Image.open('red.bmp'))
            #epd.display_frame(frame_black, frame_red)
            #im.rotate(45).show()
            #data = [im.getpixel((x, y)) for x in range(im.width) for y in range(im.height)]
            #print(data)
        # Fetch images and shrinks them to the appropriate 8x8 size
        elif sys.argv[1] == "--fetch":
            if len(sys.argv) == 3:
                print("fetching and shrinking image")
                search_phrase = sys.argv[2]
                image_type = "all"
                url = "https://pixabay.com/api/?key=" + getPixabayKey() + "&q=" + search_phrase + \
                    "&image_type=all"
                result = (requests.get(url)).json()
                limit = 10
                i=0

                for hits in result["hits"]:
                    url = hits["webformatURL"]
                    output_path = "img/" + search_phrase
                    output_path = output_path + "_" + str(i) + get_extension(url)
                    print(url)
                    urllib.urlretrieve(url, output_path.replace(" ", "_")) 

                    # Convert image to correct size
                    img = Image.open(output_path).convert('L')
                    new_img = img.resize((176,264))
                    new_img.save(output_path)
                    i+=1
                    if i==limit:
                        break

        elif sys.argv[1] == "--display":
            print("displaying images in img folder")
            epd = epd2in7b.EPD()
            epd.init()
            # clear the frame buffer
            frame_black = [0] * (epd.width * epd.height / 8)
            frame_red = [0] * (epd.width * epd.height / 8)
            output_path = "img/"
            for filename in os.listdir(output_path):
                with open(output_path + "/" + filename) as img_file: 
                    print(filename)
                    frame_black = epd.get_frame_buffer(Image.open('img/' + filename))
                    #frame_red = epd.get_frame_buffer(Image.open('red.bmp'))
                    epd.display_frame(frame_black, frame_red)
                    time.sleep(30)
        elif sys.argv[1] == "--weather":
            updateWeather()
    else:
        print("Please enter a valid argument")

# Updates weather information on epaper, pass in any variable to write to file
def updateWeather(writeToFile = None):
    location = "orlando"
    units = "imperial"
    url = "https://api.openweathermap.org/data/2.5/weather?q=" + location + "&units="+ units +"&appid=" + getAppKey()

    result = requests.get(url)
    weatherData = result.json()

    if writeToFile is not None:
        # Write json data to file
        with open('data/'+ location +'.json', 'w') as outfile:
            json.dump(weatherData, outfile)
    print("Temperature is:")
    
    print(weatherData['main']['temp'])
    print(weatherData['weather'][0]['description'])

    DayL = ['Mon','Tues','Wednes','Thurs','Fri','Satur','Sun']
    dayOfWeek = DayL[date.today().weekday()] + 'day'
    print(dayOfWeek)

    epd = epd2in7b.EPD()
    epd.init()
    
    # clear the frame buffer
    frame_black = [0] * (epd.width * epd.height / 8)
    frame_red = [0] * (epd.width * epd.height / 8)
    
    COLORED = 1
    UNCOLORED = 0

    # draw strings to the buffer
    #font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMonoBold.ttf', 18) 
    #epd.draw_string_at(frame_black, 10, 20, time.strftime("%m/%d/%Y"), font, COLORED)
    #epd.draw_string_at(frame_black, 10, 50, dayOfWeek, font, COLORED)
    #epd.draw_string_at(frame_black, 10, 80, str(weatherData['main']['temp']) + u"\u00b0" + "F", font, COLORED)
    #epd.draw_string_at(frame_red, 10, 110, weatherData['weather'][0]['description'], font, COLORED)
    # display the frames
    #epd.display_frame(frame_black, frame_red)

    # display images
    frame_black = epd.get_frame_buffer(Image.open('img/saved_ging2.png'))
    #frame_red = epd.get_frame_buffer(Image.open('red.bmp'))
    epd.display_frame(frame_black, frame_red)

def getAppKey():
    return open('secret/openweather.txt', 'r').read()

def getPixabayKey():
    return open('secret/pixabay.txt', 'r').read()

def get_extension(path_to_file):
    return os.path.splitext(path_to_file)[1]

if __name__ == "__main__":
    main()
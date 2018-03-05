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
        elif sys.argv[1] == "--resize":
            img = Image.open('img/saved_ging2.jpg')
            new_img = img.resize((176,264))
            new_img.save('img/saved_ging2.png','png')
        elif sys.argv[1] == "--convert":
            print("converting image")
            im = Image.open("img/ging2.jpg").convert('L')
            im.save("img/saved_ging2.jpg")
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

if __name__ == "__main__":
    main()
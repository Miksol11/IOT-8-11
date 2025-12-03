def printOnDisplay(temperature, pressure, humidity, altitude, disp):
    #Image
    #image = Image.new("RGB", (disp.width, disp.height), "White")
    image = Image.new("RGB", (96, 64), "WHITE")
    draw = ImageDraw.Draw(image)

    # Czcionka
    # font = ImageFont.truetype('./lib/oled/Font.ttf', 14)
    font = ImageFont.truetype('arial.ttf', 14)
    
    dictionary = {'Temperature': temperature, 'Pressure': pressure, 'Humidity': humidity, 'Altitude': altitude}
    height = 0
    for key in dictionary:
        icon = Image.open(f'Lab10/icons/{key}.png')
        image.paste(icon, (0, height), icon)
        draw.text((18, height), f"{dictionary[key]}", font=font, fill="BLACK")
        height+=16

    # Wyświetlanie
    # disp.ShowImage(image, 0, 0)
    image.show() #for testing
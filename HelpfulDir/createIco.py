from PIL import Image
logo = Image.open("icon.png")
logo.save("icon.ico",format='ICO')
logo.close()

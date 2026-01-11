import pytesseract
from PIL import Image

img = Image.open("chart.png")
text = pytesseract.image_to_string(img)

print("EXTRACTED TEXT:")
print(text)


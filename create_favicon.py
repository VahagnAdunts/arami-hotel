from PIL import Image
import os

# Open the original logo
img = Image.open('hotel_booking/static/arami_logo.png')

# Create a 32x32 favicon (standard size)
favicon = img.resize((32, 32), Image.Resampling.LANCZOS)

# Save as favicon
favicon.save('hotel_booking/static/favicon.ico', format='ICO')

# Also save as PNG for better browser support
favicon.save('hotel_booking/static/favicon.png', format='PNG')

print('Favicon created successfully!') 
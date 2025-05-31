# ST7789-Display-320x172.py
# Display BMP image from /images/ folder
# Demo of ST7789 320x172 rounded corner display purchased from Aliexpress.
import board
import displayio, busio
import digitalio
from displayio import FourWire
from adafruit_st7789 import ST7789

# Release any resources currently in use for the displays
displayio.release_displays()

# SPI setup
SCL = board.GP18   # Clock (SCK)
SDA = board.GP19   # Data (MOSI)
MISO = board.GP16  # Required by CircuitPython but unused

spi = busio.SPI(SCL, SDA, MISO)
tft_cs = board.GP20
tft_dc = board.GP21
tft_rst = board.GP15

# Backlight control
backlight = digitalio.DigitalInOut(board.GP22)
backlight.direction = digitalio.Direction.OUTPUT
backlight.value = True  # Turn on backlight

print("Backlight turned ON")

display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs, reset=tft_rst)

display = ST7789(display_bus,
                 width=320,
                 height=172,
                 rotation=90,
                 colstart=33)

print("Display initialized")

# Make the display context
splash = displayio.Group()
display.root_group = splash

# Load and display BMP image
try:
    # Change "your_image.bmp" to your actual filename
    bitmap = displayio.OnDiskBitmap("/images/make-something-awesome-small.bmp")
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=bitmap.pixel_shader)
    splash.append(tile_grid)
    print("Image loaded successfully")
except Exception as e:
    print(f"Error loading image: {e}")
    # Fallback - solid color if image fails
    color_bitmap = displayio.Bitmap(display.width, display.height, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = 0xFF0000  # Red to indicate error
    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    splash.append(bg_sprite)

while True:
    pass
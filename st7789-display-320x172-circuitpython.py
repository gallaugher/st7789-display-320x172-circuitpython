# ST7789-Display-320x172.py
# Should display a 5 pixel orange border (cut off slightly on edges by the curve of the display)
# with a purple rectangle in the center & centered text stating "ST7789".
# Demo of ST7789 320x172 rounded corner display purchased from Aliexpress.
# Note there's a chance you may need to tweak rotation and col state for your board
# since many manufacturers use different board offsets even for the same display standard.
import board
import displayio, busio, terminalio
import digitalio
from adafruit_display_text import label
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
                 colstart=33)    # Shift the display window down 33 pixels

print("Display initialized")

# Make the display context
splash = displayio.Group()
display.root_group = splash

# Purple border (full screen background)
border_bitmap = displayio.Bitmap(display.width, display.height, 1)
border_palette = displayio.Palette(1)
border_palette[0] = 0xFF8000  # Purple
border_sprite = displayio.TileGrid(border_bitmap, pixel_shader=border_palette, x=0, y=0)
splash.append(border_sprite)

# Lime green interior (5 pixel border)
interior_bitmap = displayio.Bitmap(display.width - 10, display.height - 10, 1)
interior_palette = displayio.Palette(1)
interior_palette[0] = 0x32CD32  # Lime green
interior_sprite = displayio.TileGrid(interior_bitmap, pixel_shader=interior_palette, x=5, y=5)
splash.append(interior_sprite)

# Black text "ST7789" in center
text_area = label.Label(
    terminalio.FONT,
    text="ST7789",
    color=0x000000,  # Black
    scale=3,
    anchor_point=(0.5, 0.5),
    anchored_position=(display.width // 2, display.height // 2),
)
splash.append(text_area)

print("Display test pattern loaded - Purple border, Lime interior, Black text")

while True:
    pass
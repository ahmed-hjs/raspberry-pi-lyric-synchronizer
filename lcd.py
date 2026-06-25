import smbus
import time

class LCD:
    def __init__(self, pi_rev = 2, i2c_addr = 0x3F, backlight = True):

        # device constants
        self.I2C_ADDR  = i2c_addr
        self.LCD_WIDTH = 16   # Max. characters per line

        self.LCD_CHR = 1 # Mode - Sending data
        self.LCD_CMD = 0 # Mode - Sending command

        self.LCD_LINE_1 = 0x80 # LCD RAM addr for line one
        self.LCD_LINE_2 = 0xC0 # LCD RAM addr for line two

        if backlight:
            self.LCD_BACKLIGHT  = 0x08
        else:
            self.LCD_BACKLIGHT = 0x00

        self.ENABLE = 0b00000100 # Enable bit

        self.E_PULSE = 0.0005
        self.E_DELAY = 0.0005

        if pi_rev == 2:
            self.bus = smbus.SMBus(1)
        elif pi_rev == 1:
            self.bus = smbus.SMBus(0)
        else:
            raise ValueError('pi_rev param must be 1 or 2')

        self.lcd_byte(0x33, self.LCD_CMD)
        self.lcd_byte(0x32, self.LCD_CMD)
        self.lcd_byte(0x06, self.LCD_CMD)
        self.lcd_byte(0x0C, self.LCD_CMD)
        self.lcd_byte(0x28, self.LCD_CMD)
        self.lcd_byte(0x01, self.LCD_CMD)

    def lcd_byte(self, bits, mode):
        bits_high = mode | (bits & 0xF0) | self.LCD_BACKLIGHT
        bits_low = mode | ((bits << 4) & 0xF0) | self.LCD_BACKLIGHT

        self.bus.write_byte(self.I2C_ADDR, bits_high)
        self.toggle_enable(bits_high)

        self.bus.write_byte(self.I2C_ADDR, bits_low)
        self.toggle_enable(bits_low)

    def toggle_enable(self, bits):
        time.sleep(self.E_DELAY)
        self.bus.write_byte(self.I2C_ADDR, (bits | self.ENABLE))
        time.sleep(self.E_PULSE)
        self.bus.write_byte(self.I2C_ADDR, (bits & ~self.ENABLE))
        time.sleep(self.E_DELAY)

    def message(self, string, line = 1):
        string = " " * ((16-len(string))//2) + string
        if line == 0:
            lcd_line = self.LCD_LINE_1
        elif line == 1:
            lcd_line = self.LCD_LINE_2


        string = string.ljust(self.LCD_WIDTH, " ")
        self.lcd_byte(lcd_line, self.LCD_CMD)

        for i in range(self.LCD_WIDTH):
            self.lcd_byte(ord(string[i]), self.LCD_CHR)


    def clear(self):
        self.lcd_byte(0x01, self.LCD_CMD)
        
    def message_align(self, string):
        words = string.split()

        n_pages = max(1,(len(string) + 15) // 16) #arrondi superieur
        target = len(string) / n_pages

        pages = []
        current = ""

        while words:
            word = words.pop(0)

            if not current:
                current = word
                continue

            candidate = current + " " + word

            if len(candidate) <= 16:
                current = candidate
            else:
                pages.append(current)
                current = word

        if current:
            pages.append(current)

        # Rebalance adjacent pages
        changed = True
        while changed:
            changed = False

            for i in range(len(pages) - 1):
                a = pages[i].split()
                b = pages[i + 1].split()

                if len(a) == 0 or len(b) == 0:
                    continue

                moved = a[-1]

                if len(" ".join(a[:-1])) <= 16 and len(" ".join([moved] + b)) <= 16:
                    old_diff = abs(len(pages[i]) - len(pages[i + 1]))
                    new_diff = abs(len(" ".join(a[:-1])) - len(" ".join([moved] + b)))

                    if new_diff < old_diff:
                        pages[i] = " ".join(a[:-1])
                        pages[i + 1] = " ".join([moved] + b)
                        changed = True

        return pages

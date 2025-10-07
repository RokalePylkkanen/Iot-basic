# Pico 2 W kytkettynä Joy-it pico protoilu lautaan. Buzzer GP27.
# Hälytys sireeni, jonka parametreja helppo muutta aloitusarvoissa.

from machine import Pin, PWM
from utime import sleep_ms

buzzerPin = Pin(27)
buzzer = PWM(buzzerPin)

# Asetetaan aloitusarvot
min_freq = 400   # Hz
max_freq = 2000  # Hz
step = 1        # Hz:n muutos per askel
delay = 2       # ms viive jokaisen askeleen välillä

buzzer.duty_u16(1000)  # Buzzer päälle (pieni arvo riittää)

while True:
    # Taajuus nousee
    for f in range(min_freq, max_freq, step):
        buzzer.freq(f)
        sleep_ms(delay)
    # Taajuus laskee
    for f in range(max_freq, min_freq, -step):
        buzzer.freq(f)
        sleep_ms(delay)
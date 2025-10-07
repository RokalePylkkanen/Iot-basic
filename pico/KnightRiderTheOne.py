# Pico 2 W kytkettynä Joy-it pico protoilulautaan.
# Ohjelma soittaa protolevyn kiinteällä buzzerilla (GP27) RitariÄssä tunnarin alkua. 
# Testasin koodia myöhemmin WOKWI simulaatorilla, mutta siinä ympäristössä EI oikein kuulostanut hyvältä.
# Joy-it laudalla toimii erittäin hyvin! Pitää testaa vielä jollain muulla buzzerilla.

from machine import Pin, PWM
from utime import sleep

buzzer = PWM(Pin(27))  

# Kromaattinen asteikko C4 → C6 (Hz)
notes = [
    261, 277, 293, 311, 329, 349, 369, 392,
    415, 440, 466, 493, 523, 554, 587, 622,
    659, 698, 740, 784, 830, 880, 932, 988,
    1047
]

# Melodian nuottien indeksit järjestyksessä notes listasta
melodyindex = [
    12, 13, 12, 12, 13, 12, 12, 13, 12,
    12, 12, 11, 12, 12, 12
]

duration = 0.12  # Kuudestoistaosanuotti about...

try:
    while True:       
        count1 = 0
        count2 = 0
        while count1 < 2:
            for note in melodyindex:
                if count2 < 1:
                    buzzer.freq(notes[note])
                    buzzer.duty_u16(32768)  # 50% teho
                    sleep(0.12)
                    buzzer.duty_u16(0)
                    sleep(0.12) # kuudestoistaosa tauko
                    count2 += 1
                    continue
                buzzer.freq(notes[note])
                buzzer.duty_u16(32768)
                sleep(duration )
                buzzer.duty_u16(0)
                sleep(0.01)
            count1 += 1
            count2 = 0
           
        count1 = 0
        count2 = 0
        while count1 < 2:
            for note in melodyindex:
                if count2 < 1:
                    buzzer.freq(notes[note - 2])
                    buzzer.duty_u16(32768)
                    sleep(0.12)
                    buzzer.duty_u16(0)
                    sleep(0.12)
                    count2 += 1
                    continue
                buzzer.freq(notes[note - 2])
                buzzer.duty_u16(32768)
                sleep(duration )
                buzzer.duty_u16(0)
                sleep(0.01)
            count1 += 1
            count2 = 0

except KeyboardInterrupt:
    buzzer.duty_u16(0)
    buzzer.deinit()
    Pin(27, Pin.OUT).value(0)  # pakotetaan LOW


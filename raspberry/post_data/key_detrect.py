import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM) 
channel = 17
GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)

if GPIO.input(channel):
    print('Input was HIGH')
else:
    print('Input was LOW')


def my_callback(channel):
    print('This is a edge event callback function!')
    print('Edge detected on channel %s'%channel)
GPIO.add_event_detect(channel, GPIO.RISING, callback=my_callback, bouncetime=300)

while(1):
    if(1==2):
        print(1)
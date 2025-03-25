#Include the library files
import time
import utime
import _thread
from machine import Pin, PWM
from ir_rx.print_error import print_error
from ir_rx.nec import NEC_8

#Define the IR receiver pin
pin_ir = Pin(15, Pin.IN)

#Define motors direction control pins
motor1 = Pin(2, Pin.OUT)
motor2 = Pin(3, Pin.OUT)
motor3 = Pin(4, Pin.OUT)
motor4 = Pin(5, Pin.OUT)

#Define Ultrasonic sensor pins
trigger = Pin(20, Pin.OUT)
echo = Pin(19, Pin.IN)

#Define LED pins
parking_sensor_led = Pin(17, Pin.OUT)
left_indicator = Pin(16, Pin.OUT)
right_indicator = Pin(27, Pin.OUT)
left_indicator2 = Pin(14, Pin.OUT)
right_indicator2 = Pin(0, Pin.OUT)
#Define motors speed control pins,
#set PWM frequency and max duty cycle
pwm1 = PWM(Pin(1))
pwm1.freq(1000)
pwm1.duty_u16(65535)

pwm2 = PWM(Pin(7))
pwm2.freq(1000)
pwm2.duty_u16(65535)

#Variable that holds current speed percenage
speed = 100

#Flag for turning parking sensor on/off
flag = True

#IR remote buttons description
#Values received from IR remote
fwd = 70 #move forward
rev = 21 #move backwards
stp = 64    #stop
lft = 68    #move left
rgt = 67   #move right
parking_sensor = 71 #enable/disable parking sensor
slow = 12 #change speed to 40% of max speed
medium = 24 #change speed to 60% of max speed
fast = 94 #change speed to 80% of max speed
max_speed = 22 #change speed to max speed
indicator_left = 8 #use left indicator
indicator_right = 28 #use right indicator

#LED toggle function
def toggle(t):
    parking_sensor_led.on()
    time.sleep(t)
    parking_sensor_led.off()
    time.sleep(t)
    

def indicator_toggle(pin1, pin2):
    for i in range(5):
        indicator1 = pin1
        indicator2 = pin2
        indicator1.on()
        indicator2.on()
        time.sleep(0.5)
        indicator1.off()
        indicator2.off()
        time.sleep(0.5)
    
    
#Direction control functions
def reverse():
    motor1.on()
    motor2.off()
    motor3.on()
    motor4.off()
    

def forward():
    motor1.off()
    motor2.on()
    motor3.off()
    motor4.on()


def right():
    motor1.on()
    motor2.off()
    motor3.off()
    motor4.on()


def left():
    motor1.off()
    motor2.on()
    motor3.on()
    motor4.off()


def stop():
    motor1.off()
    motor2.off()
    motor3.off()
    motor4.off()


#Getting ultrasonic sensor measurement
def ultra():
   #Generate ultrasonic signal
   #Clear trigger pin
   trigger.low()
   utime.sleep_us(2)
   
   #Set trigger pin to high for 5 us
   #(Send ultrasonic wave)
   trigger.high()
   utime.sleep_us(5)
   
   #Set pin back to low
   trigger.low()
   
   #Begin measurement when signal goes on
   while echo.value() == 0:
       #Get current time in us
       signaloff = utime.ticks_us()
   
   #End measurement when signal goes off
   while echo.value() == 1:
       #Get current time in us
       signalon = utime.ticks_us()
   
   #Calculate time that passed
   timepassed = signalon - signaloff
   
   #Calculate distance (in cm)
   distance = (timepassed * 0.0343) / 2

   return distance


#Receive and decode IR signal
def decodeKeyValue(data):
    return data
    
# User callback
def callback(data, addr, ctrl):
    if data < 0:  # NEC protocol sends repeat codes.
        pass
    else:
        if data == fwd: #forward 
            forward()
        if data == rev: #reverse
            reverse()
        if data == stp: #stop
            stop()
        if data == lft: #left
            left()
        if data == rgt: #right
            right()
        if data == parking_sensor: #turn on/off ultrasonic sensor
            global flag
            flag = False if flag is True else True
        if data == slow: #40% speed
            global speed
            speed = 40
            pwm1.duty_u16(65535*speed//100)
            pwm2.duty_u16(65535*speed//100)
        if data == medium: #60% speed
            global speed
            speed = 60
            pwm1.duty_u16(65535*speed//100)
            pwm2.duty_u16(65535*speed//100)
        if data == fast: #80% speed
            global speed
            speed = 80
            pwm1.duty_u16(65535*speed//100)
            pwm2.duty_u16(65535*speed//100)
        if data == max_speed: #max speed
            global speed
            speed = 100
            pwm1.duty_u16(65535)
            pwm2.duty_u16(65535)
        if data == indicator_left:
            _thread.start_new_thread(indicator_toggle, (left_indicator, left_indicator2))
            #indicator_toggle(left_indicator, left_indicator2)
        if data == indicator_right:
            _thread.start_new_thread(indicator_toggle, (right_indicator, right_indicator2))
                #indicator_toggle(right_indicator, right_indicator2)

# Instantiate receiver
ir = NEC_8(pin_ir, callback)

# Show debug information
ir.error_function(print_error)  
    
#Parking sensor loop
while True:
    if flag == True:
        distance = ultra()
        
        if distance < 40:
            stop()
            toggle(distance/80)
        


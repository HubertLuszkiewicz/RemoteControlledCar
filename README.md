# RemoteControlledCar

## About the project
**RemoteControlledCar** is a project coded in **MicroPython**, a lightweight version of **Python** designed for microcontrollers.

The aim of this project was to create a remote-controlled car by combining knowledge from electronics, programming and also
overall engineering.

<p align="center">
  <img src="car.jpg" alt="Alt text" width="400">
  <img src="car_top_view.jpg" alt="Alt text" width="400">
  
</p>

This repository contains code responsible for:
* **steering the car** (turning motors on and off)
* **controlling ultrasonic sensor** (parking sensor)
* **controlling LEDs** (car indicators)

These functionalities were achieved with help of library created by Peter Hinch which is available under MIT licence on GitHub: 
https://github.com/peterhinch/micropython_ir/tree/master/ir_rx

that was really helpful when it came to handling signals emited by infrared remote control.

## Schemes
<p align="center">
   <img src="electrical_scheme.png" alt="Alt text" width="700">
</p>

<p align="center">
  <img src="connection_scheme.png" alt="Alt text" width="700">  
</p>
  

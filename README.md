# psi-03

## Description

Uses Python's <code>requests</code> library to create requests to the APIs. Runs in a infinite loop. Works by first getting the ISS position and timestamp, then the coordinates are passed to the Sunrise Sunset API, where times of sunrise and sunset for the location are returned. 
Those times are then parsed into datetime. If the timestamp returned by the ISS Position API is between the sunrise and sunset, the ISS is on the sunny side of the earth. 
Otherwise it's on the dark side of earth. The optimal obervation times are then calculated by subtracting one and two hours from the sunrise and one and two hours to the sunset timestamp.
This creates two intervals of 1-2 hours before sunrise and after sunset. If the timestamp returned by the ISS Position API falls into one of these two itervals, the conditions are deemed optimal for observation.

## Usage

Run the <code>main.py</code> file in Python >= 3.8

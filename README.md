# psi-03

## Description

Uses Python's <code>requests</code> library to create requests to the APIs. Runs in a infinite loop. Works by first getting the ISS position and timestamp, then the coordinates are passed to 
the Sunrise Sunset API, where times of sunrise and sunset for the location are returned. Those times are then parsed into datetime and then into UTC timestamp. If the timestamp returned by the ISS Position API is between the sunrise and sunset, the ISS is on the sunny side of the earth. 
Otherwise it's on the dark side of earth. The optimal obervation times are then calculated by subtracting 7200 and 3600 seconds from the sunrise and adding 3600 and 7200 seconds to the sunset timestamp.
This created two intervals of 1-2 hours before sunrise and after sunset. If the timestamp returned by the ISS Position API falls into one of these two itervals, the conditions are deemed
optimal for observation.

## Usage

Run the <code>main.py</code> file in Python >= 3.8

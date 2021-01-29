# WLgenerator
Generates a wishlist from a runlist of cars, based on specific criteria



## Overview
This application takes a run list of cars that are going to auction, and then passes each vin number through an MMR calculator that is available on the internet to find out additional information about every car. This extra information is then used to rank the cars in terms of their potential return on investment. After the cars are ranked, they are filtered according to a set of predetermined criteria and sent to a MySQL database that is set up on a VPS.

The front end for this application is coded in swift and it allows the user to perform inspections on the pre-processed cars through their iPhone by accessing the MySQL database. Using this application will allow operations managers at smaller dealerships to better estimate the true value of a car without having to see it themselves in person. It is feasible to instead send a trusted employee that perhaps does not have the same level of experience in evaluating the potential value of a car.

The main goal of this application is to free up time for the operations manager by making the inspection process something that is more accessible to less skilled employees. 

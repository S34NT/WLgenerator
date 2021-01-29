# WLgenerator
Generates a wishlist from a runlist of cars, based on specific criteria



## Overview
This application takes a run list of cars that are going to auction, and then passes each vin number through an MMR calculator that is available on the internet to find out additional information about every car. This extra information is then used to rank the cars in terms of their potential return on investment. After the cars are ranked, they are filtered according to a set of predetermined criteria and sent to a MySQL database that I set up on a VPS. The front end for this application is coded in swift and it allows the user to perform inspections on the preprocessed cars through their iPhone by accessing the MySQL database. This way, employees can go to the auction and know which cars to inspect and the operations manager can review the inspections without ever having to go to the auction.

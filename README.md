# Weight Watchers

## Overview
During covid, it's become increasingly difficult to find weight lifting bumper plates available for sale. In particular, I keep finding the Ethos bumper plates at Dick's sporting goods store are always unavailable. While they have the 'notify me when available' email available, I was more interested in receiving a text message with a link to buy the actual item online.

To combat this, I made a fun little program to query for 25 and 35 pound plates (45's were removed as listing from the website at the time of creation).

The purpose of this was to be a fun little saturday night project which would result in the following
* me playing around with SNS being subscribed to by a mobile number
* result in me finally being able to purchase some more weight!

## How it Works
This program will take a json file of URLs for different size weight plates and
* hits the URL for that particular weight plate
* scans the HTML for the 'ship to me' availability message on the item
* if the item is available, it sends an SNS message with a link to buy the item

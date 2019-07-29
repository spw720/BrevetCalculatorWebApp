# Brevet time calculator.

Uses Docker + Flask + Javascript + AJAX + MongoDB + REST + AUTHO

Port 5002 for Calculator (Submit/Display/Clear) are database functionalities
Port 5001 for UI for listing content from DB in CSV or JSON format
Port 5000 for RESTful services. This includes an authentication feature where you can register a user, login a registered user, and logout a user. To expose API's, user must first be authenticated

Credits to Michal Young for the initial version of this code.

Adapted by Sean Wilson (swilso17@uoregon.edu) for CIS 322 at University of Oregon

6/7/2019

How the Algorithm Works - Both the open and close algorithms receive the control distance in kilometers, the nominal distance of the brevet and an ISO 8601 format date-time string indicating the official start time of the brevet. From this, the algorithms determine the optimal open and close times of the control stop along the brevet.

If the control is 0, the open time = start time, close time = start time + one hour

If control is longer than brevet, rule 9 is applied, seen here http://www.rusa.org/brvreg.html

Else, the standard algorithm is applied with the parameters.

An outline with examples of the algorithm can be found here https://rusa.org/pages/acp-brevet-control-times-calculator

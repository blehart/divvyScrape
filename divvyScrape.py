#!/usr/bin/python3.7

import glob
from bs4 import BeautifulSoup

def printTimeStats(title, seconds, trips):
    print(f'{title}: {seconds // 3600}h {seconds % 3600 // 60}m {seconds % 60}s, {trips} trips')

def printCostStats(seconds, trips, start, end):
    cost = 75
    days = 403
    costPerHour = cost / seconds * 3600
    costPerTrip = cost / trips
    costSoFar = (end - start) / 3600 / 24 / days * cost
    estimatedCostPerHour = costSoFar / seconds * 3600
    estimatedCostPerTrip = costSoFar / trips
    print('So Far: $%.2f/hr, $%.2f/trip'%(costPerHour, costPerTrip))
    print('Estimated Overall: $%.2f/hr, $%.2f/trip'%(estimatedCostPerHour, estimatedCostPerTrip))

def scrapeDivvy():
    totalSeconds = 0
    totalTrips = 0
    startDate = float('inf')
    endDate = float('-inf')
    for html in glob.glob('*.html'):
        with open(html) as page:
            soup = BeautifulSoup(page, 'html.parser')
            seconds = 0
            trips = 0
            for trip in soup.find_all('tr', class_='trip'):
                seconds += int(trip['data-duration-seconds'])
                trips += 1
                startDate = min(startDate, int(trip['data-start-timestamp']))
                endDate = max(endDate, int(trip['data-end-timestamp']))
    
            totalSeconds += seconds
            totalTrips += trips
            printTimeStats(html, seconds, trips)
    
    printTimeStats('Total', totalSeconds, totalTrips)
    printCostStats(totalSeconds, totalTrips, startDate, endDate)  

if __name__ == '__main__':
    scrapeDivvy()

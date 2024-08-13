import csv
import yfinance as yf
import ics
import pandas as pd
import arrow

csvFile = './watchlistExport.csv'

# Load the CSV file
with open(csvFile) as f:
    reader = csv.reader(f)
    data = [row for row in reader]
    stocks = data[1:]

# If CA: prefix is present, remove it and add .TO suffix
for i, stock in enumerate(stocks):
    if stock[1].startswith('CA:'):
        stocks[i][1] = stock[1][3:] + '.TO'

# Get earnings dates for each stock
for stock in stocks:
    ticker = yf.Ticker(stock[1])
    upcoming = ticker.get_earnings_dates(limit=4)
    upcoming = upcoming.reset_index()
    upcoming = upcoming[['Earnings Date']]
    # put earnings dates in normal list
    upcoming = upcoming['Earnings Date'].tolist()
    # convert to arrow objects
    upcoming = [arrow.get(date) for date in upcoming]
    stock.append(upcoming)

# Create a new calendar events for all earnings dates
cal = ics.Calendar()
for stock in stocks:
    name = stock[0] + ' Quarterly Earnings Release'
    for date in stock[3]:
        cal.events.add(ics.Event(name, begin=date))

# Save the calendar to a file
calFile = './earnings.ics'
with open(calFile, 'w') as f:
    f.writelines(cal)

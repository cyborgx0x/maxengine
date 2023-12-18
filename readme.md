F Engine - Backtesting And Trading Library for Python

Accept Dataframe

Features (on develope):

    - Backtesting
    - Trade backward and forward
    - Support TA-lib
    - Support Screening and backtest for screening

Definition:

- Strategy: A defined class that contain action after combine some indicators. "The term investment strategy refers to a set of principles designed to help an individual investor achieve their financial and investment goals."
- Indicator: Indicators are statistics used to measure current conditions as well as to forecast financial or economic trends. In the world of investing, indicators typically refer to technical chart patterns deriving from the price, volume, or open interest of a given security.
- TA: A library of indicators

## Engine

The Engine will process and maintain several trading strategies. Based on each strategy, it will get the signal, apply the filter. If the signal pass the filter, it will execute the trade.

- Fake Server: Handle the Request, Manage the Account, Keep the account history. 
- Time Machine: Create a time simulator. This can provide way to connect with other kind of event.

How it Work?
By letting the fake server and client to the same time, both of them now have the same price data. No need to loop over the price data. 


## Problem

I want to address the problem of generating ideas and selecting new trade to execute.

Typically, If you want to have new trade, you want to filter the price from several filters, such as: 

- Indicator
- Visualizing by chart
- Available capital
- The current Economic Situation

By doing so, you limit yourself from untested prediction. 

There are some common errors that you should avoid

- You may apply the filter the wrong way => Result in putting wrong position

For example. By including the Risk:Reward Ratio to your filter. 

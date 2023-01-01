F Engine - Backtesting And Trading Library for Python

Accept Dataframe

Features:

    - Backtesting
    - Trade backward and forward
    - Support TA-lib
    - Support Screening and backtest for screening

Definition:

- Strategy: A defined class that contain action after combine some indicators. "The term investment strategy refers to a set of principles designed to help an individual investor achieve their financial and investment goals."
- Indicator: Indicators are statistics used to measure current conditions as well as to forecast financial or economic trends. In the world of investing, indicators typically refer to technical chart patterns deriving from the price, volume, or open interest of a given security.
- TA: A library of indicators
- Engine: Automatic Apply a set of stratefies and send order to server.
- Fake Server: Handle the Request, Manage the Account, Keep the account history. The Price data of fake server and client can be different. 


How it Work?
By letting the fake server and client to the same time, both of them now have the same price data. No need to loop over the price data. 

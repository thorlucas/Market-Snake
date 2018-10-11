# Market Snake

## Overview

This Python library is designed easily script stock market indicators and alerts.

Indicators such as the MACD can provide insight into the trends the market is
taking. However, these changes can occur quickly, and they are often missed
if you are not paying attention to the market. Alerts help you quickly send
out messages so you won't miss a thing.

You can also easily script your own indicators and alerts.

This library is still in early development. It currently uses the free
AlphaVantage API to fetch price data, and indicators are calculated on top of
this data. Alerts can currently be sent by email.

# Getting Started

## Configuration

The `config.ini` file is used to store your api keys, passwords, and other data.
Make a copy of `config_example.ini` and rename it to `config.ini`.

While learning, you may want to turn `TEST_MODE` on. This uses AAPL stock at
5 minute intervals in order to avoid spamming AlphaVantage with API calls.

## Creating An AlphaVantage Instance

Currently, only the [AlphaVantage](https://www.alphavantage.co) web API is used to fetch stock market data.
Luckily, an AlphaVantage API Key is **free** and requires only your email address.
First, make sure to [get an API key from AlphaVantage](https://www.alphavantage.co/support/#api-key).
Then, add your key to the config file.

To create the AlphaVantage instance, simply pass in the name of the config file.

```python
import marketwatch.data.alphavantage as alphavantage
av = alphavantage.AlphaVantage('config.ini')
```

## Fetching Market Data

Next we have to fetch time series data from AlphaVantage. A time series
is simply a collection of data (like prices) with an associated timestamp.
Market Snake's time series classes provide of useful features, such as
fetching by timestamp or by index, performing arithmetic between two
time series, or even combining several series into one compound series.

For Open, High, Low, Close, Volume data, we use the `PriceTimeSeries` class.
This class stores a sorted collection of `PricePeriod` objects. These
are defined in `marketwatch.core`

The `AlphaVantage` class can automatically return `PriceTimeSeries` for us.
Currently, only Intraday series are available.

```python
...
timeSeries = av.Intraday('AAPL', 5)
```

This fetches the last 100 data points from AAPL at 5 minute intervals.
You can `print(timeSeries)`, but the output is not yet quite so beautiful.

## Using Indicators

We can use this time series data and calculate several indicators on top
of this. Let's try the Exponential Moving Average (EMA).
The `EMATimeSeries` and `EMAPeriod` classes are defined in `marketwatch.indicators.EMA`.

We will pass the time series data into a class method, as well as the
period to calculate the EMA on.

```python
import marketwatch.indicators.EMA as EMA
...
ema26 = EMA.EMATimeSeries.fromTimeSeries(timeSeries, 26)
```

Tada! Let's perform arithemetic between two EMAs.

```python
ema26 = ...
ema12 = EMA.EMATimeSeries.fromTimeSeries(timeSeries, 12)
base = ema12 - ema26
```

We can also perform EMAs ontop of other EMAs. In this case, we have to
pass in a lambda function that acts as a key to tell the EMA which
value to use. The default value for this key is `lambda p: p.close`, which
uses the closing price of a `PricePeriod` to calculate the EMA.

```python
signal = EMA.EMATimeSeries.fromTimeSeries(base, 9, key = lambda p: p.ema)
```

That's essentially how a MACD is calculated, and indeed that's what the
compound time series `MACDTimeSeries` does. To achieve the same thing,
we could have written

```python
import marketwatch.indicators.MACD as MACD
m = MACD.MACDTimeSeries.fromTimeSeries(timeSeries, 26, 12, 9)

print(m.base)
print(m.signal)
```

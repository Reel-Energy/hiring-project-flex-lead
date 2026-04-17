import pandas as pd

from helpers.data import get_forecasts, get_spot_price


def make_day_ahead_bids(
    sell: pd.DataFrame,
    buy: pd.DataFrame,
) -> pd.DataFrame:
    """Simple function to turn buy and sell timeseries into a bid matrix.

    :param sell: pandas dataframe with one column per sell order. The column name is the minimum price
        we want to sell that volume for.
    :param buy: pandas dataframe with one column per buy order. The column name is the maximum price
        we want to buy that volume for.
    :return: pandas dataframe with bids
    """

    # we sell nothing below min_sell_price
    sell[sell.columns.min() - 0.01] = 0
    # cumulate volume
    sell = sell.sort_index(axis=1, ascending=True).cumsum(axis=1)

    # we buy nothing above max_buy_price
    buy[buy.columns.max() + 0.01] = 0
    buy = buy.sort_index(axis=1, ascending=False).cumsum(axis=1)

    price_levels = sorted(sell.columns.tolist() + buy.columns.tolist())
    # we buy the same volume for any price below a given level expressed in the columns
    buy = buy.reindex(price_levels, axis=1).bfill(axis=1).fillna(0)
    # we sell the same volume for any price above a given level expressed in the columns
    sell = sell.reindex(price_levels, axis=1).bfill(axis=1).fillna(0)

    bids = sell.abs() - buy.abs()
    bids.columns = bids.columns.round(2)
    return bids


def example():
    """Simple example to illustrate how to create bids.
    We get the solar forecast for today, rescale it a bit to have a realistic level.
    We then decide to charge in the 8 lowest priced settlement periods and discharge in the highest.
    Note: this is clearly not a realistic strategy as we are assuming perfect foresight of prices
    and completely ignoring state of charge.
    """
    today = pd.Timestamp("now", tz="CET").normalize()
    date_range = pd.date_range(
        start=today, end=today + pd.DateOffset(days=1), freq="15min", inclusive="left"
    )

    forecast = (
        get_forecasts(
            time_from=date_range[0],
            time_to=date_range[-1] + pd.Timedelta("1h"),
            price_area="DK1",
            forecast_type="Solar",
        )
        .set_index("Minutes5UTC")["ForecastDayAhead"]
        .resample("15min")
        .mean()
        .reindex(date_range)
        .fillna(0)
        / 2000  # rescale
        * 100
    ).clip(upper=100)
    spot = get_spot_price(
        time_from=date_range[0],
        time_to=date_range[-1] + pd.Timedelta("1h"),
        price_area="DK1",
    ).set_index("TimeUTC")["DayAheadPriceEUR"]

    # we discharge in the highest 8 settlement periods
    discharge_threshold = spot.nlargest(8).min()
    charge_threshold = spot.nsmallest(8).max()
    bess_discharge = (spot >= discharge_threshold) * 50
    # we charge in the lowest 8 settlement periods
    bess_charge = (spot <= charge_threshold) * 50
    # we sell the forecasted solar production for a minimum of 1.5 EUR
    sell = pd.DataFrame({1.5: forecast, discharge_threshold: bess_discharge})
    buy = pd.DataFrame({charge_threshold: bess_charge})
    bids = make_day_ahead_bids(sell, buy)

    print(bids)


if __name__ == "__main__":
    example()

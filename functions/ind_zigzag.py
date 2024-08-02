import pandas as pd

def calculate_zigzag(data, deviation_percent, pivot_legs):
    times = []
    prices = []
    trends = []  
    last_pivot_index = 0
    last_pivot_price = data['Low'][0]
    trend = 0
    retraces = []  # Initialise with None for the first two entries to align with retracement calculation

    for i in range(pivot_legs, len(data) - pivot_legs):
        high = data['High'][i]
        low = data['Low'][i]
        time = data.index[i]

        if high >= last_pivot_price * (1 + deviation_percent / 100):
            if all(high >= data['High'][j] for j in range(i - pivot_legs, i + pivot_legs + 1)):
                if trend == 1:
                    times[-1] = time
                    prices[-1] = high
                else:
                    times.append(time)
                    prices.append(high)
                    trends.append(1)
                    retraces.append(None)  # No retracement calculation for trend 1
                last_pivot_price = high
                last_pivot_index = i
                trend = 1

        if low <= last_pivot_price * (1 - deviation_percent / 100):
            if all(low <= data['Low'][j] for j in range(i - pivot_legs, i + pivot_legs + 1)):
                if trend == -1:
                    times[-1] = time
                    prices[-1] = low
                else:
                    times.append(time)
                    prices.append(low)
                    trends.append(-1)
                    # Calculate retracement for trend -1, ensure there are at least 3 prices to perform calculation
                    if len(prices) > 2:
                        retracement = (prices[-1] - prices[-2]) / (prices[-2] - prices[-3]) if prices[-2] != prices[-3] else None
                        retraces.append(retracement)
                    else:
                        retraces.append(None)
                last_pivot_price = low
                last_pivot_index = i
                trend = -1

    # Evaluate the remaining data for a potential pivot
    for i in range(last_pivot_index + 1, len(data)):
        high = data['High'][i]
        low = data['Low'][i]
        time = data.index[i]

        if trend == 1 and high >= last_pivot_price * (1 + deviation_percent / 100):
            times[-1] = time
            prices[-1] = high
            last_pivot_price = high
        elif trend == -1 and low <= last_pivot_price * (1 - deviation_percent / 100):
            times[-1] = time
            prices[-1] = low
            last_pivot_price = low 

    # Ensure all lists are of the same length
    
    # Convert to DataFrame
    zigzag_df = pd.DataFrame({'Time': times, 'Price': prices, 'Trends': trends, 'Retrace': retraces})

    # Calculate percentage change
    zigzag_df['Percentage Change'] = zigzag_df['Price'].pct_change() * 100

    return zigzag_df, retraces
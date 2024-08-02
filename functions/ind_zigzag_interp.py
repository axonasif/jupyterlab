import pandas as pd
import numpy as np

def zigzag_interp(data):
    n = len(data)
    zigzag_index = np.full(n, np.nan)

    # IsUp = 1; IsDown = 2
    for i in range(2, n):
        if data['Price'].iloc[i] < data['Price'].iloc[i-1] and data['Price'].iloc[i] > data['Price'].iloc[i-2]:
            zigzag_index[i] = 1
        elif data['Price'].iloc[i] < data['Price'].iloc[i-1] and data['Price'].iloc[i] < data['Price'].iloc[i-2]:
            zigzag_index[i] = 2

    # Join points continuously
    zigzag_interp = []
    for i in range(1, n-1):
        if zigzag_index[i-1] == 2 and np.isnan(zigzag_index[i]) and zigzag_index[i+1] == 1:
            zigzag_interp.append([data.index[i-1], data['Price'].iloc[i-1]])
        if zigzag_index[i-1] == 1 and np.isnan(zigzag_index[i]) and zigzag_index[i+1] == 2:
            zigzag_interp.append([data.index[i], data['Price'].iloc[i]])
    
    # Convert to DataFrame
    zigzag_interp_df = pd.DataFrame(zigzag_interp, columns=['Time', 'Price'])

    # Calculate percentage change
    zigzag_interp_df['Percentage Change'] = zigzag_interp_df['Price'].pct_change() * 100

    return zigzag_interp_df
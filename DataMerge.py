import pandas as pd
import numpy as np

# Load your data from CSV files
df1 = pd.read_csv("C:\\Users\\manan\\Download\\Magicbricks_maindata_Jul-23-24 - Sheet1 (2).csv")
df2 = pd.read_csv('C:\\Users\\manan\\Download\\Magicbricks_maindata_Jul-23-24 - Sheet2.csv')


# Forward fill the Locality column in both DataFrames
df1['Locality'] = df1['Locality'].replace('', np.nan).ffill()
df2['Locality'] = df2['Locality'].replace('', np.nan).ffill()



# Combine the two DataFrames
combined_df = pd.concat([df1, df2], ignore_index=True)

# Function to convert Quarter to datetime for sorting
def convert_quarter_to_date(quarter_str):
    if pd.isna(quarter_str) or not isinstance(quarter_str, str):
        return pd.NaT  # Return Not a Time for NaN values
    
    if 'Jan' in quarter_str:
        month = 1
    elif 'Apr' in quarter_str:
        month = 4
    elif 'Jul' in quarter_str:
        month = 7
    elif 'Oct' in quarter_str:
        month = 10
    else:
        month = 10  # Adjust if you want to handle other cases

    year = int(quarter_str.split()[-1])
    return pd.Timestamp(year=year, month=month, day=1)

# Apply the conversion function to create a new column for sorting
combined_df['Quarter_Date'] = combined_df['Quarter'].apply(convert_quarter_to_date)

# Sort the DataFrame by the new Quarter Date column in descending order
combined_df_sorted = combined_df.sort_values(by='Quarter_Date', ascending=False)

# Rearrange the DataFrame to have each locality's current quarter followed by the previous quarter
final_df = pd.DataFrame()

for locality in combined_df_sorted['Locality'].unique():
    locality_data = combined_df_sorted[combined_df_sorted['Locality'] == locality]
    final_df = pd.concat([final_df, locality_data], ignore_index=True)

# Reset index
final_df.reset_index(drop=True, inplace=True)

# Drop the Quarter_Date column (optional) but keep the Quarter column
final_df.drop(columns='Quarter_Date', inplace=True)

# Display the final rearranged DataFrame
print(final_df)

final_df.to_csv('C:\\Users\\manan\\Download\\final_property_data.csv', index=False)






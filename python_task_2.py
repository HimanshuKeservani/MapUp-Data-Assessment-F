#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


def calculate_distance_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame): Dataset with 'id_1', 'id_2', and 'distance' columns.

    Returns:
        pandas.DataFrame: Distance matrix
    """

    # Create a pivot table with distances as values and ids as indexes and columns
    distance_matrix = df.pivot_table(index="id_1", columns="id_2", values="distance", fill_value=0)

    # Make the matrix symmetric
    for i in distance_matrix.index:
        for j in distance_matrix.index:
            if i != j and distance_matrix.loc[i, j] == 0:
                distance_matrix.loc[i, j] = distance_matrix.loc[j, i]

    # Set diagonal values to 0
    np.fill_diagonal(distance_matrix.values, 0)

    return distance_matrix


# In[3]:


def unroll_distance_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame): Distance matrix with ID pairs and distances.

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """

    # Get all unique pairs of IDs
    id_pairs = df.stack().index.to_frame().reset_index()

    # Rename columns to match the desired output
    id_pairs.rename(columns={"level_1": "id_start", "level_2": "id_end"}, inplace=True)

    # Merge with the original DataFrame to get the distances
    unrolled_df = id_pairs.merge(df, on=["id_start", "id_end"], how="left")

    # Filter out duplicate rows where id_start and id_end are the same
    unrolled_df = unrolled_df[unrolled_df["id_start"] != unrolled_df["id_end"]]

    return unrolled_df


# In[4]:


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here

    return df


# In[5]:


def calculate_toll_rate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame): Unrolled distance matrix with 'id_start', 'id_end', and 'distance' columns.

    Returns:
        pandas.DataFrame: DataFrame with additional columns for each vehicle type and their toll rates.
    """

    # Define rate coefficients for each vehicle type
    rate_coefficients = {
        "moto": 0.8,
        "car": 1.2,
        "rv": 1.5,
        "bus": 2.2,
        "truck": 3.6,
    }

    # Create new columns for each vehicle type and calculate toll rates
    for vehicle_type, rate_coefficient in rate_coefficients.items():
        df[vehicle_type] = df["distance"] * rate_coefficient

    return df


# In[6]:


from datetime import datetime, timedelta

import pandas as pd


def calculate_time_based_toll_rates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame): Unrolled distance matrix with 'id_start', 'id_end', and 'distance' columns.

    Returns:
        pandas.DataFrame: DataFrame with additional columns for time information and time-adjusted toll rates.
    """

    # Define time intervals and discount factors
    weekdays_discounts = {
        (pd.Timedelta("00:00:00"), pd.Timedelta("10:00:00")): 0.8,
        (pd.Timedelta("10:00:00"), pd.Timedelta("18:00:00")): 1.2,
        (pd.Timedelta("18:00:00"), pd.Timedelta("24:00:00")): 0.8,
    }
    weekends_discount = 0.7

    # Define helper functions
    def get_day_name(date):
        return date.strftime("%A")

    def calculate_time_interval(start_time, end_time):
        current_time = start_time
        while current_time <= end_time:
            for interval, discount in weekdays_discounts.items():
                if interval[0] <= current_time < interval[1]:
                    yield current_time, discount
                    break
            else:
                yield current_time, weekends_discount
            current_time += timedelta(minutes=30)

    # Generate time information and apply discounts
    for index, row in df.iterrows():
        # Calculate start and end dates for a full 24-hour period
        start_date = datetime.strptime(row["startDay"], "%Y-%m-%d")
        end_date = start_date + timedelta(days=1)

        # Generate start and end times with 30-minute intervals
        start_time = datetime.strptime(row["startTime"], "%H:%M:%S").time()
        end_time = datetime.strptime(row["endTime"], "%H:%M:%S").time()

        # Add time information and calculate discounted toll rates
        for current_time, discount in calculate_time_interval(start_time, end_time):
            new_row = {
                "id_start": row["id_start"],
                "id_end": row["id_end"],
                "distance": row["distance"],
                "start_day": get_day_name(start_date + timedelta(days=current_time.days)),
                "start_time": current_time,
                "end_day": get_day_name(end_date + timedelta(days=current_time.days)),
                "end_time": current_time + timedelta(minutes=30),
            }
            for vehicle_type in df.filter(like="^moto|^car|^rv|^bus|^truck"):
                new_row[vehicle_type] = row[vehicle_type] * row["distance"] * discount
            df.loc[index + 1] = new_row
        df.drop(index=index, inplace=True)

    return df


# In[ ]:





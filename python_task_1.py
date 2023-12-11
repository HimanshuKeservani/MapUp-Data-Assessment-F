#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


def generate_car_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Creates a DataFrame for id combinations.

    Args:
        df (pandas.DataFrame): Dataset with 'id_1', 'id_2', and 'car' columns.

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values,
                            where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    matrix = df.pivot_table(index='id_1', columns='id_2', values='car', fill_value=0)
    # Set diagonal values to 0
    np.fill_diagonal(matrix.values, 0)
    return matrix


# In[3]:


def get_type_count(df: pd.DataFrame) -> dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame): Dataset with 'car' column.

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Define value thresholds for each type
    low_threshold = 15
    medium_threshold = 25

    # Define classification function based on thresholds
    def classify_car_type(car_value):
        if car_value <= low_threshold:
            return "low"
        elif low_threshold < car_value <= medium_threshold:
            return "medium"
        else:
            return "high"

    # Add new categorical column with car types
    df["car_type"] = df["car"].apply(classify_car_type)

    # Calculate the count of occurrences for each car type
    type_counts = df["car_type"].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    return dict(sorted(type_counts.items()))


# In[4]:


def get_bus_indexes(df: pd.DataFrame) -> list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame): Dataset with 'bus' column.

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """

    # Calculate the mean of the 'bus' column
    bus_mean = df["bus"].mean()

    # Filter indices where 'bus' values are greater than twice the mean
    bus_indexes = df[df["bus"] > 2 * bus_mean].index.tolist()

    # Sort the filtered indexes in ascending order
    bus_indexes.sort()

    return bus_indexes


# In[5]:


def filter_routes(df: pd.DataFrame) -> list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """

    # Calculate average 'truck' values per route
    avg_truck_per_route = df.groupby("route")["truck"].mean()

    # Filter routes with avg truck value > 7
    filtered_routes = avg_truck_per_route[avg_truck_per_route > 7].index.tolist()

    # Sort the filtered routes
    filtered_routes.sort()

    return filtered_routes


# In[6]:


def multiply_matrix(matrix: pd.DataFrame) -> pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """

    # Define thresholds for multiplication factors
    threshold = 20

    # Define a function to apply multiplication based on conditions
    def multiply_value(value):
        if value > threshold:
            return value * 0.75
        else:
            return value * 1.25

    # Apply the multiplication function to each value in the matrix
    modified_matrix = matrix.applymap(multiply_value)

    # Round values to 1 decimal place
    modified_matrix = modified_matrix.round(1)

    return modified_matrix


# In[7]:


from datetime import timedelta

def time_check(df: pd.DataFrame) -> pd.Series:
    """
    Verifies if timestamps for each unique (id, id_2) pair cover 24 hours and 7 days.

    Args:
        df (pandas.DataFrame): Dataset with 'id', 'id_2', 'startDay', 'startTime', 'endDay', and 'endTime' columns.

    Returns:
        pd.Series: Boolean series with multi-index (id, id_2) indicating incorrect timestamps.
    """

    def check_time_range(row):
        """
        Helper function to check if a single row has valid timestamps.

        Args:
            row (pandas.Series): A row from the DataFrame.

        Returns:
            bool: True if timestamps are valid, False otherwise.
        """

        # Combine start and end times into datetime objects
        start_time = pd.to_datetime(row[["startDay", "startTime"]])
        end_time = pd.to_datetime(row[["endDay", "endTime"]])

        # Calculate duration
        duration = end_time - start_time

        # Check if duration covers 24 hours and 7 days
        return duration >= timedelta(days=7) and duration >= timedelta(hours=24)

    # Apply the check_time_range function to each row
    is_valid_time = df.apply(check_time_range, axis=1)

    # Set the multi-index based on 'id' and 'id_2' columns
    is_valid_time.index = pd.MultiIndex.from_tuples(df[["id", "id_2"]].values)

    return is_valid_time


# In[ ]:





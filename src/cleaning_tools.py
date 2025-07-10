import re

import pandas as pd


def clear_trailing_spaces(df):
    """
    Description: Removes any trailing whitespaces in all columns of the dataframe

    Argument:
        df: Dataframe with columns containing trailing spaces

    Returns:
        df: Dataframe with columns having trailing spaces removed
    """

    for col in df.columns:
        try:
            df[col] = df[col].str.strip()
        except AttributeError:
            print(
                f"Column {col} is of the wrong data type, unable to remove trailing whitespaces"
            )
            continue
        except Exception as e:
            print(f"Error: {e}")

    return df


def standardize_lower_case(df):
    """
    Description: Converts the text strings in a dataframe to lower case

    Argument:
        df: Dataframe with columns containing values with inconsistent capitalisation

    Returns:
        df: Dataframe with columns containing values with lower case string texts
    """

    for col in df.columns:
        try:
            df[col] = df[col].str.lower()
        except AttributeError:
            print(
                f"Column {col} is of the wrong data type, unable to convert to lower case"
            )
            continue
        except Exception as e:
            print(f"Error: {e}")

    return df


def remove_characters(df, col, *args):
    """
    Description: Removes specified unwanted characters from a column of a dataframe

    Argument:
        df: Pandas dataframe
        col: Column in the dataframe containing values with unnecessary characters
        *args: Characters or substrings to remove from the column (special characters handled safely)

    Returns:
        df: Pandas dataframe with the specified characters removed from the column
    """
    try:
        df[col] = df[col].astype(str)
        for arg in args:
            escaped_arg = re.escape(arg)
            df[col] = df[col].str.replace(escaped_arg, "", regex=True)
    except Exception as e:
        print(f"Error: {e}")
    return df


def has_mental_health_concerns(value):
    """
    Converts mental health status to binary values:

    0 = No concerns
    1 = Has concerns
    """
    if pd.isna(value):
        return 0

    no_concern = [
        "good",
        "goood",
        "goo",
        "god",
        "fair",
        "fiar",
        "faire",
        "excellent",
        "excellnt",
    ]
    return 0 if any(rating in value for rating in no_concern) else 1


def impute_by_grouped_median(df, col_to_impute, *groupby_col):
    """
    Description: Imputes missing values in a column of a dataframe by median values of each grouped category (in-place)

    Argument:
        df: Pandas dataframe
        col_to_impute: Column with missing values which would be imputed
        *groupby_col: Columns to group a dataframe by to find the median value to impute missing values with

    Returns:
        None (modifies dataframe in-place)
    """

    try:
        # Impute using median values based on each group and subgroup
        df[col_to_impute] = df.groupby(list(groupby_col), observed=True)[
            col_to_impute
        ].transform(lambda x: x.fillna(x.median()))

        # Fallback using columns's overall median if group combination has no valid data
        remaining_missing = df[col_to_impute].isnull().sum()
        proportion_missing = round(remaining_missing / len(df) * 100, 2)

        if remaining_missing > 0:
            overall_median = df[col_to_impute].median()
            df[col_to_impute] = df[col_to_impute].fillna(overall_median)
            print(
                f"No valid data found in groupby combination. Applied overall median as fallback for {col_to_impute} : ({remaining_missing} records, {proportion_missing}%)"
            )

    except Exception as e:
        print(f"Error imputing {col_to_impute}: {str(e)}")

def filter_immediate_stopgain(input_df):
    """
    Function to remove rows with 'immediate-stopgain' and their preceding rows.
    """
    # Create a copy
    filtered_df = input_df.copy()

    for index, row in filtered_df.iterrows():
        if row["Mutation Type"] == "immediate-stopgain":
            filtered_df.drop(index, inplace=True)
            filtered_df.drop(index - 1, inplace=True)

    # Reset the index of the modified DataFrame
    filtered_df.reset_index(drop=True, inplace=True)

    return filtered_df

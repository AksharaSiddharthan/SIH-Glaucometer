import pandas as pd
import numpy as np

def process_patient_data(file_name):
    """
    Loads patient data from an XLSX file, processes it, and saves the corrected data to a new CSV file.

    Args:
        file_name (str): The name of the input XLSX file.
    """
    try:
        # Load the dataset from an XLSX file
        df = pd.read_csv(file_name)
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")
        print("Please ensure the file is in the same folder as this script.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    # --- IMPORTANT: Update this dictionary with the exact column names from your XLSX file ---
    column_mapping = {
        'age': 'Age',
        'gender': 'Gender',
        'iop_pneumatic': 'Pneumatic',
        'iop_perkins': 'Perkins',
        'pachymetry': 'Pachymetry',
        'axial_length': 'Axial_Length'
    }
    
    missing_cols = [v for k, v in column_mapping.items() if v not in df.columns]
    if missing_cols:
        print("Error: The following required columns were not found in your file:")
        print(missing_cols)
        print("\nPlease update the `column_mapping` dictionary with the correct names.")
        return

    # --- Step 1: Process IOP values ---
    df['IOP'] = np.nan
    
    both_present = df[column_mapping['iop_pneumatic']].notna() & df[column_mapping['iop_perkins']].notna()
    df.loc[both_present, 'IOP'] = (df.loc[both_present, column_mapping['iop_pneumatic']] + df.loc[both_present, column_mapping['iop_perkins']]) / 2
    
    pneumatic_only = df[column_mapping['iop_pneumatic']].notna() & df[column_mapping['iop_perkins']].isna()
    df.loc[pneumatic_only, 'IOP'] = df.loc[pneumatic_only, column_mapping['iop_pneumatic']]
    
    # Filter out rows where IOP could not be calculated
    df = df[df['IOP'].notna()]

    # Filter out rows with null values in Age, Gender, or Cornea Thickness
    initial_rows = len(df)
    df.dropna(subset=[column_mapping['age'], column_mapping['gender'], column_mapping['pachymetry']], inplace=True)
    rows_removed = initial_rows - len(df)
    print(f"\n{rows_removed} rows were removed due to missing Age, Gender, or Cornea Thickness values.")

    # --- Step 2: Select and rename columns for the final dataset ---
    processed_df = df.copy()[[
        column_mapping['age'],
        column_mapping['gender'],
        column_mapping['pachymetry'],
        'IOP',
        column_mapping['axial_length']
    ]]
    
    processed_df.rename(columns={
        column_mapping['pachymetry']: 'Cornea Thickness'
    }, inplace=True)

    # --- Step 3: Save the processed data as a CSV file ---
    output_file_name = "full_dataset_cleaned.csv"
    processed_df.to_csv(output_file_name, index=False)
    
    print("\nData processing complete! ")
    print(f"A new file named '{output_file_name}' has been created with the corrected data.")
    print("\nHere's a preview of the processed data:")
    print(processed_df.head())


# Run the function with your file name
# Note: Ensure you provide the name of the .xlsx file here
file_to_process = "full_patient_dataset.csv"
process_patient_data(file_to_process)
import pandas as pd

def get_google_sheet():
    sheet_id='1deLM8E8weSnd4nbK1byV8TSlUkWuy7dqwmSfHgmneiw'
    df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
    df_headers = list(df.columns)
    
    return df,df_headers

import pandas as pd

def get_google_sheet():
    sheet_id='1deLM8E8weSnd4nbK1byV8TSlUkWuy7dqwmSfHgmneiw'
    df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
    df_headers = list(df.columns)
    
    return df,df_headers


def search_filter(df,df_headers,search):
    Filter=[]
    for header in df_headers:
        if df[header].dtypes=="int64":
            df[header] = df[header].values.astype(str)
        new=df[df[header].str.contains(search)]
        new1=[{i:new.iloc[i].to_dict()} for i in range(len(new))]
        Filter.append(new1)
    adict={}    
    for i in Filter:
        for j,k in enumerate(i):
            adict[j]=k[j]
    query=[]        
    for i in adict.values():
        query.append(i)
        
    return query

import pandas as pd


def get_google_sheet():
    sheet_id = "1deLM8E8weSnd4nbK1byV8TSlUkWuy7dqwmSfHgmneiw"
    df = pd.read_csv(
        f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    )
    df_headers = list(df.columns)

    return df, df_headers


def search_filter(df, df_headers, search):
    # Αναζήτηση σε κάθε column για τη λέξη-κλειδί(search),
    # παίρνουμε τη row που υπάρχει η λέξη-κλειδί,
    # Προσοχή υπάρχουν διπλοεγγραφές
    filter = []
    for header in df_headers:
        if df[header].dtypes == "int64":
            df[header] = df[header].values.astype(str)

        new = df[df[header].str.contains(search)]
        new1 = [{i: new.iloc[i].to_dict()} for i in range(len(new))]
        filter.append(new1)

    # Μετά την αναζήτηση str.contains η λίστα filter έχει διπλοεγγραφές,
    # τα μεταφέρουμε σε ένα λεξικό για αποφυγή διπλοεγγραφών,
    # ώστε να λάβουμε μία φορά τη row από το Dataframe.
    adict = {}
    for i in filter:
        for j, k in enumerate(i):
            adict[j] = k[j]

    # Τελική μορφή για να διαβιβαστούν στο front-end
    query = [value for value in adict.values()]

    return query

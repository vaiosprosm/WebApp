from flask import (Blueprint,render_template,request,)
from flask_login import login_required
import numpy as np
from natsort import index_natsorted
from WebApp.home import components as comp


home = Blueprint('home', __name__)



@home.route("/",methods=["GET"])
@home.route("/home",methods=["GET"])
@login_required
def root():
    df,df_headers = comp.get_google_sheet()
    
    dataframe=[df.iloc[i].to_dict() for i in range(len(df))]
    df_headers = list(df.columns)
  
    return render_template("home/index.html",dataframe=dataframe,df_headers=df_headers,datalist_options=df)


@home.route("/home/filter/<column>",methods=["GET"])
@login_required
def filter(column):
    start_with=request.args.get("startWith")
    
    df,df_headers = comp.get_google_sheet()
    
    if df[column].dtypes=="int64":
        df[column] = df[column].values.astype(str)
        
    new_df=df[df[column].str.startswith(start_with)]  
    dataframe=[new_df.iloc[i].to_dict() for i in range(len(new_df))]
    
    return render_template("home/index.html",dataframe=dataframe,df_headers=df_headers,datalist_options=df)


@home.route("/home/taksinomisi_by/<column>",methods=["GET"])
@login_required
def taksinomisi_by(column):
    df,df_headers = comp.get_google_sheet()
    
    new_df=df.sort_values(
    by=column,
    key=lambda x: np.argsort(index_natsorted(df[column]))
    )
    
    dataframe=[new_df.iloc[i].to_dict() for i in range(len(new_df))]
    
    return render_template("home/index.html",dataframe=dataframe,df_headers=df_headers,datalist_options=df)








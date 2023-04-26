from flask import (Blueprint,render_template,
                   redirect,
                   url_for,
                   request,
                   flash, abort,
                   jsonify)


from WebApp import app, db
from flask_login import login_required
import pandas as pd


home = Blueprint('home', __name__)


@home.route("/",methods=["GET"])
@home.route("/home",methods=["GET"])
@login_required
def root():
    sheet_id='1deLM8E8weSnd4nbK1byV8TSlUkWuy7dqwmSfHgmneiw'
    df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
    shape_df = df.shape    
    dataframe=[df.iloc[i].to_dict() for i in range(shape_df[0])]
    df_headers = list(df.columns)
  
    return render_template("home/index.html",dataframe=dataframe,df_headers=df_headers)



@home.route("/home/data",methods=["GET"])
@login_required
def home_data():
    sheet_id='1deLM8E8weSnd4nbK1byV8TSlUkWuy7dqwmSfHgmneiw'
    df = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv")
    shape_df = df.shape    
    dataframe=[df.iloc[i].to_dict() for i in range(shape_df[0])]
  
    return jsonify({"df":dataframe})
    




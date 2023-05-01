import json

import numpy as np
from flask import Blueprint, abort, render_template, request
from flask_login import login_required
from natsort import index_natsorted

from WebApp.home import components as comp

home = Blueprint("home", __name__)


@home.errorhandler(500)
def internal_server_error(e):
    return render_template("errors/500.html"), 500


@home.route("/")
@home.route("/home", methods=["GET"])
@login_required
def root():
    try:
        df, df_headers = comp.get_google_sheet()
        headers_th = [i for i in df_headers]
        print(df_headers)
    except:
        abort(500)

    return render_template(
        "home/index.html",
        title="Server-Driven Table",
        headers_th=headers_th,
        headers_th_javascript=json.dumps(headers_th),
    )


@home.route("/home/data")
@login_required
def data():
    df, df_headers = comp.get_google_sheet()

    query = [df.iloc[i].to_dict() for i in range(len(df))]
    len_query = len(query)
    df_headers = list(df.columns)

    # sorting
    i = 0
    while True:
        col_index = request.args.get(f"order[{i}][column]")
        col_name = request.args.get(f"columns[{col_index}][data]")
        descending = request.args.get(f"order[{i}][dir]") == "desc"

        if col_index is None:
            break

        if col_name not in df_headers:
            break

        if not descending:
            new_df = df.sort_values(
                by=col_name, key=lambda x: np.argsort(index_natsorted(df[col_name]))
            )
        else:
            new_df_desc = df.sort_values(
                by=col_name, key=lambda x: np.argsort(index_natsorted(df[col_name]))
            )
            new_df = new_df_desc.iloc[::-1]

        query = [new_df.iloc[i].to_dict() for i in range(len(new_df))]
        i += 1

    # filter
    search = request.args.get("search[value]")
    if search:
        query = comp.search_filter(df, df_headers, search)

    # pagination
    start = request.args.get("start", type=int)
    length = request.args.get("length", type=int)
    query = query[start : start + length]

    # response
    return {
        "data": query,
        "recordsFiltered": len_query,
        "recordsTotal": len_query,
        "draw": request.args.get("draw", type=int),
    }

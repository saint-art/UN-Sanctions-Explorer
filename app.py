from flask import Flask
from flask import request
from flask import render_template
from flask import jsonify
from flask import make_response

import csv
import io
import re

from openpyxl import Workbook
from io import BytesIO
from database import (
    search_persons,
    export_search_results,
    get_top_nationalities,
    get_dashboard_stats,
    get_person,
    get_aliases,
    get_passports,
    get_addresses,
    get_amendments
)

app = Flask(__name__)

@app.template_filter("highlight")
def highlight(text, search):

    if not text or not search:
        return text

    pattern = re.compile(
        re.escape(search),
        re.IGNORECASE
    )

    return pattern.sub(
        lambda m: f"<mark>{m.group(0)}</mark>",
        str(text)
    )


@app.route("/")
def home():

    search = request.args.get("search", "")

    field = request.args.get(
        "field",
        "all"
    )

    sort = request.args.get(
        "sort",
        "name"
    )

    page = request.args.get(
        "page",
        default=1,
        type=int
    )

    per_page = request.args.get(
        "per_page",
        default=10,
        type=int
    )

    results = []
    total = 0

    if search:

        results, total = search_persons(
            search=search,
            field=field,
            page=page,
            per_page=per_page,
            sort=sort
        )

    stats = get_dashboard_stats()

    pages = (total + per_page - 1) // per_page

    return render_template(

        "index.html",

        search=search,

        field=field,

        sort=sort,

        per_page=per_page,

        results=results,

        stats=stats,

        page=page,

        pages=pages,

        total=total

    )

@app.route("/dashboard")
def dashboard():

    stats = get_dashboard_stats()

    top_nationalities = get_top_nationalities()

    return render_template(
        "dashboard.html",
        stats=stats,
        top_nationalities=top_nationalities
    )

@app.route("/person/<sanction_id>")
def person_details(sanction_id):

    person = get_person(sanction_id)

    aliases = get_aliases(sanction_id)

    addresses = get_addresses(sanction_id)

    passports = get_passports(sanction_id)

    amendments = get_amendments(sanction_id)

    return render_template(
        "person.html",
        person=person,
        aliases=aliases,
        addresses=addresses,
        passports=passports,
        amendments=amendments
    )

@app.route("/api/search")
def api_search():

    search = request.args.get(
        "name",
        ""
    )

    rows, total = search_persons(search)

    results = []

    for row in rows:

        results.append({
            "sanction_id": row[0],
            "full_name": row[1],
            "nationality": row[2],
            "dob": row[3]
        })

    return jsonify(results)

@app.route("/api/dashboard")
def api_dashboard():

    stats = get_dashboard_stats()

    nationality_rows = get_top_nationalities()

    return jsonify({

        "stats": stats,

        "nationalities": [

            {
                "name": row[0],
                "count": row[1]
            }

            for row in nationality_rows

        ]

    })

@app.route("/export/csv")
def export_csv():

    search = request.args.get(
        "search",
        ""
    )

    field = request.args.get(
        "field",
        "all"
    )

    sort = request.args.get(
        "sort",
        "name"
    )

    rows = export_search_results(
        search=search,
        field=field,
        sort=sort
    )

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "Sanction ID",
        "Full Name",
        "Nationality",
        "Date of Birth"
    ])

    for row in rows:

        writer.writerow([
            row[0],
            row[1],
            row[2],
            row[3]
        ])

    response = make_response(output.getvalue())

    response.headers["Content-Disposition"] = (
        "attachment; filename=sanctions_export.csv"
    )

    response.headers["Content-Type"] = "text/csv"

    return response

@app.route("/export/excel")
def export_excel():

    search = request.args.get("search", "")

    field = request.args.get("field", "all")

    sort = request.args.get("sort", "name")

    rows = export_search_results(
        search=search,
        field=field,
        sort=sort
    )

    wb = Workbook()

    ws = wb.active

    ws.title = "Sanctions"

    ws.append([
        "Sanction ID",
        "Full Name",
        "Nationality",
        "Date of Birth"
    ])

    for row in rows:

        ws.append([
            row[0],
            row[1],
            row[2],
            row[3]
        ])

    output = BytesIO()

    wb.save(output)

    output.seek(0)

    response = make_response(output.getvalue())

    response.headers[
        "Content-Disposition"
    ] = "attachment; filename=sanctions_export.xlsx"

    response.headers[
        "Content-Type"
    ] = (
        "application/vnd.openxmlformats-officedocument."
        "spreadsheetml.sheet"
    )

    return response

@app.route("/health")
def health():

    try:

        stats = get_dashboard_stats()

        return jsonify({

            "status": "healthy",

            "api": "running",

            "database": "connected",

            "persons": stats["persons"],

            "aliases": stats["aliases"],

            "passports": stats["passports"],

            "addresses": stats["addresses"],

            "amendments": stats["amendments"]

        })

    except Exception as e:

        return jsonify({

            "status": "unhealthy",

            "api": "running",

            "database": "disconnected",

            "error": str(e)

        }), 500

@app.route("/health-ui")
def health_ui():

    stats = get_dashboard_stats()

    return render_template(
        "health.html",
        stats=stats
    )

@app.route("/docs")
def docs():

    return render_template("docs.html")


@app.errorhandler(404)
def page_not_found(error):

    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(error):

    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(debug=True)

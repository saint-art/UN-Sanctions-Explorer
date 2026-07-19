from flask import Flask, jsonify, request

from database import (
    get_connection,
    get_dashboard_stats,
    get_person,
    get_aliases
)

app = Flask(__name__)


@app.route("/")
def home():

    return jsonify({

        "project": "UN Security Council Sanctions API",

        "version": "1.0",

        "developer": "Nelvin",

        "endpoints": [

            "/stats",

            "/persons",

            "/person/<sanction_id>",

            "/search?q=name",

            "/health"

        ]

    })


@app.route("/persons")
def persons():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM persons

        LIMIT 50

    """)

    rows = cursor.fetchall()

    conn.close()

    return jsonify([dict(row) for row in rows])


@app.route("/search")
def search():

    query = request.args.get("q", "")

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT *

        FROM persons

        WHERE

            full_name LIKE ?

            OR nationality LIKE ?

            OR sanction_id LIKE ?

        LIMIT 50

    """, (

        f"%{query}%",

        f"%{query}%",

        f"%{query}%"

    ))

    rows = cursor.fetchall()

    conn.close()

    return jsonify({

        "count": len(rows),

        "results": [dict(row) for row in rows]

    })


@app.route("/stats")
def stats():

    stats = get_dashboard_stats()

    return jsonify(stats)


@app.route("/person/<sanction_id>")
def person_details(sanction_id):

    person = get_person(sanction_id)

    if person is None:

        return jsonify({

            "error": "Person not found"

        }), 404

    aliases = get_aliases(sanction_id)

    return jsonify({

        "person": dict(person),

        "aliases": [

            row["alias_name"]

            for row in aliases

        ]

    })


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


if __name__ == "__main__":

    app.run(debug=True)
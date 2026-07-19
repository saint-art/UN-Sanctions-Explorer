import sqlite3

DB_NAME = "sanctions.db"


# ----------------------------------------
# Database Connection
# ----------------------------------------

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


# ----------------------------------------
# Search Persons
# ----------------------------------------

def search_persons(
    search="",
    field="all",
    page=1,
    per_page=10,
    sort="name"
):

    conn = get_connection()
    cursor = conn.cursor()

    pattern = f"%{search}%"

    filters = {

        "name": (
            "full_name LIKE ?",
            [pattern]
        ),

        "nationality": (
            "nationality LIKE ?",
            [pattern]
        ),

        "id": (
            "sanction_id LIKE ?",
            [pattern]
        )

    }

    if field in filters:

        where, params = filters[field]

    else:

        where = """

            full_name LIKE ?

            OR nationality LIKE ?

            OR sanction_id LIKE ?

        """

        params = [
            pattern,
            pattern,
            pattern
        ]

    # Safe ORDER BY mapping
    sort_columns = {
        "id": "sanction_id",

        "name": "full_name",

        "nationality": "nationality",

        "dob": "dob"

    }

    order_by = sort_columns.get(
        sort,
        "full_name"
    )

    cursor.execute(

        f"""

        SELECT COUNT(*)

        FROM persons

        WHERE {where}

        """,

        params

    )

    total = cursor.fetchone()[0]

    offset = (page - 1) * per_page

    cursor.execute(

        f"""

        SELECT

            sanction_id,

            full_name,

            nationality,

            dob

        FROM persons

        WHERE {where}

        ORDER BY {order_by}

        LIMIT ?

        OFFSET ?

        """,

        params + [
            per_page,
            offset
        ]

    )

    rows = cursor.fetchall()

    conn.close()

    return rows, total

def export_search_results(
    search="",
    field="all",
    sort="name"
):

    conn = get_connection()
    cursor = conn.cursor()

    pattern = f"%{search}%"

    filters = {

        "name": (
            "full_name LIKE ?",
            [pattern]
        ),

        "nationality": (
            "nationality LIKE ?",
            [pattern]
        ),

        "id": (
            "sanction_id LIKE ?",
            [pattern]
        )

    }

    if field in filters:

        where, params = filters[field]

    else:

        where = """
            full_name LIKE ?
            OR nationality LIKE ?
            OR sanction_id LIKE ?
        """

        params = [
            pattern,
            pattern,
            pattern
        ]

    sort_columns = {

        "name": "full_name",

        "nationality": "nationality",

        "dob": "dob"

    }

    order_by = sort_columns.get(
        sort,
        "full_name"
    )

    cursor.execute(

        f"""
        SELECT

            sanction_id,

            full_name,

            nationality,

            dob

        FROM persons

        WHERE {where}

        ORDER BY {order_by}
        """,

        params

    )

    rows = cursor.fetchall()

    conn.close()

    return rows

# ----------------------------------------
# Dashboard Statistics
# ----------------------------------------

def get_dashboard_stats():

    conn = get_connection()
    cursor = conn.cursor()

    stats = {}

    for table in (
        "persons",
        "aliases",
        "passports",
        "addresses",
        "amendments"
    ):

        cursor.execute(

            f"SELECT COUNT(*) FROM {table}"

        )

        stats[table] = cursor.fetchone()[0]

    conn.close()

    return stats


# ----------------------------------------
# Person Information
# ----------------------------------------

def get_person(sanction_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(

        """

        SELECT *

        FROM persons

        WHERE sanction_id = ?

        """,

        (sanction_id,)

    )

    person = cursor.fetchone()

    conn.close()

    return person


def get_aliases(sanction_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(

        """

        SELECT alias_name

        FROM aliases

        WHERE sanction_id = ?

        """,

        (sanction_id,)

    )

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_passports(sanction_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(

        """

        SELECT passport_detail

        FROM passports

        WHERE sanction_id = ?

        """,

        (sanction_id,)

    )

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_addresses(sanction_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(

        """

        SELECT address

        FROM addresses

        WHERE sanction_id = ?

        """,

        (sanction_id,)

    )

    rows = cursor.fetchall()

    conn.close()

    return rows


def get_amendments(sanction_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(

        """

        SELECT amendment_date

        FROM amendments

        WHERE sanction_id = ?

        """,

        (sanction_id,)

    )

    rows = cursor.fetchall()

    conn.close()

    return rows


# ----------------------------------------
# Dashboard Analytics
# ----------------------------------------

def get_top_nationalities(limit=10):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(

        """

        SELECT

            nationality,

            COUNT(*) AS total

        FROM persons

        WHERE nationality IS NOT NULL
          AND nationality <> ''

        GROUP BY nationality

        ORDER BY total DESC

        LIMIT ?

        """,

        (limit,)

    )

    rows = cursor.fetchall()

    conn.close()

    return rows
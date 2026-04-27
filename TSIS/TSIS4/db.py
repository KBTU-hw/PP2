import psycopg2


def get_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="Ai474663",
        host="localhost",
        port="5432"
    )


def setup_database():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS players (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS game_sessions (
            id SERIAL PRIMARY KEY,
            player_id INTEGER REFERENCES players(id),
            score INTEGER NOT NULL,
            level_reached INTEGER NOT NULL,
            played_at TIMESTAMP DEFAULT NOW()
        );
        """
    )
    conn.commit()
    cur.close()
    conn.close()


def get_or_create_player(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM players WHERE username=%s", (username,))
    row = cur.fetchone()
    if row:
        cur.close()
        conn.close()
        return row[0]

    cur.execute("INSERT INTO players(username) VALUES(%s) RETURNING id", (username,))
    pid = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return pid


def save_result(username, score, level):
    pid = get_or_create_player(username)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO game_sessions(player_id,score,level_reached) VALUES(%s,%s,%s)",
        (pid, int(score), int(level)),
    )
    conn.commit()
    cur.close()
    conn.close()


def get_top_scores(limit=10):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT p.username, g.score, g.level_reached, g.played_at
        FROM game_sessions g
        JOIN players p ON p.id=g.player_id
        ORDER BY g.score DESC, g.played_at DESC
        LIMIT %s
        """,
        (limit,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_personal_best(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT COALESCE(MAX(g.score),0)
        FROM game_sessions g
        JOIN players p ON p.id=g.player_id
        WHERE p.username=%s
        """,
        (username,),
    )
    best = cur.fetchone()[0]
    cur.close()
    conn.close()
    return int(best)

import psycopg2
from datetime import datetime
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


class SnakeGameDB:
    def __init__(self):
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Connect to PostgreSQL database"""
        try:
            self.conn = psycopg2.connect(
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
            self.cursor = self.conn.cursor()
            return True
        except Exception as e:
            print(f"Database connection failed: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
    
    def create_tables(self):
        """Create players and game_sessions tables if they don't exist"""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS players (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL
                );
            """)
            
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS game_sessions (
                    id SERIAL PRIMARY KEY,
                    player_id INTEGER REFERENCES players(id),
                    score INTEGER NOT NULL,
                    level_reached INTEGER NOT NULL,
                    played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error creating tables: {e}")
            self.conn.rollback()
            return False
    
    def get_or_create_player(self, username):
        """Get player ID, or create new player if doesn't exist"""
        try:
            # Check if player exists
            self.cursor.execute("SELECT id FROM players WHERE username = %s", (username,))
            result = self.cursor.fetchone()
            
            if result:
                return result[0]
            
            # Create new player
            self.cursor.execute("INSERT INTO players (username) VALUES (%s) RETURNING id", (username,))
            player_id = self.cursor.fetchone()[0]
            self.conn.commit()
            return player_id
        except Exception as e:
            print(f"Error getting/creating player: {e}")
            return None
    
    def save_game_session(self, player_id, score, level):
        """Save game session to database"""
        try:
            self.cursor.execute(
                "INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)",
                (player_id, score, level)
            )
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error saving game session: {e}")
            self.conn.rollback()
            return False
    
    def get_leaderboard(self, limit=10):
        """Get top scores from leaderboard"""
        try:
            self.cursor.execute("""
                SELECT 
                    ROW_NUMBER() OVER (ORDER BY score DESC) as rank,
                    p.username,
                    g.score,
                    g.level_reached,
                    g.played_at
                FROM game_sessions g
                JOIN players p ON g.player_id = p.id
                ORDER BY g.score DESC
                LIMIT %s;
            """, (limit,))
            
            results = self.cursor.fetchall()
            return results
        except Exception as e:
            print(f"Error fetching leaderboard: {e}")
            return []
    
    def get_player_best_score(self, username):
        """Get player's best score"""
        try:
            self.cursor.execute("""
                SELECT MAX(score) FROM game_sessions g
                JOIN players p ON g.player_id = p.id
                WHERE p.username = %s;
            """, (username,))
            
            result = self.cursor.fetchone()
            return result[0] if result[0] is not None else 0
        except Exception as e:
            print(f"Error fetching player best score: {e}")
            return 0


# Global database instance
db = SnakeGameDB()

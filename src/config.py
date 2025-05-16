from dataclasses import dataclass
from dotenv import load_dotenv
from os import getenv

@dataclass
class _Config():
    HOST: str
    PORT: int
    
    DB_MAXCON: int
    DB_URL: str
    DB_URL_SYNC: str
    
    def init():
        load_dotenv()
        
        pg_username, pg_password, pg_database = (getenv('PGUSER', "app"),
                                                 getenv('PGPASSWORD', "secret"),
                                                 getenv('PGDATABASE', "appdb"))
    
        db_url = f"postgresql+asyncpg://{pg_username}:{pg_password}@postgres:5432/{pg_database}"
        db_url_sync = db_url.replace("+asyncpg", "")
        db_maxcon = int(getenv('DB_MAXCON', 5))
        
        host, port = '0.0.0.0', 8000
        
        return _Config(
            HOST=host,
            PORT=port,
            DB_MAXCON=db_maxcon,
            DB_URL=db_url,
            DB_URL_SYNC=db_url_sync
        )

Config = _Config.init()
        
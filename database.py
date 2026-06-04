import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Cargamos las variables de entorno si existen
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# --- LÓGICA DE DECISIÓN DE ENTORNOS ---

if not DATABASE_URL:
    # 1. MODO DESARROLLO (TU MÁQUINA): Si no hay archivo .env, usamos SQLite
    DATABASE_URL = "sqlite:///./votacion.db"
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
    print("🔧 MODO LOCAL: Usando base de datos SQLite (votacion.db)")

else:
    # 2. MODO PRODUCCIÓN (NUBE / COMPAÑERO): Si hay un enlace a PostgreSQL
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    engine = create_engine(DATABASE_URL)
    print("☁️ MODO NUBE: Usando base de datos PostgreSQL")

# --- CONFIGURACIÓN ESTÁNDAR ---
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Operatore(Base):
    __tablename__ = 'operatori'
    id = Column(Integer, primary_key=True)
    badge_id = Column(String(20), unique=True)
    nome = Column(String(50))
    cognome = Column(String(50))
    ruolo = Column(String(50))
    turno = Column(String(20))
    
    # Relazione 1:N verso Lotto (Un operatore fa molti lotti)
    lotti = relationship("Lotto", back_populates="operatore")

class Farmaco(Base):
    __tablename__ = 'farmaci'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    temp_max = Column(Float)
    umidita_max = Column(Float)
    
    # Relazione 1:N verso Lotto (Un farmaco ha molti lotti)
    lotti = relationship("Lotto", back_populates="farmaco")

class Lotto(Base):
    __tablename__ = 'lotti'
    id = Column(Integer, primary_key=True)
    codice_lotto = Column(String(50), unique=True)
    temperatura_rilevata = Column(Float)
    umidita_rilevata = Column(Float)
    esito_controllo = Column(String(20))
    timestamp = Column(DateTime, default=datetime.now)

    # --- CHIAVI ESTERNE (Foreign Keys) ---
    id_farmaco = Column(Integer, ForeignKey('farmaci.id'))
    id_operatore = Column(Integer, ForeignKey('operatori.id'))

    # Collegamenti per la navigazione tra oggetti in Python
    farmaco = relationship("Farmaco", back_populates="lotti")
    operatore = relationship("Operatore", back_populates="lotti")

# Creazione fisica del database
# NOTA: Uso un nuovo nome file per evitare conflitti con vecchie versioni incomplete
engine = create_engine('sqlite:///azienda_farmaceutica.db')
Base.metadata.create_all(engine)

print("✅ Database generato correttamente con le relazioni FK!")
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime


Base = declarative_base()



class Farmaco(Base):
    __tablename__ = 'farmaci'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50), nullable=False)
    temp_max = Column(Float)
    umidita_max = Column(Float)
    
    lotti = relationship("Lotto", back_populates="farmaco")

class Operatore(Base):
    __tablename__ = 'operatori'
    id = Column(Integer, primary_key=True)
    badge_id = Column(String(20), unique=True)
    nome = Column(String(50))
    cognome = Column(String(50))
    ruolo = Column(String(50))
    turno = Column(String(20))
    
    lotti = relationship("Lotto", back_populates="operatore")

class Lotto(Base):
    __tablename__ = 'lotti'
    id = Column(Integer, primary_key=True)
    codice_lotto = Column(String(50), unique=True)
    temperatura_rilevata = Column(Float)
    umidita_rilevata = Column(Float)
    esito_controllo = Column(String(20))
    timestamp = Column(DateTime, default=datetime.now)
    
    
    id_farmaco = Column(Integer, ForeignKey('farmaci.id'))
    id_operatore = Column(Integer, ForeignKey('operatori.id'))
    
    
    farmaco = relationship("Farmaco", back_populates="lotti")
    operatore = relationship("Operatore", back_populates="lotti")



engine = create_engine('sqlite:///azienda_farmaceutica.db')
Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)
session = Session()

def popola_dati_iniziali():
    print("⏳ Inizializzazione azienda in corso...")
    
    
    f1 = Farmaco(nome="Tachipirina", temp_max=25.0, umidita_max=40.0)
    f2 = Farmaco(nome="Oki Task", temp_max=22.0, umidita_max=35.0)
    f3 = Farmaco(nome="Bentelan", temp_max=24.0, umidita_max=45.0)

    
    op1 = Operatore(badge_id="B001", nome="Francesco", cognome="Rossi", ruolo="Tecnico Linea", turno="Mattina")
    op2 = Operatore(badge_id="B002", nome="Laura", cognome="Bianchi", ruolo="Supervisore", turno="Pomeriggio")
    op3 = Operatore(badge_id="B003", nome="Giuseppe", cognome="Esposito", ruolo="Responsabile Qualità", turno="Notte")

    
    session.add_all([f1, f2, f3, op1, op2, op3])
    session.commit()
    
    print("✅ Database 'azienda_farmaceutica.db' creato con successo!")
    print("✅ Operatori e Farmaci inseriti.")

if __name__ == "__main__":
    popola_dati_iniziali()

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker



engine = create_engine('sqlite:///azienda_farmaceutica.db')
Session = sessionmaker(bind=engine)
session = Session()

def popola_farmaci_da_excel():
    try:
        
        
        df = pd.read_excel('anagrafica_prodotti.xlsx')
        
        print(f"File trovato! Sto caricando {len(df)} farmaci...")

        for index, riga in df.iterrows():
            
            nuovo_farmaco = Farmaco(
                nome=riga['Nome'], 
                temp_max=riga['Temp_Max'], 
                umidita_max=riga['Umidita_Max']
            )
            session.add(nuovo_farmaco)
        
        session.commit()
        print("✅ Database aggiornato con i farmaci dall'Excel!")
        
    except FileNotFoundError:
        print("❌ Errore: Il file 'anagrafica_prodotti.xlsx' non è stato trovato!")
    except Exception as e:
        print(f"❌ Errore durante l'importazione: {e}")


if __name__ == "__main__":
    
    popola_farmaci_da_excel()


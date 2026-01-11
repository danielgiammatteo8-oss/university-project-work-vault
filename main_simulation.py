import time
import random
from sqlalchemy.orm import sessionmaker
from database import engine, Farmaco, Operatore
from core_logic import ControlloQualita

def avvia_produzione():
    # 1. Inizializzazione Sessione e Logica
    Session = sessionmaker(bind=engine)
    session = Session()
    qc_system = ControlloQualita()
    
    # 2. Caricamento Anagrafiche dal DB
    farmaci_disponibili = session.query(Farmaco).all()
    operatori_disponibili = session.query(Operatore).all()

    if not farmaci_disponibili or not operatori_disponibili:
        print("❌ ERRORE: Database vuoto! Esegui prima 'setup_azienda.py'.")
        return

    print("--- 🏭 AVVIO SIMULATORE LINEA DI PRODUZIONE CONNESSO AL DB ---")
    
    count = 1
    try:
        while count <= 15:
            # Selezione casuale di un farmaco e un operatore reali dal database
            farmaco = random.choice(farmaci_disponibili)
            operatore = random.choice(operatori_disponibili)
            
            codice = f"BATCH-2025-{count:03d}"
            
            # Simulazione sensori
            temp = round(random.gauss(22.0, 2.0), 2) # Temperatura tra 22.0 e 27.0, 22.0 è la media, 2.0 è la deviazione più il valore è piccolo più i dati sono simili, più è grande più sono diversi
            umid = round(random.gauss(45.0, 5.0), 2)

            # Eseguiamo il controllo e il salvataggio tramite il Core Logic
            # Passiamo gli oggetti farmaco e operatore per mantenere le relazioni (FK)
            risultato = qc_system.analizza_e_salva(codice, farmaco, operatore, temp, umid)
            
            print(f"📦 Lotto: {codice} | Prodotto: {farmaco.nome}")
            print(f"   Operatore: {operatore.nome} {operatore.cognome} ({operatore.turno})")
            print(f"   Sensori: {temp}°C, {umid}% -> Esito: {risultato}")
            print("-" * 50)
            
            count += 1
            time.sleep(1) 
            
    except KeyboardInterrupt:
        print("\n🛑 Linea fermata manualmente.")
    finally:
        session.close()

if __name__ == "__main__":
    avvia_produzione()
import logging
from sqlalchemy.orm import sessionmaker
from database import engine, Lotto

# Configurazione Log per tracciabilità (Audit Trail farmaceutico)
logging.basicConfig(
    filename='produzione.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ControlloQualita:
    def __init__(self):
        # Inizializziamo la sessione per salvare i risultati
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def analizza_e_salva(self, codice, farmaco_obj, operatore_obj, temp, umidita):
        """
        Riceve gli oggetti del DB (farmaco e operatore) e i dati dei sensori.
        Esegue il controllo e salva il Lotto.
        """
        # LOGICA DI CONTROLLO (Usa i limiti salvati nel database per quel farmaco)
        esito = "CONFORME"
        if temp > farmaco_obj.temp_max or umidita > farmaco_obj.umidita_max:
            esito = "SCARTO"
            msg = f"ALLARME: Lotto {codice} ({farmaco_obj.nome}) fuori specifica! Operatore: {operatore_obj.cognome}"
            logging.warning(msg)
        else:
            logging.info(f"Lotto {codice} approvato da {operatore_obj.cognome}.")

        # SALVATAGGIO NEL DATABASE (Sfruttando le Foreign Keys)
        nuovo_lotto = Lotto(
            codice_lotto=codice,
            temperatura_rilevata=temp,
            umidita_rilevata=umidita,
            esito_controllo=esito,
            id_farmaco=farmaco_obj.id,     # FK verso Farmaco
            id_operatore=operatore_obj.id  # FK verso Operatore
        )
        
        try:
            self.session.add(nuovo_lotto)
            self.session.commit()
            return esito
        except Exception as e:
            self.session.rollback()
            logging.error(f"Errore salvataggio DB: {e}")
            return "ERRORE DB"
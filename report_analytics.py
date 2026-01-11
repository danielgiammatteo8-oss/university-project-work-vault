import pandas as pd
from sqlalchemy import create_engine

def genera_report_professionale():
    engine = create_engine('sqlite:///azienda_farmaceutica.db')
    
    # Nota: assicurati che il nome della tabella sia 'produzione' o 'lotti' in base al tuo DB
    query = """
    SELECT 
        l.codice_lotto, 
        f.nome AS prodotto, 
        o.nome || ' ' || o.cognome AS operatore,
        o.turno,
        l.temperatura_rilevata AS temperatura, 
        l.umidita_rilevata AS umidita, 
        l.esito_controllo, 
        l.timestamp
    FROM lotti l
    JOIN farmaci f ON l.id_farmaco = f.id
    JOIN operatori o ON l.id_operatore = o.id
    """
    
    df = pd.read_sql(query, engine)
    
    if df.empty:
        print("Database vuoto! Esegui prima la simulazione.")
        return

    file_name = "Report_Produzione.xlsx"
    writer = pd.ExcelWriter(file_name, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Dati Produzione', index=False)

    workbook  = writer.book
    worksheet = writer.sheets['Dati Produzione']

    # --- FORMATTAZIONE ESISTENTE ---
    format_rosso = workbook.add_format({'bg_color': '#FFC7CE', 'font_color': '#9C0006'})
    format_verde = workbook.add_format({'bg_color': '#C6EFCE', 'font_color': '#006100'})

    worksheet.conditional_format('G2:G500', {
        'type': 'cell', 'criteria': '==', 'value': '"SCARTO"', 'format': format_rosso
    })
    worksheet.conditional_format('G2:G500', {
        'type': 'cell', 'criteria': '==', 'value': '"CONFORME"', 'format': format_verde
    })

    # --- AGGIUNTA GRAFICI ---
    
    # 1. GRAFICO A TORTA: Riepilogo Esiti (Conforme vs Scarto)
    # Creiamo un foglio di supporto per i calcoli del grafico (opzionale ma pulito)
    counts = df['esito_controllo'].value_counts()
    summary_sheet = workbook.add_worksheet('Statistiche')
    summary_sheet.write('A1', 'Esito')
    summary_sheet.write('B1', 'Conteggio')
    summary_sheet.write_column('A2', counts.index)
    summary_sheet.write_column('B2', counts.values)

    pie_chart = workbook.add_chart({'type': 'pie'})
    pie_chart.add_series({
        'name': 'Distribuzione Qualità',
        'categories': '=Statistiche!$A$2:$A$3',
        'values':     '=Statistiche!$B$2:$B$3',
        'points': [
            {'fill': {'color': '#C6EFCE'}}, # Verde per Conforme
            {'fill': {'color': '#FFC7CE'}}, # Rosso per Scarto
        ],
    })
    pie_chart.set_title({'name': 'Riepilogo Conformità Lotti'})
    
    # Inseriamo il grafico nel foglio principale
    worksheet.insert_chart('J2', pie_chart)

    # 2. GRAFICO A LINEE: Andamento Temperature
    line_chart = workbook.add_chart({'type': 'line'})
    line_chart.add_series({
        'name':       'Temperatura',
        'categories': f'=Dati Produzione!$A$2:$A${len(df)+1}',
        'values':     f'=Dati Produzione!$E$2:$E${len(df)+1}',
        'line':       {'color': 'blue'},
    })
    line_chart.set_title({'name': 'Monitoraggio Termico Produzione'})
    line_chart.set_x_axis({'name': 'Codice Lotto'})
    line_chart.set_y_axis({'name': 'Temperatura (°C)'})
    
    worksheet.insert_chart('J18', line_chart)

    # Regoliamo la larghezza delle colonne
    worksheet.set_column('A:H', 20)

    writer.close()
    print(f"✅ Report con grafici creato: {file_name}")

if __name__ == "__main__":
    genera_report_professionale()
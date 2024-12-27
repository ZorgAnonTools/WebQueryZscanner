import random
import string
import aiohttp
import asyncio
from termcolor import colored
import pandas as pd

# Funzione per generare query string casuali
def genera_query_casuale():
    parametri = ["param1", "param2", "id", "q", "search", "category"]
    valori = ["value1", "value2", "123", "query", "keyword", "cat1", "cat2"]
    query = f"{random.choice(parametri)}={random.choice(valori)}"
    return query

# Numero di query string da generare
num_query_da_generare = 1000

# Genera e stampa le query string casuali
query_string_casuali = [genera_query_casuale() for _ in range(num_query_da_generare)]

# Chiedi all'utente di inserire un URL di destinazione
url_destinazione = input("Inserisci il dominio di destinazione (es. google.com): ")

# Aggiungi uno schema di default (http://) all'URL inserito dall'utente
if not url_destinazione.startswith("http://") and not url_destinazione.startswith("https://"):
    url_destinazione = "http://" + url_destinazione

# Lista di siti web di destinazione
siti_web = [url_destinazione]

async def verifica_query_string(session, sito, query_string):
    url = f"{sito}/?{query_string}"
    async with session.get(url) as response:
        risultato = "OK" if response.status == 200 else "KO"
        risultati[sito].append({"URL_completo": url, "Query": query_string, "Risultato": risultato})
        risultati_tabella.append({"URL_completo": url, "Query": query_string, "Risultato": risultato})

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [verifica_query_string(session, sito, query_string) for sito in siti_web for query_string in query_string_casuali]
        await asyncio.gather(*tasks)

risultati = {sito: [] for sito in siti_web}
risultati_tabella = []

loop = asyncio.get_event_loop()
loop.run_until_complete(main())

# Creazione e visualizzazione della tabella dei risultati
df = pd.DataFrame(risultati_tabella)

# Filtra il dataframe per mostrare solo i risultati "OK"
df_ok = df[df['Risultato'] == 'OK']

# Stampare la tabella dei risultati "OK"
print("\nTabella dei risultati (solo URL con query funzionanti):")
print(df_ok[['URL_completo', 'Query']])

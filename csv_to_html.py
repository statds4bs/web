import pandas as pd
from bs4 import BeautifulSoup
import re
import glob
import datetime
today = datetime.datetime.now().strftime("%d/%m")

ff = glob.glob("parteci*.csv")
df = pd.read_csv(ff[0])
def capitalize(text):
    return text.lower().capitalize()
# Todo: filtra anche i cancellati
cons = (df['Consenso alla pubblicazione del nome come partecipante'] != 'No')
non_canc = (df["Cancellato"] != "Si")
df_clean = df[cons & non_canc][['Nome', 'Cognome', 'Azienda']]

df_clean = df_clean.apply(lambda x: x.str.title())

# rimuovi i test
df_export = df_clean[3:]
df_export = df_export.drop_duplicates(subset=["Nome", "Cognome"])
df_export = df_export.sort_values("Cognome")

with open("partecipanti.html", "r", encoding="utf-8") as file:
     hh = file.read()

# Parse the HTML
pag = BeautifulSoup(hh, "html.parser")
tab_html = df_export.to_html(justify="left", index = False)
tab_html = tab_html.replace('<th>', '<th style="font-weight:bold;">')

# Update the table
table_element = pag.find("table")
table_element.clear()
table_element.append(BeautifulSoup(tab_html, "html.parser"))

# Update date
aggOLD = pag.find(text = re.compile('aggiornata'))
number_match = re.search(r'\d+/\d+', aggOLD)
modified_string = aggOLD.replace(number_match.group(), today)
# Update the content with the modified string
aggOLD.replace_with(modified_string)


with open("partecipanti.html", "w", encoding="utf-8") as file:
        file.write(str(pag))


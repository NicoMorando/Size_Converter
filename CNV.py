# IMPORT LIBRARIES
import os
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.config import Config
import pandas as pd
from datetime import datetime

# AUTHOR: Morando Nicolò, date: '27/04/2024'
# ULTIMA MODIFICA: '08/05/2024'

# Configurazione interfaccia grafica
class Convertitore(App):
    def build(self):
        # config
        self.icon = "favicon.png"
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.8, 0.9)
        self.window.pos_hint = {"center_x": 0.5, "center_y": 0.5}
        # LOGO
        self.window.add_widget(Image(source="assets/logo.png"))
        # PULSANTI
        self.button_nike = Button(
            text="NIKE - Aggiungi Age Group",
            size_hint=(2, 0.5),
            bold=True,
            background_color='#ff3d33',
        )
        self.button_haddad = Button(
            text="HADDAD - Aggiungi Age Group & Brand",
            size_hint=(2, 0.5),
            bold=True,
            background_color='#ff3d33',
        ) # START
        self.button_nike.bind(on_press=self.NIKE)
        self.button_haddad.bind(on_press=self.HADDAD)
        self.window.add_widget(self.button_nike)
        self.window.add_widget(self.button_haddad)
        return self.window

# ---------------------------------------------------------------------------------------------------------

    # Funzione per conversione Conferme d'ordine NIKE
    def NIKE(self, instance):
        current_dateTime = datetime.now()
        """
            Convertitore per Age Group di Nike.
            Richiede il file excel della conferma d'ordine di Nike posizionabile nella cartella "excel/..."
            riceve i codici e size Nike e li decodifica secondo la logica e le nominazioni apprese.
            Args:
                input_file (str): Path to the input Excel file.
                received_code (str): Code used for processing the data.
                output_file (str): Path to the output Excel file.
        """

        # Decodifica Age Group
        def categorize_age_group(gender_age_code):
            if gender_age_code in ["MENS", "WOMENS", "ADULT", "ADULT UNISEX"]:
                return "BIG SIZE"
            elif gender_age_code == "TODDLER UNISEX":
                return "INFANT"
            elif gender_age_code == "PRE SCHOOL UNSX":
                return "KIDS"
            elif "BOYS GRADE SCHL" in gender_age_code:
                return "TEEN"
            elif "GRD SCHOOL UNSX" in gender_age_code:
                return "TEEN"
            elif "BOYS" in gender_age_code or "GIRLS" in gender_age_code or gender_age_code == "YOUTH UNISEX":
                return "TEEN"
            else:
                return "MANCANTE"

        # Funzione per la modifica del file excel in input
        def process_excel_file(input_file):
            input_df = pd.read_excel(input_file)
            if 'Gndr Age Cd' not in input_df.columns:
                print("ERRORE - Conferma d'ordine errata, assicurati di aver inserito quella di NIKE.")
                return
            else:
                input_df['Age Group'] = input_df['Gndr Age Cd'].apply(categorize_age_group)
                input_df.to_excel(input_file, index=False)
                # Ricezione file excel path e scrittura sul log
                print("ESEGUITO - Conversione Nike Eseguita", current_dateTime)

        file_path = next(os.path.join("excel/", f) for f in os.listdir("excel/") if f.endswith(".xlsx"))
        process_excel_file(file_path)

# ---------------------------------------------------------------------------------------------------------

    # Funzione per la conversione Conferme d'ordine HADDAD
    def HADDAD(self, instance):
        current_dateTime = datetime.now()
        """
            Convertitore per Age Group di haddad (nike, jordan, converse).
            Richiede un file excel della conferma d'ordine Haddad posizionabile nella cartella "excel/..."
            riceve i codici prodotto Haddad e li decodifica secondo la logica appresa
            Args:
                input_file (str): Path to the input Excel file.
                received_code (str): Code used for processing the data.
                output_file (str): Path to the output Excel file.
        """

        # funzione principale
        def process_excel_file(input_file):
            input_df = pd.read_excel(input_file)
            if 'Vendor Item No_' not in input_df.columns:
                print("ERRORE - Conferma d'ordine errata, assicurati di aver inserito quella di HADDAD.")
                return
            else:            # Verifica dell'age Group
                def categorize_age_group(code):
                    if code[1] == 'A':
                        return ''
                    if code[0] in ['1', '6']:
                        return 'INFANT'
                    elif code[0] in ['3', '8']:
                        return 'KIDS'
                    elif code[0] in ['4', '9']:
                        return 'TEEN'
                    else:
                        return ''

                            # Verifica del brand
                def categorize_brand(code):
                        if code[1] == '6':
                            return 'NIKE'
                        elif code[1] == '5':
                            return 'JORDAN'
                        elif code[1] == 'C':
                            return 'CONVERSE'
                        elif code[1] == 'A':
                            return ''
        # Se visualizza che è un accessorio e il secondo carattere è una lettera (A) non darà brand
                        else:
                            return ''

                print("ESEGUITO - Conversione Haddad Eseguita", current_dateTime)
        # Lettura file ed attribuzione nuova colonna
                input_df['Age Group'] = input_df['Vendor Item No_'].apply(categorize_age_group)
                input_df['Brand'] = input_df['Vendor Item No_'].apply(categorize_brand)
                input_df.to_excel(input_file, index=False)

        # Ricezione file excel path e scrittura sul log
        file_path = next(os.path.join("excel/", f) for f in os.listdir("excel/") if f.endswith(".xlsx"))
        process_excel_file(file_path)


# Avvio
if __name__ == "__main__":
    Convertitore().run()

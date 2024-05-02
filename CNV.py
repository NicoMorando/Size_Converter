from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.config import Config
import pandas as pd

# AUTHOR: Morando Nicolò, date: 02/05/2024

class Conv(App):
    def build(self):
        # Configurazione interfaccia grafica
        self.icon = "favicon.png"
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.6, 0.7)
        self.window.pos_hint = {"center_x": 0.5, "center_y":0.5}

        # LOGO
        self.window.add_widget(Image(source="assets/logo.png"))

        # Buttons per interfaccia
        self.button_nike = Button(
                      text= "CONVERTI NIKE",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#ff3d33',
                      )
        self.button_haddad = Button(
                      text= "CONVERTI HADDAD",
                      size_hint= (1,0.5),
                      bold= True,
                      background_color ='#ff3d33',
                      )

        self.button_nike.bind(on_press=self.NIKE)
        self.button_haddad.bind(on_press=self.HADDAD)
        self.window.add_widget(self.button_nike)
        self.window.add_widget(self.button_haddad)
        return self.window


# Configurazione Funzioni per la conversione aggiornate al 02/05/2024, attuali disponibili: NIKE, HADDAD

    # Funzione per conversione FILE NIKE
    def NIKE(self, instance):
        def categorize_age_group(gender_age_code):
            """Categorizes the age group based on the gender age code."""
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
        # Lettura file Excel in input
        def process_excel_file(input_file, output_file):
            df = pd.read_excel(input_file)
            # Crea una colonna : 'age group' basata sulla : 'Gndr Age Cd'
            df['age group'] = df['Gndr Age Cd'].apply(categorize_age_group)
            # Esportazione nel nuovo file Excel convertito.
            df[['Prod Cd', 'age group']].to_excel(output_file, index=False)
        # Files di input ed output
        input_file = "ricezione/nike.xlsx"
        output_file = "convertiti/conv_nike.xlsx"
        # Elaborazione
        process_excel_file(input_file, output_file)
        print("ESEGUITO >>>>>>>>>>>> - Conversione Nike Eseguita")

# ---------------------------------------------------------------------------------------------------------------------------------------

    # Funzione per la conversione FILE HADDAD
    def HADDAD(self, instance):
        def process_excel_file(input_file, received_code, output_file):
            """
            Convertitore per Age Group di haddad (nike, jordan, converse).
            Richiede un file excel posizionabile nel folder  "ricezione/..." nominato "haddad.xlsx"
            riceve i codici prodotto haddad e li decodifica in modo alla
            Args:
                input_file (str): Path to the input Excel file.
                received_code (str): Code used for processing the data.
                output_file (str): Path to the output Excel file.
            """
            # Input del file excel
            df = pd.read_excel(input_file)
            # Crea due nuove colonne che poi verranno inserite nel file excel convertito
            df['Age Group'] = ''
            df['Brand'] = ''
            # Ricezione codice prodotto da excel
            for index, row in df.iterrows():
                code = str(row['Cod.Prodotto'])
                # code = str(df.iloc[:, 0])
                # Esegue il controllo su il primo e il secondo carattere
                    # primo carattere
                if code[0] == '1':
                    df.at[index, 'Age Group'] = 'INFANT'
                elif code[0] == '3':
                    df.at[index, 'Age Group'] = 'KIDS'
                elif code[0] == '4':
                    df.at[index, 'Age Group'] = 'TEEN'
                elif code[0] == '6':
                    df.at[index, 'Age Group'] = 'INFANT'
                elif code[0] == '8':
                    df.at[index, 'Age Group'] = 'KIDS'
                elif code[0] == '9':
                    df.at[index, 'Age Group'] = 'TEEN'
                # secondo carattere
                if code[1] == '6':
                    df.at[index, 'Brand'] = 'NIKE'
                elif code[1] == '5':
                    df.at[index, 'Brand'] = 'JORDAN'
                elif code[1] == 'c':
                    df.at[index, 'Brand'] = 'CONVERSE'
                # Salta se il primo carattere è una lettera ovvero un Accessorio
                if code[0].isalpha():
                    df.at[index, 'Age Group'] = 'ACCESSORIO'
            # Importa il processo in un nuovo file excel
            df.to_excel(output_file, index=False)
        # Output ed esportazione file excel convertito
        process_excel_file('ricezione/haddad.xlsx', '123', 'convertiti/conv_haddad.xlsx')
        print("ESEGUITO >>>>>>>>>>>> - Conversione Haddad Eseguita")

# run interface
if __name__ == "__main__":
    Conv().run()

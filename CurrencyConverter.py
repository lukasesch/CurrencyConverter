import argparse
import logging
import requests
import customtkinter

logging.basicConfig(level=logging.INFO)

argumentparser = argparse.ArgumentParser(description="CLI Währungsrechner")
argumentparser.add_argument("amount", type=float, help="Betrag welcher konvertiert werden soll")
argumentparser.add_argument("fromcurrency", type=str, help="Währung des Inputs")
argumentparser.add_argument("tocurrency", type=str, help="Währung des Outputs")

args = argumentparser.parse_args()
logging.info(f"Konvertiere {args.amount} {args.fromcurrency} nach {args.tocurrency}")


conversion_url = "https://api.frankfurter.dev/v1/latest"
parameters = {
    "base": args.fromcurrency,
    "symbols": args.tocurrency
}

response = requests.get(conversion_url, parameters)
logging.info(f"URL Aufruf gestartet an: {response.url}")
if response.status_code == 200:
    data = response.json()
    result = data["rates"][args.tocurrency]
    logging.info(f"Konvertierungsrate: {result}")
else:
    logging.error(response.status_code)

converted_result = float(result) * args.amount
print(f"{args.amount} {args.fromcurrency} sind zur Zeit umgerechnet {converted_result:.2f} {args.tocurrency}!")

#TODO CLI Use with arguments, otherwise GUI
#TODO Textfields erstellen
#TODO Währungen beziehen und via Drop Down neben Textfields

app = customtkinter.CTk()
app.geometry("300x150")
app.title("Currency Converter")

button = customtkinter.CTkButton(app, text="Convert", command=print("Button"))
button.pack(padx=20, pady=20)

app.mainloop()
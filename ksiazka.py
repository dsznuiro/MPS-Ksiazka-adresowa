import tkinter as tk
from tkinter import ttk, messagebox
import json

def load_data():
    try:
        with open("dane.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print("Plik 'dane.json' nie został znaleziony.")
        return []
    return data

def save_data(data):
    try:
        with open("dane.json", "r", encoding="utf-8") as f:
            adresy = json.load(f)
    except FileNotFoundError:
        adresy = []
    adresy.append(data)
    with open("dane.json", "w", encoding="utf-8") as f:
        json.dump(adresy, f, ensure_ascii=False, indent=4)

def show_table():
    for row in table.get_children():
        table.delete(row)
    adresy = load_data()
    for adres in adresy:
        table.insert("", "end", values=(
            adres["Imię"],
            adres["Nazwisko"],
            adres["Ulica"],
            adres["Numer domu"],
            adres["Miasto"]
        ))

def sprawdz_duplikaty(imie, nazwisko):
    adresy = load_data()
    for adres in adresy:
        if adres["Imię"] == imie and adres["Nazwisko"] == nazwisko:
            messagebox.showwarning("Uwaga", "Taki użytkownik już istnieje!")
            return True
    return False

def submit_data():
    imie = entry_imie.get()
    nazwisko = entry_nazwisko.get()
    ulica = entry_ulica.get()
    numer_domu = entry_numer_domu.get()
    miasto = entry_miasto.get()

    if not imie or not nazwisko:
        messagebox.showwarning("Uwaga", "Imię i nazwisko są wymagane!")
        return

    if sprawdz_duplikaty(imie, nazwisko):
        return

    adres = {
        "Imię": imie,
        "Nazwisko": nazwisko,
        "Ulica": ulica,
        "Numer domu": numer_domu,
        "Miasto": miasto
    }
    save_data(adres)
    show_table()
    entry_imie.delete(0, tk.END)
    entry_nazwisko.delete(0, tk.END)
    entry_ulica.delete(0, tk.END)
    entry_numer_domu.delete(0, tk.END)
    entry_miasto.delete(0, tk.END)

def szukaj():
    fraza = entry_szukaj.get()
    adresy = load_data()
    for row in table.get_children():
        table.delete(row)
    for adres in adresy:
        if fraza.lower() in adres["Nazwisko"].lower():
            table.insert("", "end", values=(
                adres["Imię"],
                adres["Nazwisko"],
                adres["Ulica"],
                adres["Numer domu"],
                adres["Miasto"]
            ))

def statystyki():
    adresy = load_data()
    miasta = {}
    for adres in adresy:
        miasto = adres["Miasto"]
        miasta[miasto] = miasta.get(miasto, 0) + 1
    statystyka = "\n".join([f"{miasto}: {liczba}" for miasto, liczba in miasta.items()])
    messagebox.showinfo("Statystyki", statystyka)

#tworzenie okna głównego
root = tk.Tk()
root.title("Formularz Adresowy")

#pola do wprowadzania danych
tk.Label(root, text="Imię:").grid(row=0, column=0, sticky="w")
entry_imie = tk.Entry(root)
entry_imie.grid(row=0, column=1)

tk.Label(root, text="Nazwisko:").grid(row=1, column=0, sticky="w")
entry_nazwisko = tk.Entry(root)
entry_nazwisko.grid(row=1, column=1)

tk.Label(root, text="Ulica:").grid(row=2, column=0, sticky="w")
entry_ulica = tk.Entry(root)
entry_ulica.grid(row=2, column=1)

tk.Label(root, text="Numer domu:").grid(row=3, column=0, sticky="w")
entry_numer_domu = tk.Entry(root)
entry_numer_domu.grid(row=3, column=1)

tk.Label(root, text="Miasto:").grid(row=4, column=0, sticky="w")
entry_miasto = tk.Entry(root)
entry_miasto.grid(row=4, column=1)

#przycisk zatwierdzający
submit_button = tk.Button(root, text="Zatwierdź", command=submit_data)
submit_button.grid(row=5, columnspan=2)

#tabela do wyświetlania danych
columns = ("Imię", "Nazwisko", "Ulica", "Numer domu", "Miasto")
table = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    table.heading(col, text=col)
table.grid(row=6, columnspan=2)

#przycisk do ręcznego odświeżania tabeli
load_button = tk.Button(root, text="Wczytaj dane", command=show_table)
load_button.grid(row=7, columnspan=2)

#pole do wyszukiwania
tk.Label(root, text="Szukaj po nazwisku:").grid(row=8, column=0, sticky="w")
entry_szukaj = tk.Entry(root)
entry_szukaj.grid(row=8, column=1)

#przycisk szukaj
szukaj_button = tk.Button(root, text="Szukaj", command=szukaj)
szukaj_button.grid(row=9, columnspan=2)

#przycisk statystyki
statystyki_button = tk.Button(root, text="Statystyki", command=statystyki)
statystyki_button.grid(row=10, columnspan=2)

#pokazanie danych na starcie
show_table()

root.mainloop()

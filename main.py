from tkinter import *
from tkinter import messagebox
import tkintermapview
import requests
from bs4 import BeautifulSoup
from tkinter import TclError

employees: list = []
place: list = []
clients: list = []


class Employee:
    def __init__(self, name, surname, location, staz, associated_place=None):
        self.name = name
        self.surname = surname
        self.location = location
        self.staz = staz
        self.associated_place = associated_place
        self.coordinates = self.get_coordinates()

    def get_coordinates(self) -> list:
        try:
            adres_url: str = f'https://pl.wikipedia.org/wiki/{self.location}'
            response = requests.get(adres_url)
            response.raise_for_status()
            response_html = BeautifulSoup(response.text, 'html.parser')
            lat = response_html.select('.latitude')
            lon = response_html.select('.longitude')
            if len(lat) > 1 and len(lon) > 1:
                return [
                    float(lat[1].text.replace(',', '.')),
                    float(lon[1].text.replace(',', '.')),
                ]
            else:
                return [52.23, 21.00]
        except (requests.RequestException, IndexError, ValueError):
            return [52.23, 21.00]

    def __eq__(self, other):
        return self.name == other.name and self.surname == other.surname and self.staz == other.staz


class Place:
    def __init__(self, placowka, lokalizacja, telefon, godzinyotwarcia):
        self.placowka = placowka
        self.lokalizacja = lokalizacja
        self.telefon = telefon
        self.godzinyotwarcia = godzinyotwarcia
        self.coordinates = self.get_coordinates()

    def get_coordinates(self) -> list:
        try:
            adres_url: str = f'https://pl.wikipedia.org/wiki/{self.lokalizacja}'
            response = requests.get(adres_url)
            response.raise_for_status()
            response_html = BeautifulSoup(response.text, 'html.parser')
            lat = response_html.select('.latitude')
            lon = response_html.select('.longitude')
            if len(lat) > 1 and len(lon) > 1:
                return [
                    float(lat[1].text.replace(',', '.')),
                    float(lon[1].text.replace(',', '.')),
                ]
            else:
                return [52.23, 21.00]
        except (requests.RequestException, IndexError, ValueError):
            return [52.23, 21.00]

    def __eq__(self, other):
        return self.placowka == other.placowka


class Client:
    def __init__(self, name, surname, location, contact_number, associated_place=None):
        self.name = name
        self.surname = surname
        self.location = location
        self.contact_number = contact_number
        self.associated_place = associated_place
        self.coordinates = self.get_coordinates()

    def get_coordinates(self) -> list:
        try:
            adres_url: str = f'https://pl.wikipedia.org/wiki/{self.location}'
            response = requests.get(adres_url)
            response.raise_for_status()
            response_html = BeautifulSoup(response.text, 'html.parser')
            lat = response_html.select('.latitude')
            lon = response_html.select('.longitude')
            if len(lat) > 1 and len(lon) > 1:
                return [
                    float(lat[1].text.replace(',', '.')),
                    float(lon[1].text.replace(',', '.')),
                ]
            else:
                return [52.23, 21.00]
        except (requests.RequestException, IndexError, ValueError):
            return [52.23, 21.00]

    def __eq__(self, other):
        return self.name == other.name and self.surname == other.surname and self.associated_place == other.associated_place


def add_user() -> None:
    name = entry_imie.get()
    surname = entry_nazwisko.get()
    location = entry_miejscowosc.get()
    staz = entry_staz.get()
    place_name = var_place.get()

    if not name or not surname or not location or not staz:
        messagebox.showerror("Błąd", "Wszystkie pola muszą być wypełnione!")
        return

    associated_place = next((p for p in place if p.placowka == place_name), None)
    if not associated_place and place_name != "Brak":
        messagebox.showerror("Błąd", "Wybrana placówka nie istnieje!")
        return

    user = Employee(name=name, surname=surname, location=location, staz=staz, associated_place=associated_place)
    employees.append(user)

    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_miejscowosc.delete(0, END)
    entry_staz.delete(0, END)
    var_place.set("Brak")

    entry_imie.focus()
    show_users()


def show_users():
    listbox_lista_obiektow.delete(0, END)
    for idx, user in enumerate(employees):
        place_name = user.associated_place.placowka if user.associated_place else "Brak"
        listbox_lista_obiektow.insert(idx, f'{idx + 1}. {user.name} {user.surname} ({place_name})')


def remove_user():
    i = listbox_lista_obiektow.index(ACTIVE)
    employees.pop(i)
    show_users()


def edit_user():
    i = listbox_lista_obiektow.index(ACTIVE)
    name = employees[i].name
    surname = employees[i].surname
    location = employees[i].location
    staz = employees[i].staz
    place_name = employees[i].associated_place.placowka if employees[i].associated_place else "Brak"

    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_miejscowosc.delete(0, END)
    entry_staz.delete(0, END)
    var_place.set(place_name)

    entry_imie.insert(0, name)
    entry_nazwisko.insert(0, surname)
    entry_miejscowosc.insert(0, location)
    entry_staz.insert(0, staz)

    button_dodaj_obiekt.config(text='Zapisz', command=lambda: update_user(i))


def update_user(i):
    name = entry_imie.get()
    surname = entry_nazwisko.get()
    location = entry_miejscowosc.get()
    staz = entry_staz.get()
    place_name = var_place.get()

    if not name or not surname or not location or not staz:
        messagebox.showerror("Błąd", "Wszystkie pola muszą być wypełnione!")
        return

    associated_place = next((p for p in place if p.placowka == place_name), None)
    if not associated_place and place_name != "Brak":
        messagebox.showerror("Błąd", "Wybrana placówka nie istnieje!")
        return

    employees[i].name = name
    employees[i].surname = surname
    employees[i].location = location
    employees[i].staz = staz
    employees[i].associated_place = associated_place

    employees[i].coordinates = employees[i].get_coordinates()

    show_users()
    button_dodaj_obiekt.config(text='Dodaj', command=add_user)

    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_miejscowosc.delete(0, END)
    entry_staz.delete(0, END)
    var_place.set("Brak")

    entry_imie.focus()


def show_user_details():
    i = listbox_lista_obiektow.index(ACTIVE)
    label_szczegoly_obiektu_name_wartosc.config(text=employees[i].name)
    label_szczegoly_obiektu_surname_wartosc.config(text=employees[i].surname)
    label_szczegoly_obiektu_miejscowosc_wartosc.config(text=employees[i].location)
    label_szczegoly_obiektu_staz_wartosc.config(text=employees[i].staz)
    place_name = employees[i].associated_place.placowka if employees[i].associated_place else "Brak"
    label_szczegoly_obiektu_place_wartosc.config(text=place_name)

    map_widget.set_position(employees[i].coordinates[0], employees[i].coordinates[1])
    map_widget.set_zoom(15)


def add_placowka() -> None:
    placowka = entry_placowka.get()
    lokalizacja = entry_lokalizacja.get()
    telefon = entry_telefon.get()
    godzinyotwarcia = entry_godzinyotwarcia.get()

    if not placowka or not lokalizacja or not telefon or not godzinyotwarcia:
        messagebox.showerror("Błąd", "Wszystkie pola muszą być wypełnione!")
        return

    plac = Place(placowka=placowka, lokalizacja=lokalizacja, telefon=telefon, godzinyotwarcia=godzinyotwarcia)
    place.append(plac)
    update_place_dropdowns()
    print(place)

    entry_placowka.delete(0, END)
    entry_lokalizacja.delete(0, END)
    entry_telefon.delete(0, END)
    entry_godzinyotwarcia.delete(0, END)

    entry_placowka.focus()
    show_placowki()


def show_placowki():
    listbox_lista_placowek.delete(0, END)
    for idx, plac in enumerate(place):
        listbox_lista_placowek.insert(idx, f'{idx + 1}. {plac.placowka}')


def remove_placowka():
    i = listbox_lista_placowek.index(ACTIVE)
    associated_users = [u for u in employees if u.associated_place == place[i]]
    associated_clients = [c for c in clients if c.associated_place == place[i]]
    if associated_users or associated_clients:
        messagebox.showerror("Błąd", "Nie można usunąć placówki, która ma przypisanych pracowników lub klientów!")
        return
    place.pop(i)
    update_place_dropdowns()
    show_placowki()


def edit_placowka():
    i = listbox_lista_placowek.index(ACTIVE)
    placowka = place[i].placowka
    lokalizacja = place[i].lokalizacja
    telefon = place[i].telefon
    godzinyotwarcia = place[i].godzinyotwarcia

    entry_placowka.delete(0, END)
    entry_lokalizacja.delete(0, END)
    entry_telefon.delete(0, END)
    entry_godzinyotwarcia.delete(0, END)

    entry_placowka.insert(0, placowka)
    entry_lokalizacja.insert(0, lokalizacja)
    entry_telefon.insert(0, telefon)
    entry_godzinyotwarcia.insert(0, godzinyotwarcia)

    button_dodaj_placowke.config(text='Zapisz', command=lambda: update_placowka(i))


def update_placowka(i):
    placowka = entry_placowka.get()
    lokalizacja = entry_lokalizacja.get()
    telefon = entry_telefon.get()
    godzinyotwarcia = entry_godzinyotwarcia.get()

    if not placowka or not lokalizacja or not telefon or not godzinyotwarcia:
        messagebox.showerror("Błąd", "Wszystkie pola muszą być wypełnione!")
        return

    place[i].placowka = placowka
    place[i].lokalizacja = lokalizacja
    place[i].telefon = telefon
    place[i].godzinyotwarcia = godzinyotwarcia

    place[i].coordinates = place[i].get_coordinates()

    update_place_dropdowns()
    show_placowki()
    button_dodaj_placowke.config(text='Dodaj', command=add_placowka)

    entry_placowka.delete(0, END)
    entry_lokalizacja.delete(0, END)
    entry_telefon.delete(0, END)
    entry_godzinyotwarcia.delete(0, END)

    entry_placowka.focus()


def show_placowka_details():
    i = listbox_lista_placowek.index(ACTIVE)
    label_szczegoly_obiektu_placowka_wartosc.config(text=place[i].placowka)
    label_szczegoly_obiektu_lokalizacja_wartosc.config(text=place[i].lokalizacja)
    label_szczegoly_obiektu_telefon_wartosc.config(text=place[i].telefon)
    label_szczegoly_obiektu_godzinyotwarcia_wartosc.config(text=place[i].godzinyotwarcia)

    map_widget.set_position(place[i].coordinates[0], place[i].coordinates[1])
    map_widget.set_zoom(15)


def add_client() -> None:
    name = entry_client_name.get()
    surname = entry_client_surname.get()
    location = entry_client_location.get()
    contact_number = entry_client_contact.get()
    place_name = var_client_place.get()

    if not name or not surname or not location or not contact_number:
        messagebox.showerror("Błąd", "Wszystkie pola muszą być wypełnione!")
        return

    associated_place = next((p for p in place if p.placowka == place_name), None)
    if not associated_place and place_name != "Brak":
        messagebox.showerror("Błąd", "Wybrana placówka nie istnieje!")
        return

    client = Client(name=name, surname=surname, location=location, contact_number=contact_number,
                    associated_place=associated_place)
    clients.append(client)

    entry_client_name.delete(0, END)
    entry_client_surname.delete(0, END)
    entry_client_location.delete(0, END)
    entry_client_contact.delete(0, END)
    var_client_place.set("Brak")

    entry_client_name.focus()
    show_clients()


def show_clients():
    listbox_lista_klientow.delete(0, END)
    for idx, client in enumerate(clients):
        place_name = client.associated_place.placowka if client.associated_place else "Brak"
        listbox_lista_klientow.insert(idx, f'{idx + 1}. {client.name} {client.surname} ({place_name})')


def remove_client():
    i = listbox_lista_klientow.index(ACTIVE)
    clients.pop(i)
    show_clients()


def edit_client():
    i = listbox_lista_klientow.index(ACTIVE)
    name = clients[i].name
    surname = clients[i].surname
    location = clients[i].location
    contact_number = clients[i].contact_number
    place_name = clients[i].associated_place.placowka if clients[i].associated_place else "Brak"

    entry_client_name.delete(0, END)
    entry_client_surname.delete(0, END)
    entry_client_location.delete(0, END)
    entry_client_contact.delete(0, END)
    var_client_place.set(place_name)

    entry_client_name.insert(0, name)
    entry_client_surname.insert(0, surname)
    entry_client_location.insert(0, location)
    entry_client_contact.insert(0, contact_number)

    button_dodaj_klienta.config(text='Zapisz', command=lambda: update_client(i))


def update_client(i):
    name = entry_client_name.get()
    surname = entry_client_surname.get()
    location = entry_client_location.get()
    contact_number = entry_client_contact.get()
    place_name = var_client_place.get()

    if not name or not surname or not location or not contact_number:
        messagebox.showerror("Błąd", "Wszystkie pola muszą być wypełnione!")
        return

    associated_place = next((p for p in place if p.placowka == place_name), None)
    if not associated_place and place_name != "Brak":
        messagebox.showerror("Błąd", "Wybrana placówka nie istnieje!")
        return

    clients[i].name = name
    clients[i].surname = surname
    clients[i].location = location
    clients[i].contact_number = contact_number
    clients[i].associated_place = associated_place

    clients[i].coordinates = clients[i].get_coordinates()

    show_clients()
    button_dodaj_klienta.config(text='Dodaj', command=add_client)

    entry_client_name.delete(0, END)
    entry_client_surname.delete(0, END)
    entry_client_location.delete(0, END)
    entry_client_contact.delete(0, END)
    var_client_place.set("Brak")

    entry_client_name.focus()


def show_client_details():
    i = listbox_lista_klientow.index(ACTIVE)
    label_szczegoly_klienta_name_wartosc.config(text=clients[i].name)
    label_szczegoly_klienta_surname_wartosc.config(text=clients[i].surname)
    label_szczegoly_klienta_location_wartosc.config(text=clients[i].location)
    label_szczegoly_klienta_contact_wartosc.config(text=clients[i].contact_number)
    place_name = clients[i].associated_place.placowka if clients[i].associated_place else "Brak"
    label_szczegoly_klienta_place_wartosc.config(text=place_name)

    map_widget.set_position(clients[i].coordinates[0], clients[i].coordinates[1])
    map_widget.set_zoom(15)


def update_place_dropdowns():
    place_names = ["Brak"] + [p.placowka for p in place]
    menu = option_menu_place["menu"]
    menu.delete(0, "end")
    for name in place_names:
        menu.add_command(label=name, command=lambda value=name: var_place.set(value))
    var_place.set("Brak")

    menu_client = option_menu_client_place["menu"]
    menu_client.delete(0, "end")
    for name in place_names:
        menu_client.add_command(label=name, command=lambda value=name: var_client_place.set(value))
    var_client_place.set("Brak")


def generate_map_all_shelters():
    map_widget.delete_all_marker()
    map_widget.set_zoom(5)

    for plac in place:
        map_widget.set_marker(
            plac.coordinates[0],
            plac.coordinates[1],
            text=f"{plac.placowka}"
        )

def generate_map_all_employees():
    map_widget.delete_all_marker()
    map_widget.set_zoom(5)
    for user in employees:
        map_widget.set_marker(
            user.coordinates[0],
            user.coordinates[1],
            text=f"{user.name} {user.surname}"
        )


def generate_map_users_selected_shelter():
    map_widget.delete_all_marker()
    map_widget.set_zoom(5)
    if not listbox_lista_placowek.curselection():
        messagebox.showerror("Błąd", "Wybierz placówkę z listy!")
        return
    i = listbox_lista_placowek.index(ACTIVE)
    selected_place = place[i]
    associated_users = [c for c in clients if c.associated_place == selected_place]
    for user in associated_users:
        map_widget.set_marker(
            user.coordinates[0],
            user.coordinates[1],
            text=f"{user.name} {user.surname}"
        )


def generate_map_employees_selected_shelter():
    map_widget.delete_all_marker()
    map_widget.set_zoom(5)
    if not listbox_lista_placowek.curselection():
        messagebox.showerror("Błąd", "Wybierz placówkę z listy!")
        return
    i = listbox_lista_placowek.index(ACTIVE)
    selected_place = place[i]
    associated_users = [e for e in employees if e.associated_place == selected_place]
    for user in associated_users:
        map_widget.set_marker(
            user.coordinates[0],
            user.coordinates[1],
            text=f"{user.name} {user.surname}"
        )


def generate_map_clients_selected_shelter():
    map_widget.delete_all_marker()
    map_widget.set_zoom(5)
    if not listbox_lista_placowek.curselection():
        messagebox.showerror("Błąd", "Wybierz placówkę z listy!")
        return
    i = listbox_lista_placowek.index(ACTIVE)
    selected_place = place[i]
    associated_users = [e for e in clients if e.associated_place == selected_place]
    for user in associated_users:
        map_widget.set_marker(
            user.coordinates[0],
            user.coordinates[1],
            text=f"{user.name} {user.surname}"
        )


root = Tk()
root.geometry("1500x1000")
root.title('Projekt-baza schroniska')

# Frames for Users
ramka_lista_obiektow = Frame(root)
ramka_formularz = Frame(root)
ramka_szczegoly_obiektow = Frame(root)
ramka_mapa = Frame(root)

ramka_lista_obiektow.grid(row=4, column=0, sticky="nsew")
ramka_formularz.grid(row=4, column=1, sticky="nsew")
ramka_szczegoly_obiektow.grid(row=5, column=0, columnspan=2, sticky="nsew")
ramka_mapa.grid(row=0, column=2, rowspan=6, sticky="nsew")

# Frames for Clients
ramka_lista_klientow = Frame(root)
ramka_formularz_klientow = Frame(root)
ramka_szczegoly_klientow = Frame(root)

ramka_lista_klientow.grid(row=2, column=0, sticky="nsew")
ramka_formularz_klientow.grid(row=2, column=1, sticky="nsew")
ramka_szczegoly_klientow.grid(row=3, column=0, columnspan=2, sticky="nsew")

# Frames for Places
ramka_lista_placowek = Frame(root)
ramka_formularz_placowek = Frame(root)
ramka_szczegoly_placowek = Frame(root)

ramka_lista_placowek.grid(row=0, column=0, sticky="nsew")
ramka_formularz_placowek.grid(row=0, column=1, sticky="nsew")
ramka_szczegoly_placowek.grid(row=1, column=0, columnspan=2, sticky="nsew")

# ramka_lista_obiektow (Users)
label_lista_obiektow = Label(ramka_lista_obiektow, text='Lista użytkowników:')
label_lista_obiektow.grid(row=0, column=0)

listbox_lista_obiektow = Listbox(ramka_lista_obiektow, width=50, height=10)
listbox_lista_obiektow.grid(row=1, column=0, columnspan=3)

button_pokaz_szczegoly = Button(ramka_lista_obiektow, text='Pokaż szczegóły', command=show_user_details)
button_pokaz_szczegoly.grid(row=2, column=0)
button_usun_obiekt = Button(ramka_lista_obiektow, text='Usuń', command=remove_user)
button_usun_obiekt.grid(row=2, column=1)
button_edytuj_obiekt = Button(ramka_lista_obiektow, text='Edytuj', command=edit_user)
button_edytuj_obiekt.grid(row=2, column=2)

# ramka_formularz (Users)
label_formularz = Label(ramka_formularz, text='Formularz pracowników schroniska:')
label_formularz.grid(row=0, column=0)

label_imie = Label(ramka_formularz, text='Imię:')
label_imie.grid(row=1, column=0, sticky=W)
label_nazwisko = Label(ramka_formularz, text='Nazwisko:')
label_nazwisko.grid(row=2, column=0, sticky=W)
label_miejscowosc = Label(ramka_formularz, text='Miejscowość:')
label_miejscowosc.grid(row=3, column=0, sticky=W)
label_staz = Label(ramka_formularz, text='Staż w schronisku:')
label_staz.grid(row=4, column=0, sticky=W)
label_place = Label(ramka_formularz, text='Placówka:')
label_place.grid(row=5, column=0, sticky=W)

entry_imie = Entry(ramka_formularz)
entry_imie.grid(row=1, column=1)
entry_nazwisko = Entry(ramka_formularz)
entry_nazwisko.grid(row=2, column=1)
entry_miejscowosc = Entry(ramka_formularz)
entry_miejscowosc.grid(row=3, column=1)
entry_staz = Entry(ramka_formularz)
entry_staz.grid(row=4, column=1)

var_place = StringVar(value="Brak")
option_menu_place = OptionMenu(ramka_formularz, var_place, "Brak")
option_menu_place.grid(row=5, column=1)

button_dodaj_obiekt = Button(ramka_formularz, text='Dodaj', command=add_user)
button_dodaj_obiekt.grid(row=6, column=0, columnspan=2)

button_mapa_wszyscy_uzytkownicy = Button(ramka_formularz, text='Mapa wszystkich użytkowników',
                                         command=generate_map_all_employees)
button_mapa_wszyscy_uzytkownicy.grid(row=7, column=0, columnspan=2)

# ramka_szczegoly_obiektow (Users)
label_pokaz_szczegoly = Label(ramka_szczegoly_obiektow, text='Szczegóły użytkownika:')
label_pokaz_szczegoly.grid(row=0, column=0)

label_szczegoly_obiektu_name = Label(ramka_szczegoly_obiektow, text='Imię: ')
label_szczegoly_obiektu_name.grid(row=1, column=0)
label_szczegoly_obiektu_name_wartosc = Label(ramka_szczegoly_obiektow, text='....')
label_szczegoly_obiektu_name_wartosc.grid(row=1, column=1)

label_szczegoly_obiektu_surname = Label(ramka_szczegoly_obiektow, text='Nazwisko: ')
label_szczegoly_obiektu_surname.grid(row=1, column=2)
label_szczegoly_obiektu_surname_wartosc = Label(ramka_szczegoly_obiektow, text='....')
label_szczegoly_obiektu_surname_wartosc.grid(row=1, column=3)

label_szczegoly_obiektu_miejscowosc = Label(ramka_szczegoly_obiektow, text='Miejscowość: ')
label_szczegoly_obiektu_miejscowosc.grid(row=1, column=4)
label_szczegoly_obiektu_miejscowosc_wartosc = Label(ramka_szczegoly_obiektow, text='....')
label_szczegoly_obiektu_miejscowosc_wartosc.grid(row=1, column=5)

label_szczegoly_obiektu_staz = Label(ramka_szczegoly_obiektow, text='Długość stażu (w latach): ')
label_szczegoly_obiektu_staz.grid(row=1, column=6)
label_szczegoly_obiektu_staz_wartosc = Label(ramka_szczegoly_obiektow, text='....')
label_szczegoly_obiektu_staz_wartosc.grid(row=1, column=7)

label_szczegoly_obiektu_place = Label(ramka_szczegoly_obiektow, text='Placówka: ')
label_szczegoly_obiektu_place.grid(row=1, column=8)
label_szczegoly_obiektu_place_wartosc = Label(ramka_szczegoly_obiektow, text='....')
label_szczegoly_obiektu_place_wartosc.grid(row=1, column=9)

# ramka_lista_klientow (Clients)
label_lista_klientow = Label(ramka_lista_klientow, text='Lista klientów:')
label_lista_klientow.grid(row=0, column=0)

listbox_lista_klientow = Listbox(ramka_lista_klientow, width=50, height=10)
listbox_lista_klientow.grid(row=1, column=0, columnspan=3)

button_pokaz_szczegoly_klienta = Button(ramka_lista_klientow, text='Pokaż szczegóły', command=show_client_details)
button_pokaz_szczegoly_klienta.grid(row=2, column=0)
button_usun_klienta = Button(ramka_lista_klientow, text='Usuń', command=remove_client)
button_usun_klienta.grid(row=2, column=1)
button_edytuj_klienta = Button(ramka_lista_klientow, text='Edytuj', command=edit_client)
button_edytuj_klienta.grid(row=2, column=2)

# ramka_formularz_klientow (Clients)
label_formularz_klientow = Label(ramka_formularz_klientow, text='Formularz klientów:')
label_formularz_klientow.grid(row=0, column=0)

label_client_name = Label(ramka_formularz_klientow, text='Imię:')
label_client_name.grid(row=1, column=0, sticky=W)
label_client_surname = Label(ramka_formularz_klientow, text='Nazwisko:')
label_client_surname.grid(row=2, column=0, sticky=W)
label_client_location = Label(ramka_formularz_klientow, text='Miejscowość:')
label_client_location.grid(row=3, column=0, sticky=W)
label_client_contact = Label(ramka_formularz_klientow, text='Numer kontaktowy:')
label_client_contact.grid(row=4, column=0, sticky=W)
label_client_place = Label(ramka_formularz_klientow, text='Placówka:')
label_client_place.grid(row=5, column=0, sticky=W)

entry_client_name = Entry(ramka_formularz_klientow)
entry_client_name.grid(row=1, column=1)
entry_client_surname = Entry(ramka_formularz_klientow)
entry_client_surname.grid(row=2, column=1)
entry_client_location = Entry(ramka_formularz_klientow)
entry_client_location.grid(row=3, column=1)
entry_client_contact = Entry(ramka_formularz_klientow)
entry_client_contact.grid(row=4, column=1)

var_client_place = StringVar(value="Brak")
option_menu_client_place = OptionMenu(ramka_formularz_klientow, var_client_place, "Brak")
option_menu_client_place.grid(row=5, column=1)

button_dodaj_klienta = Button(ramka_formularz_klientow, text='Dodaj', command=add_client)
button_dodaj_klienta.grid(row=6, column=0, columnspan=2)

# ramka_szczegoly_klientow (Clients)
label_pokaz_szczegoly_klientow = Label(ramka_szczegoly_klientow, text='Szczegóły klienta:')
label_pokaz_szczegoly_klientow.grid(row=0, column=0)

label_szczegoly_klienta_name = Label(ramka_szczegoly_klientow, text='Imię: ')
label_szczegoly_klienta_name.grid(row=1, column=0)
label_szczegoly_klienta_name_wartosc = Label(ramka_szczegoly_klientow, text='....')
label_szczegoly_klienta_name_wartosc.grid(row=1, column=1)

label_szczegoly_klienta_surname = Label(ramka_szczegoly_klientow, text='Nazwisko: ')
label_szczegoly_klienta_surname.grid(row=1, column=2)
label_szczegoly_klienta_surname_wartosc = Label(ramka_szczegoly_klientow, text='....')
label_szczegoly_klienta_surname_wartosc.grid(row=1, column=3)

label_szczegoly_klienta_location = Label(ramka_szczegoly_klientow, text='Miejscowość: ')
label_szczegoly_klienta_location.grid(row=1, column=4)
label_szczegoly_klienta_location_wartosc = Label(ramka_szczegoly_klientow, text='....')
label_szczegoly_klienta_location_wartosc.grid(row=1, column=5)

label_szczegoly_klienta_contact = Label(ramka_szczegoly_klientow, text='Numer kontaktowy: ')
label_szczegoly_klienta_contact.grid(row=1, column=6)
label_szczegoly_klienta_contact_wartosc = Label(ramka_szczegoly_klientow, text='....')
label_szczegoly_klienta_contact_wartosc.grid(row=1, column=7)

label_szczegoly_klienta_place = Label(ramka_szczegoly_klientow, text='Placówka: ')
label_szczegoly_klienta_place.grid(row=1, column=8)
label_szczegoly_klienta_place_wartosc = Label(ramka_szczegoly_klientow, text='....')
label_szczegoly_klienta_place_wartosc.grid(row=1, column=9)

# ramka_lista_placowek (Places)
label_lista_placowek = Label(ramka_lista_placowek, text='Lista placówek:')
label_lista_placowek.grid(row=0, column=0)

listbox_lista_placowek = Listbox(ramka_lista_placowek, width=50, height=10)
listbox_lista_placowek.grid(row=1, column=0, columnspan=3)

button_pokaz_szczegoly_placowek = Button(ramka_lista_placowek, text='Pokaż szczegóły', command=show_placowka_details)
button_pokaz_szczegoly_placowek.grid(row=2, column=0)
button_usun_placowke = Button(ramka_lista_placowek, text='Usuń', command=remove_placowka)
button_usun_placowke.grid(row=2, column=1)
button_edytuj_placowke = Button(ramka_lista_placowek, text='Edytuj', command=edit_placowka)
button_edytuj_placowke.grid(row=2, column=2)

# ramka_formularz_placowek (Places)
label_formularz_placowek = Label(ramka_formularz_placowek, text='Formularz placówek:')
label_formularz_placowek.grid(row=0, column=0)

label_placowka = Label(ramka_formularz_placowek, text='Nazwa:')
label_placowka.grid(row=1, column=0, sticky=W)
label_lokalizacja = Label(ramka_formularz_placowek, text='Lokalizacja:')
label_lokalizacja.grid(row=2, column=0, sticky=W)
label_telefon = Label(ramka_formularz_placowek, text='Numer kontaktowy:')
label_telefon.grid(row=3, column=0, sticky=W)
label_godzinyotwarcia = Label(ramka_formularz_placowek, text='Godziny otwarcia:')
label_godzinyotwarcia.grid(row=4, column=0, sticky=W)

entry_placowka = Entry(ramka_formularz_placowek)
entry_placowka.grid(row=1, column=1)
entry_lokalizacja = Entry(ramka_formularz_placowek)
entry_lokalizacja.grid(row=2, column=1)
entry_telefon = Entry(ramka_formularz_placowek)
entry_telefon.grid(row=3, column=1)
entry_godzinyotwarcia = Entry(ramka_formularz_placowek)
entry_godzinyotwarcia.grid(row=4, column=1)

button_dodaj_placowke = Button(ramka_formularz_placowek, text='Dodaj', command=add_placowka)
button_dodaj_placowke.grid(row=5, column=0, columnspan=2)

button_mapa_wszystkich_schronisk = Button(ramka_formularz_placowek, text='Mapa wszystkich schronisk',
                                          command=generate_map_all_shelters)
button_mapa_wszystkich_schronisk.grid(row=6, column=0, columnspan=2)

button_mapa_pracownikow = Button(ramka_formularz_placowek, text='Mapa pracowników schroniska',
                                 command=generate_map_employees_selected_shelter)
button_mapa_pracownikow.grid(row=7, column=0, columnspan=2)

button_mapa_uzytkownikow = Button(ramka_formularz_placowek, text='Mapa klientów schroniska',
                                  command=generate_map_users_selected_shelter)
button_mapa_uzytkownikow.grid(row=8, column=0, columnspan=2)

# ramka_szczegoly_placowek (Places Details)
label_pokaz_szczegoly_placowek = Label(ramka_szczegoly_placowek, text='Informacje o placówce:')
label_pokaz_szczegoly_placowek.grid(row=0, column=0)

label_szczegoly_obiektu_placowka = Label(ramka_szczegoly_placowek, text='Placówka: ')
label_szczegoly_obiektu_placowka.grid(row=1, column=0)
label_szczegoly_obiektu_placowka_wartosc = Label(ramka_szczegoly_placowek, text='....')
label_szczegoly_obiektu_placowka_wartosc.grid(row=1, column=1)

label_szczegoly_obiektu_lokalizacja = Label(ramka_szczegoly_placowek, text='Lokalizacja: ')
label_szczegoly_obiektu_lokalizacja.grid(row=1, column=2)
label_szczegoly_obiektu_lokalizacja_wartosc = Label(ramka_szczegoly_placowek, text='....')
label_szczegoly_obiektu_lokalizacja_wartosc.grid(row=1, column=3)

label_szczegoly_obiektu_telefon = Label(ramka_szczegoly_placowek, text='Numer kontaktowy: ')
label_szczegoly_obiektu_telefon.grid(row=1, column=4)
label_szczegoly_obiektu_telefon_wartosc = Label(ramka_szczegoly_placowek, text='....')
label_szczegoly_obiektu_telefon_wartosc.grid(row=1, column=5)

label_szczegoly_obiektu_godzinyotwarcia = Label(ramka_szczegoly_placowek, text='Godziny otwarcia: ')
label_szczegoly_obiektu_godzinyotwarcia.grid(row=1, column=6)
label_szczegoly_obiektu_godzinyotwarcia_wartosc = Label(ramka_szczegoly_placowek, text='....')
label_szczegoly_obiektu_godzinyotwarcia_wartosc.grid(row=1, column=7)

# ramka_mapa (Shared Map for Users, Clients, and Places)
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=500, height=600, corner_radius=0)
map_widget.grid(row=0, column=0, sticky="nsew")
map_widget.set_position(52.23, 21.00)
map_widget.set_zoom(5)

# Initialize dropdowns
update_place_dropdowns()


root.mainloop()
from tkinter import *
import tkintermapview
import requests
from bs4 import BeautifulSoup

users: list = []
place: list = []
clients: list = []

class User:
    def __init__(self, name, surname, location, staz):
        self.name = name
        self.surname = surname
        self.location = location
        self.staz = staz
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1],
                                            text=f'{self.name} {self.surname}')

    def get_coordinates(self) -> list:
        adres_url: str = f'https://pl.wikipedia.org/wiki/{self.location}'
        response_html = BeautifulSoup(requests.get(adres_url).text, 'html.parser')
        return [
            float(response_html.select('.latitude')[1].text.replace(',', '.')),
            float(response_html.select('.longitude')[1].text.replace(',', '.')),
        ]

class Place:
    def __init__(self, placowka, lokalizacja, telefon, godzinyotwarcia):
        self.placowka = placowka
        self.lokalizacja = lokalizacja
        self.telefon = telefon
        self.godzinyotwarcia = godzinyotwarcia
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1],
                                            text=f'{self.placowka}')

    def get_coordinates(self) -> list:
        adres_url: str = f'https://pl.wikipedia.org/wiki/{self.lokalizacja}'
        response_html = BeautifulSoup(requests.get(adres_url).text, 'html.parser')
        return [
            float(response_html.select('.latitude')[1].text.replace(',', '.')),
            float(response_html.select('.longitude')[1].text.replace(',', '.')),
        ]

class Client:
    def __init__(self, name, surname, location, contact_number):
        self.name = name
        self.surname = surname
        self.location = location
        self.contact_number = contact_number
        self.coordinates = self.get_coordinates()
        self.marker = map_widget.set_marker(self.coordinates[0], self.coordinates[1],
                                            text=f'{self.name} {self.surname}')

    def get_coordinates(self) -> list:
        adres_url: str = f'https://pl.wikipedia.org/wiki/{self.location}'
        response_html = BeautifulSoup(requests.get(adres_url).text, 'html.parser')
        return [
            float(response_html.select('.latitude')[1].text.replace(',', '.')),
            float(response_html.select('.longitude')[1].text.replace(',', '.')),
        ]

def add_user() -> None:
    name = entry_imie.get()
    surname = entry_nazwisko.get()
    location = entry_miejscowosc.get()
    staz = entry_staz.get()

    user = User(name=name, surname=surname, location=location, staz=staz)
    users.append(user)
    print(users)

    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_miejscowosc.delete(0, END)
    entry_staz.delete(0, END)

    entry_imie.focus()
    show_users()

def show_users():
    listbox_lista_obiektow.delete(0, END)
    for idx, user in enumerate(users):
        listbox_lista_obiektow.insert(idx, f'{idx + 1}. {user.name} {user.surname}')

def remove_user():
    i = listbox_lista_obiektow.index(ACTIVE)
    users[i].marker.delete()
    users.pop(i)
    show_users()

def edit_user():
    i = listbox_lista_obiektow.index(ACTIVE)
    name = users[i].name
    surname = users[i].surname
    location = users[i].location
    staz = users[i].staz

    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_miejscowosc.delete(0, END)
    entry_staz.delete(0, END)

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

    users[i].name = name
    users[i].surname = surname
    users[i].location = location
    users[i].staz = staz

    users[i].coordinates = users[i].get_coordinates()
    users[i].marker.delete()
    users[i].marker = map_widget.set_marker(users[i].coordinates[0], users[i].coordinates[1],
                                            text=f'{users[i].name} {users[i].surname}')

    show_users()
    button_dodaj_obiekt.config(text='Dodaj', command=add_user)

    entry_imie.delete(0, END)
    entry_nazwisko.delete(0, END)
    entry_miejscowosc.delete(0, END)
    entry_staz.delete(0, END)

    entry_imie.focus()

def show_user_details():
    i = listbox_lista_obiektow.index(ACTIVE)
    label_szczegoly_obiektu_name_wartosc.config(text=users[i].name)
    label_szczegoly_obiektu_surname_wartosc.config(text=users[i].surname)
    label_szczegoly_obiektu_miejscowosc_wartosc.config(text=users[i].location)
    label_szczegoly_obiektu_staz_wartosc.config(text=users[i].staz)

    map_widget.set_zoom(15)
    map_widget.set_position(users[i].coordinates[0], users[i].coordinates[1])

def add_placowka() -> None:
    placowka = entry_placowka.get()
    lokalizacja = entry_lokalizacja.get()
    telefon = entry_telefon.get()
    godzinyotwarcia = entry_godzinyotwarcia.get()

    plac = Place(placowka=placowka, lokalizacja=lokalizacja, telefon=telefon, godzinyotwarcia=godzinyotwarcia)
    place.append(plac)
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
    place[i].marker.delete()
    place.pop(i)
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

    place[i].placowka = placowka
    place[i].lokalizacja = lokalizacja
    place[i].telefon = telefon
    place[i].godzinyotwarcia = godzinyotwarcia

    place[i].coordinates = place[i].get_coordinates()
    place[i].marker.delete()
    place[i].marker = map_widget.set_marker(place[i].coordinates[0], place[i].coordinates[1],
                                            text=f'{place[i].placowka}')

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

    map_widget.set_zoom(15)
    map_widget.set_position(place[i].coordinates[0], place[i].coordinates[1])

def add_client() -> None:
    name = entry_client_name.get()
    surname = entry_client_surname.get()
    location = entry_client_location.get()
    contact_number = entry_client_contact.get()

    client = Client(name=name, surname=surname, location=location, contact_number=contact_number)
    clients.append(client)
    print(clients)

    entry_client_name.delete(0, END)
    entry_client_surname.delete(0, END)
    entry_client_location.delete(0, END)
    entry_client_contact.delete(0, END)

    entry_client_name.focus()
    show_clients()

def show_clients():
    listbox_lista_klientow.delete(0, END)
    for idx, client in enumerate(clients):
        listbox_lista_klientow.insert(idx, f'{idx + 1}. {client.name} {client.surname}')

def remove_client():
    i = listbox_lista_klientow.index(ACTIVE)
    clients[i].marker.delete()
    clients.pop(i)
    show_clients()

def edit_client():
    i = listbox_lista_klientow.index(ACTIVE)
    name = clients[i].name
    surname = clients[i].surname
    location = clients[i].location
    contact_number = clients[i].contact_number

    entry_client_name.delete(0, END)
    entry_client_surname.delete(0, END)
    entry_client_location.delete(0, END)
    entry_client_contact.delete(0, END)

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

    clients[i].name = name
    clients[i].surname = surname
    clients[i].location = location
    clients[i].contact_number = contact_number

    clients[i].coordinates = clients[i].get_coordinates()
    clients[i].marker.delete()
    clients[i].marker = map_widget.set_marker(clients[i].coordinates[0], clients[i].coordinates[1],
                                              text=f'{clients[i].name} {clients[i].surname}')

    show_clients()
    button_dodaj_klienta.config(text='Dodaj', command=add_client)

    entry_client_name.delete(0, END)
    entry_client_surname.delete(0, END)
    entry_client_location.delete(0, END)
    entry_client_contact.delete(0, END)

    entry_client_name.focus()

def show_client_details():
    i = listbox_lista_klientow.index(ACTIVE)
    label_szczegoly_klienta_name_wartosc.config(text=clients[i].name)
    label_szczegoly_klienta_surname_wartosc.config(text=clients[i].surname)
    label_szczegoly_klienta_location_wartosc.config(text=clients[i].location)
    label_szczegoly_klienta_contact_wartosc.config(text=clients[i].contact_number)

    map_widget.set_zoom(15)
    map_widget.set_position(clients[i].coordinates[0], clients[i].coordinates[1])

root = Tk()
root.geometry("1500x1000")
root.title('Projekt-baza schroniska')

# Frames for Users
ramka_lista_obiektow = Frame(root)
ramka_formularz = Frame(root)
ramka_szczegoly_obiektow = Frame(root)
ramka_mapa = Frame(root)

ramka_lista_obiektow.grid(row=0, column=0, sticky="nsew")
ramka_formularz.grid(row=0, column=1, sticky="nsew")
ramka_szczegoly_obiektow.grid(row=1, column=0, columnspan=2, sticky="nsew")
ramka_mapa.grid(row=2, column=10, columnspan=3, sticky="nsew")

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

ramka_lista_placowek.grid(row=4, column=0, sticky="nsew")
ramka_formularz_placowek.grid(row=4, column=1, sticky="nsew")
ramka_szczegoly_placowek.grid(row=5, column=0, columnspan=2, sticky="nsew")

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

entry_imie = Entry(ramka_formularz)
entry_imie.grid(row=1, column=1)
entry_nazwisko = Entry(ramka_formularz)
entry_nazwisko.grid(row=2, column=1)
entry_miejscowosc = Entry(ramka_formularz)
entry_miejscowosc.grid(row=3, column=1)
entry_staz = Entry(ramka_formularz)
entry_staz.grid(row=4, column=1)

button_dodaj_obiekt = Button(ramka_formularz, text='Dodaj', command=add_user)
button_dodaj_obiekt.grid(row=5, column=0, columnspan=2)

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

entry_client_name = Entry(ramka_formularz_klientow)
entry_client_name.grid(row=1, column=1)
entry_client_surname = Entry(ramka_formularz_klientow)
entry_client_surname.grid(row=2, column=1)
entry_client_location = Entry(ramka_formularz_klientow)
entry_client_location.grid(row=3, column=1)
entry_client_contact = Entry(ramka_formularz_klientow)
entry_client_contact.grid(row=4, column=1)

button_dodaj_klienta = Button(ramka_formularz_klientow, text='Dodaj', command=add_client)
button_dodaj_klienta.grid(row=5, column=0, columnspan=2)

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

# ramka_szczegoly_placowek (Places)
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
map_widget = tkintermapview.TkinterMapView(ramka_mapa, width=500, height=400, corner_radius=0)
map_widget.grid(row=12, column=12, columnspan=2)
map_widget.set_position(52.23, 21.00)
map_widget.set_zoom(6)

root.mainloop()
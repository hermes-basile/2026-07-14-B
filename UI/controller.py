import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

        self.result1 = None
        self.result2 = None


    def fill_DD(self):


        self._view._ddGenre.options.clear()
        self._view._ddGenre.value = None
        self.result1 = None

        lista_da_caricare = self._model.lista_all_generi()

        # se l'elemento è formato da oggetti classe
        for elemento in lista_da_caricare:
            self._view._ddGenre.options.append(
                ft.dropdown.Option(
                    text=str(elemento),
                    data = elemento,
                    on_click=self.readResult1
                )
            )
        self._view.update_page()

    def readResult1(self, e):
        self.result1 = e.control.data

    def handleCreaGrafo(self, e):
        self._view._txt_result.controls.clear()

        genere = self.result1
        print(F"GENERE {genere}")

        if genere is None:
            self._view._txt_result.controls.append(
                ft.Text("Devi prima selezionare un opzione dal menù a tendina", color="red"))
            self._view.update_page()
            return

        self._view._txt_result.controls.append(
            ft.Text("Stiamo creando il grafo, aspetta qualche secondo.."))
        self._view.update_page()

        # Creare il grafo da model e pulire la view
        self._model.crea_grafo(genere)
        self._view._txt_result.controls.clear()

        # scrivere all'utente che è tutto ok, nodi e archi
        self._view._txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato. ", color="green"))

        self._view._txt_result.controls.append(ft.Text(
            f"Il grafo ha {self._model.num_nodi()} nodi e {self._model.num_archi()} archi."))

        self._view._btnStampaInfo.disabled = False

        self.fill_film()

        self._view.update_page()


    def fill_film(self):

        self._view._ddMovie.options.clear()
        self._view._ddMovie.value = None
        self.result2 = None

        lista_da_caricare = self._model.lista_film_completa()

        for elemento in lista_da_caricare:
            self._view._ddMovie.options.append(
                ft.dropdown.Option(
                    text=str(elemento),
                    data=elemento,
                    on_click=self.readResult2
                )
            )

    def readResult2(self, e):
        self.result2 = e.control.data



    def handleStampaInfo(self, e):
        self._view._txt_result.controls.clear()



        self._view._txt_result.controls.append(ft.Text(
            f"numero componenti connesse: {self._model.numero_componenti_connesse()} \n"))

        film,archi = self._model.film_maggiore_archi_uscenti()
        self._view._txt_result.controls.append(ft.Text(
            f"film con maggiori archi uscenti: {film} (archi uscenti:{archi}) \n"))

        lista_nodi_componente = self._model.info_componente_connessa_maggiore()



        self._view._txt_result.controls.append(ft.Text(f"La componente connessa maggiore ha {len(lista_nodi_componente)} film."))


        self._view._txt_result.controls.append(ft.Text("Le informazioni sulla componente connessa:"))

        for nodo in lista_nodi_componente:
            self._view._txt_result.controls.append(ft.Text(f"{nodo}: {nodo.numero_attori_recitanti()} attori"))

        self._view.update_page()





    def handleTrovaSelezione(self, e):
        self._view._txt_result.controls.clear()


        scelta_utente_DD = self.result2


        if scelta_utente_DD is None:
            self._view._txt_result.controls.append(ft.Text(
                "Attenzione prima di proseguire è necessario scegliere un opzione del dropdown", color="red"))
            self._view.update_page()
            return

        self._view._txt_result.controls.clear()


        txt_in = self._view._txtInN.value
        if txt_in is None or txt_in.strip() == "":
            self._view._txt_result.controls.append(ft.Text(
                "Devi inserire un valore valido", color="red"))
            self._view.update_page()
            return

        try:
            number = int(txt_in)
        except ValueError:
            self._view._txt_result.controls.append(ft.Text(
                "Attenzione, gli unici caratteri ammessi sono da 0 a 9: puoi inserire solo numeri", color="red"))
            self._view._txtInN.value = ""
            self._view.update_page()
            return

        self._view._txt_result.controls.append(ft.Text(f"Tutti i dati inseriti sono coerenti", color="green"))
        self._view.update_page()

        lista, voto = self._model.crea_ricorsione(scelta_utente_DD, number)

        lista_ordinata = self._model.ordina_listaFilm_per_titolo(lista)

        self._view._txt_result.controls.clear()

        self._view._txt_result.controls.append(ft.Text(f"Di seguito la lista ordinata di film"))
        self._view._txt_result.controls.append(ft.Text(f"\n"))

        for film in lista_ordinata:
            self._view._txt_result.controls.append(ft.Text(f""
                                                          f"{film.title} dell'anno {film.year}, con {film.numero_attori_recitanti()} attori"))

        self._view._txt_result.controls.append(ft.Text(f"Il numero di film è: {number}"))
        self._view._txt_result.controls.append(ft.Text(f"\n"))
        self._view._txt_result.controls.append(ft.Text(f"la valutazione complessiva è di {voto}"))
        self._view.update_page()










    
import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def _errore(self, msg):
        self._view.txt_result.controls.append(ft.Text(msg, color="red"))
        self._view.update_page()

    # ---------- PUNTO 1a ----------
    def fillDDGeneri(self):
        for g in self._model.getGeneri():
            self._view._ddGenere.options.append(ft.dropdown.Option(g))

    # ---------- PUNTO 1b/1c ----------
    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()

        genere = self._view._ddGenere.value
        if genere is None:
            self._errore("Selezionare un genere!")
            return

        minimo = self._view._txtVoti.value
        if minimo is None or minimo == "":
            self._errore("Inserire il numero minimo di voti!")
            return
        try:
            minimo = int(minimo)
        except ValueError:
            self._errore("Il numero minimo di voti deve essere un intero!")
            return
        if minimo < 0:
            self._errore("Il numero minimo di voti non può essere negativo!")
            return

        self._model.buildGraph(genere, minimo)
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo creato per il genere {genere} con almeno {minimo} voti!"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di vertici: {self._model.getNumNodi()}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))

        # menu "Film" per il punto 2
        self._view._ddFilm.options.clear()
        self._view._ddFilm.value = None
        for f in sorted(self._model.getNodes(), key=str):
            self._view._ddFilm.options.append(ft.dropdown.Option(key=f.id, text=str(f)))

        self._view.update_page()

    # ---------- PUNTO 1d ----------
    def handleDettagli(self, e):
        self._view.txt_result.controls.clear()

        if self._model.getNumNodi() == 0:
            self._errore("Creare prima il grafo!")
            return

        self._view.txt_result.controls.append(ft.Text("Tre archi di peso maggiore:"))
        for titolo1, titolo2, peso in self._model.getTopArchi():
            self._view.txt_result.controls.append(ft.Text(f"{titolo1} -- {titolo2} (peso: {peso})"))

        self._view.txt_result.controls.append(
            ft.Text(f"Numero di componenti connesse: {self._model.getNumComponenti()}"))

        componente = self._model.getComponenteMax()
        self._view.txt_result.controls.append(
            ft.Text(f"Componente connessa più grande: {len(componente)} film"))
        for f in componente:
            self._view.txt_result.controls.append(ft.Text(f"{f} - grado {self._model.getGrado(f)}"))

        self._view.update_page()

    # ---------- PUNTO 2 ----------
    # ---------- PUNTO 2 ----------
    def handlePercorso(self, e):
        self._view.txt_result.controls.clear()

        if self._model.getNumNodi() == 0:
            self._errore("Creare prima il grafo!")
            return
        if self._view._ddFilm.value is None:
            self._errore("Selezionare un film!")
            return
        start = self._model.idMap.get(self._view._ddFilm.value)
        if start is None:
            self._errore("Film non trovato!")
            return

        cammino, sommaVoti = self._model.getCammino(start)
        if len(cammino) <= 1:
            self._errore(f"Da {start} non si raggiunge nessun film con voto medio maggiore!")
            return

        self._view.txt_result.controls.append(ft.Text(f"Cammino a partire da {start}:"))
        for f in cammino:
            self._view.txt_result.controls.append(ft.Text(f"{f} - voto medio {f.avg_rating}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di film: {len(cammino)}"))
        self._view.txt_result.controls.append(ft.Text(f"Somma dei voti ricevuti: {sommaVoti}"))
        self._view.update_page()
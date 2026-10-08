import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self._page.title = "TdP - Film e interpreti"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._controller = None
        self.txt_result = None

    def load_interface(self):
        self._page.controls.append(
            ft.Text("TdP - imdb: film e interpreti", color="blue", size=24))

        # ---------- RIGA 1: genere + voti minimi + crea grafo + dettagli (PUNTO 1) ----------
        self._ddGenere = ft.Dropdown(label="Genere", width=200)
        self._txtVoti = ft.TextField(label="Voti minimi", width=150, value="10000")
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea grafo",
                                               on_click=self._controller.handleCreaGrafo, width=180)
        self._btnDettagli = ft.ElevatedButton(text="Stampa dettagli",
                                              on_click=self._controller.handleDettagli, width=180)
        row1 = ft.Row([self._ddGenere, self._txtVoti, self._btnCreaGrafo, self._btnDettagli],
                      alignment=ft.MainAxisAlignment.CENTER)

        # ---------- RIGA 2: film + cerca percorso (PUNTO 2) ----------
        self._ddFilm = ft.Dropdown(label="Film", width=450)
        self._btnPercorso = ft.ElevatedButton(text="Cerca percorso",
                                              on_click=self._controller.handlePercorso, width=180)
        row2 = ft.Row([self._ddFilm, self._btnPercorso],
                      alignment=ft.MainAxisAlignment.CENTER)

        self._page.controls.append(row1)
        self._page.controls.append(row2)

        # ---------- area risultati ----------
        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)

        # riempio il menu dei generi all'avvio (punto 1a)
        self._controller.fillDDGeneri()

        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def update_page(self):
        self._page.update()

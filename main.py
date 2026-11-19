import os
import json

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup

CONFIG_FILE = "config.json"


class BuscadorLayout(BoxLayout):

    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            spacing=5,
            padding=10,
            **kwargs
        )

        self.ruta_bd = self.cargar_configuracion()

        self.add_widget(
            Label(
                text="Buscador De Socios por Convenio",
                size_hint=(1, None),
                height=40
            )
        )

        self.txt_ruta = TextInput(
            text=self.ruta_bd,
            multiline=False,
            hint_text="Ruta carpeta TXT",
            size_hint=(1, None),
            height=40
        )
        self.add_widget(self.txt_ruta)

        btn_guardar = Button(
            text="GUARDAR RUTA",
            size_hint=(1, None),
            height=40
        )
        btn_guardar.bind(on_press=self.guardar_ruta)
        self.add_widget(btn_guardar)

        self.txt_cedula = TextInput(
            hint_text="Cédula",
            multiline=False,
            size_hint=(1, None),
            height=40
        )
        self.add_widget(self.txt_cedula)

        self.txt_nombres = TextInput(
            hint_text="Nombres",
            multiline=False,
            size_hint=(1, None),
            height=40
        )
        self.add_widget(self.txt_nombres)

        self.txt_apellidos = TextInput(
            hint_text="Apellidos",
            multiline=False,
            size_hint=(1, None),
            height=40
        )
        self.add_widget(self.txt_apellidos)

        self.txt_funcionario = TextInput(
            hint_text="Funcionario",
            multiline=False,
            size_hint=(1, None),
            height=40
        )
        self.add_widget(self.txt_funcionario)

        btn_buscar = Button(
            text="BUSCAR",
            size_hint=(1, None),
            height=60
        )
        btn_buscar.bind(on_press=self.buscar)
        self.add_widget(btn_buscar)

        self.lbl_total = Label(
            text="Resultados encontrados: 0",
            size_hint=(1, None),
            height=30
        )
        self.add_widget(self.lbl_total)

        # Encabezados tipo Excel
        cabecera = GridLayout(
            cols=5,
            size_hint=(None, None),
            width=1300,
            height=30,
            spacing=2
        )

        cabecera.add_widget(
            Label(
                text="[b]CÉDULA[/b]",
                markup=True,
                size_hint_x=None,
                width=120
            )
        )

        cabecera.add_widget(
            Label(
                text="[b]NOMBRES[/b]",
                markup=True,
                size_hint_x=None,
                width=300
            )
        )

        cabecera.add_widget(
            Label(
                text="[b]APELLIDOS[/b]",
                markup=True,
                size_hint_x=None,
                width=300
            )
        )

        cabecera.add_widget(
            Label(
                text="[b]FUNCIONARIO[/b]",
                markup=True,
                size_hint_x=None,
                width=120
            )
        )

        cabecera.add_widget(
            Label(
                text="[b]CONVENIO[/b]",
                markup=True,
                size_hint_x=None,
                width=460
            )
        )

        self.add_widget(cabecera)

        self.scroll = ScrollView(
            do_scroll_x=True,
            do_scroll_y=True
        )

        self.resultados = GridLayout(
            cols=1,
            spacing=1,
            size_hint=(None, None),
            width=1300
        )

        self.resultados.bind(
            minimum_height=self.resultados.setter("height")
        )

        self.scroll.add_widget(self.resultados)

        self.add_widget(self.scroll)

    def cargar_configuracion(self):

        if os.path.exists(CONFIG_FILE):
            try:
                with open(
                    CONFIG_FILE,
                    "r",
                    encoding="utf-8"
                ) as f:
                    datos = json.load(f)

                return datos.get("ruta_bd", "")
            except:
                pass

        return ""

    def guardar_ruta(self, instance):

        self.ruta_bd = self.txt_ruta.text.strip()

        try:
            with open(
                CONFIG_FILE,
                "w",
                encoding="utf-8"
            ) as f:
                json.dump(
                    {"ruta_bd": self.ruta_bd},
                    f,
                    ensure_ascii=False,
                    indent=4
                )

            self.mensaje(
                "Ruta guardada correctamente"
            )

        except Exception as e:
            self.mensaje(str(e))

    def mensaje(self, texto):

        Popup(
            title="Información",
            content=Label(text=texto),
            size_hint=(0.8, 0.4)
        ).open()

    def limpiar_resultados(self):
        self.resultados.clear_widgets()

    def agregar_resultado(
        self,
        cedula,
        nombres,
        apellidos,
        funcionario,
        convenio
    ):

        fila = GridLayout(
            cols=5,
            size_hint=(None, None),
            width=1300,
            height=30,
            spacing=2
        )

        fila.add_widget(
            Label(
                text=cedula,
                size_hint_x=None,
                width=120
            )
        )

        fila.add_widget(
            Label(
                text=nombres,
                size_hint_x=None,
                width=300
            )
        )

        fila.add_widget(
            Label(
                text=apellidos,
                size_hint_x=None,
                width=300
            )
        )

        fila.add_widget(
            Label(
                text=funcionario,
                size_hint_x=None,
                width=120
            )
        )

        fila.add_widget(
            Label(
                text=convenio,
                size_hint_x=None,
                width=460
            )
        )

        self.resultados.add_widget(fila)

    def buscar(self, instance):

        self.ruta_bd = self.txt_ruta.text.strip()

        if not self.ruta_bd:
            self.mensaje(
                "Debe indicar la carpeta que contiene los TXT"
            )
            return

        if not os.path.exists(self.ruta_bd):
            self.mensaje(
                "La carpeta indicada no existe"
            )
            return

        self.limpiar_resultados()

        cedula_buscar = self.txt_cedula.text.strip().upper()
        nombres_buscar = self.txt_nombres.text.strip().upper()
        apellidos_buscar = self.txt_apellidos.text.strip().upper()
        funcionario_buscar = self.txt_funcionario.text.strip().upper()

        total = 0

        try:

            for archivo in os.listdir(self.ruta_bd):

                if not archivo.lower().endswith(".txt"):
                    continue

                ruta_archivo = os.path.join(
                    self.ruta_bd,
                    archivo
                )

                convenio = os.path.splitext(
                    archivo
                )[0]

                with open(
                    ruta_archivo,
                    "r",
                    encoding="utf-8",
                    errors="ignore"
                ) as f:

                    for linea in f:

                        if len(linea) < 106:
                            continue

                        cedula = linea[0:11].strip()
                        nombres = linea[13:52].strip()
                        apellidos = linea[53:94].strip()
                        funcionario = linea[94:106].strip()

                        coincide = True

                        if cedula_buscar:
                            coincide &= (
                                cedula_buscar in cedula.upper()
                            )

                        if nombres_buscar:
                            coincide &= (
                                nombres_buscar in nombres.upper()
                            )

                        if apellidos_buscar:
                            coincide &= (
                                apellidos_buscar in apellidos.upper()
                            )

                        if funcionario_buscar:
                            coincide &= (
                                funcionario_buscar in funcionario.upper()
                            )

                        if coincide:

                            self.agregar_resultado(
                                cedula,
                                nombres,
                                apellidos,
                                funcionario,
                                convenio
                            )

                            total += 1

            self.lbl_total.text = (
                f"Resultados encontrados: {total}"
            )

        except Exception as e:
            self.mensaje(str(e))


class BuscadorApp(App):

    def build(self):
        return BuscadorLayout()


if __name__ == "__main__":
    BuscadorApp().run()
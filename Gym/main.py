import tkinter as tk
from tkinter import ttk
from datetime import datetime
import database as db
import validaciones as v

                                          
BG = '#0a1020'
SIDEBAR = '#101a2c'
SUBSIDEBAR = '#0d1526'
CARD = '#142238'
CARD_2 = '#182942'
TEXT = '#f4f7fb'
MUTED = '#9aaac0'
ACCENT = '#22c55e'
BLUE = '#3b82f6'
ORANGE = '#f59e0b'
RED = '#ef4444'
PURPLE = '#8b5cf6'
BORDER = '#253751'
INPUT = '#0c1627'

                                                                       
ROLES_MENU = {
    'Inicio': ['Administrador', 'Empleado', 'Entrenador'],
    'Clientes': ['Administrador', 'Empleado', 'Entrenador'],
    'Empleados': ['Administrador'],
    'Entrenadores': ['Administrador', 'Entrenador'],
    'Membresías y pagos': ['Administrador', 'Empleado'],
    'Accesos': ['Administrador', 'Empleado'],
    'Máquinas': ['Administrador', 'Empleado'],
    'Rutinas': ['Administrador', 'Empleado', 'Entrenador'],
    'Clases': ['Administrador', 'Empleado', 'Entrenador'],
    'Reportes': ['Administrador'],
}


class App:

    def __init__(self, root):
        self.root = root
        self.root.title('GYM PRO • Sistema de Gestión')
        self.root.geometry('1280x780')
        self.root.minsize(1150, 700)
        self.root.configure(bg=BG)

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configurar_estilos()

        self.status_var = tk.StringVar(value='Listo. Selecciona un módulo para comenzar.')
        self.page_title = tk.StringVar(value='Panel de control')
        self.page_subtitle = tk.StringVar(value='Administra los 50 requerimientos desde una sola ventana.')
        self.content = None
        self.nav_buttons = {}
        self.usuario_actual = None
        self.tipo_usuario = None

        self.mostrar_login()

                                                       
    def configurar_estilos(self):
        self.style.configure(
            'Treeview',
            background=CARD,
            fieldbackground=CARD,
            foreground=TEXT,
            borderwidth=0,
            rowheight=31,
            font=('Segoe UI', 10)
        )
        self.style.configure(
            'Treeview.Heading',
            background=CARD_2,
            foreground=TEXT,
            relief='flat',
            font=('Segoe UI', 10, 'bold')
        )
        self.style.map('Treeview', background=[('selected', '#1f6f46')], foreground=[('selected', 'white')])
        self.style.configure('Vertical.TScrollbar', background=CARD_2, troughcolor=SIDEBAR, bordercolor=SIDEBAR, arrowcolor=TEXT)
        self.style.configure('TCombobox', fieldbackground=INPUT, background=INPUT, foreground=TEXT, arrowcolor=TEXT)

                                                                       
    def mostrar_login(self):
                                                                          
        for w in self.root.winfo_children():
            w.destroy()

        wrap = tk.Frame(self.root, bg=BG)
        wrap.pack(fill='both', expand=True)

        card = tk.Frame(wrap, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor='center')

        tk.Label(card, text='GYM PRO', bg=CARD, fg=ACCENT, font=('Segoe UI', 28, 'bold')).pack(padx=70, pady=(34, 2))
        tk.Label(card, text='Inicia sesión para continuar (RF25)', bg=CARD, fg=MUTED, font=('Segoe UI', 10)).pack(pady=(0, 22))

        tk.Label(card, text='Usuario', bg=CARD, fg=MUTED, font=('Segoe UI', 9, 'bold')).pack(anchor='w', padx=44)
        user_e = self.entrada(card, 26)
        user_e.pack(padx=44, pady=(3, 14))

        tk.Label(card, text='Contraseña', bg=CARD, fg=MUTED, font=('Segoe UI', 9, 'bold')).pack(anchor='w', padx=44)
        pass_e = self.entrada(card, 26)
        pass_e.config(show='•')
        pass_e.pack(padx=44, pady=(3, 8))

        msg_var = tk.StringVar(value='')
        tk.Label(card, textvariable=msg_var, bg=CARD, fg=RED, font=('Segoe UI', 9), wraplength=260, justify='left').pack(padx=44, pady=(0, 6))

        def intentar():
            usuario = user_e.get().strip()
            contrasena = pass_e.get().strip()
            if not usuario or not contrasena:
                msg_var.set('Escribe usuario y contraseña.')
                return
            tipo = db.validar_usuario(usuario, contrasena)
            if tipo:
                self.usuario_actual = usuario
                self.tipo_usuario = tipo
                self.construir()
                db.actualizar_estados_membresia()
                self.mostrar_dashboard()
            else:
                msg_var.set('Usuario o contraseña incorrectos.')

        self.boton(card, 'INGRESAR', intentar, ACCENT).pack(padx=44, pady=(6, 10), fill='x')
        tk.Label(
            card,
            text='Usuarios de prueba:\nadmin / admin123 (Administrador)\nempleado / empleado123 (Empleado)\nentrenador / entrenador123 (Entrenador)',
            bg=CARD, fg=MUTED, font=('Segoe UI', 8), justify='left'
        ).pack(pady=(2, 26), padx=44, anchor='w')

        user_e.focus_set()
        pass_e.bind('<Return>', lambda ev: intentar())
        user_e.bind('<Return>', lambda ev: pass_e.focus_set())

    def cerrar_sesion(self):
        self.usuario_actual = None
        self.tipo_usuario = None
        self.mostrar_login()

                                                                    
    def construir(self):
                                                                                              
                                                                       
        for w in self.root.winfo_children():
            w.destroy()

                
        header = tk.Frame(self.root, bg=BG)
        header.pack(fill='x', padx=26, pady=(20, 8))

        brand = tk.Frame(header, bg=BG)
        brand.pack(side='left')
        tk.Label(brand, text='GYM', bg=BG, fg=ACCENT, font=('Segoe UI', 30, 'bold')).pack(side='left')
        tk.Label(brand, text=' PRO', bg=BG, fg=TEXT, font=('Segoe UI', 18, 'bold')).pack(side='left', padx=(6, 0), pady=(7, 0))

        right_head = tk.Frame(header, bg=BG)
        right_head.pack(side='right')
        tk.Label(right_head, text=f'Sesión: {self.usuario_actual} ({self.tipo_usuario})', bg=BG, fg=MUTED, font=('Segoe UI', 10)).pack(anchor='e')
        tk.Label(right_head, textvariable=self.status_var, bg=BG, fg=TEXT, font=('Segoe UI', 9), wraplength=520, justify='right').pack(anchor='e', pady=(4, 0))

                
        body = tk.Frame(self.root, bg=BG)
        body.pack(fill='both', expand=True, padx=26, pady=(8, 18))

        self.sidebar = tk.Frame(body, bg=SIDEBAR, width=220)
        self.sidebar.pack(side='left', fill='y', padx=(0, 16))
        self.sidebar.pack_propagate(False)

        self.main_area = tk.Frame(body, bg=BG)
        self.main_area.pack(side='left', fill='both', expand=True)

        self.page_header = tk.Frame(self.main_area, bg=BG)
        self.page_header.pack(fill='x', pady=(0, 12))
        tk.Label(self.page_header, textvariable=self.page_title, bg=BG, fg=TEXT, font=('Segoe UI', 24, 'bold')).pack(anchor='w')
        tk.Label(self.page_header, textvariable=self.page_subtitle, bg=BG, fg=MUTED, font=('Segoe UI', 10)).pack(anchor='w', pady=(3, 0))

                                                 
        content_container = tk.Frame(self.main_area, bg=BG)
        content_container.pack(fill='both', expand=True)

        self.content_canvas = tk.Canvas(content_container, bg=BG, highlightthickness=0, bd=0)
        self.content_scroll = ttk.Scrollbar(content_container, orient='vertical', command=self.content_canvas.yview)
        self.content_canvas.configure(yscrollcommand=self.content_scroll.set)
        self.content_canvas.pack(side='left', fill='both', expand=True)
        self.content_scroll.pack(side='right', fill='y')

        self.content = tk.Frame(self.content_canvas, bg=BG)
        self.content_window = self.content_canvas.create_window((0, 0), window=self.content, anchor='nw')

        def _actualizar_scrollregion(event=None):
            self.content_canvas.configure(scrollregion=self.content_canvas.bbox('all'))

        def _ajustar_ancho(event):
            self.content_canvas.itemconfig(self.content_window, width=event.width)

        self.content.bind('<Configure>', _actualizar_scrollregion)
        self.content_canvas.bind('<Configure>', _ajustar_ancho)

                                                                                       
        def _rueda_mouse(event):
            if event.num == 4:
                self.content_canvas.yview_scroll(-1, 'units')
            elif event.num == 5:
                self.content_canvas.yview_scroll(1, 'units')
            else:
                self.content_canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')

        def _activar_scroll(event):
            self.content_canvas.bind_all('<MouseWheel>', _rueda_mouse)
            self.content_canvas.bind_all('<Button-4>', _rueda_mouse)
            self.content_canvas.bind_all('<Button-5>', _rueda_mouse)

        def _desactivar_scroll(event):
            self.content_canvas.unbind_all('<MouseWheel>')
            self.content_canvas.unbind_all('<Button-4>')
            self.content_canvas.unbind_all('<Button-5>')

        self.content_canvas.bind('<Enter>', _activar_scroll)
        self.content_canvas.bind('<Leave>', _desactivar_scroll)

        self.construir_menu()

    def construir_menu(self):
        tk.Label(
            self.sidebar,
            text='NAVEGACIÓN',
            bg=SIDEBAR,
            fg=MUTED,
            font=('Segoe UI', 9, 'bold')
        ).pack(anchor='w', padx=16, pady=(18, 10))

        todos_los_menus = [
            ('Inicio', self.mostrar_dashboard),
            ('Clientes', self.mostrar_clientes),
            ('Empleados', self.mostrar_empleados),
            ('Entrenadores', self.mostrar_entrenadores),
            ('Membresías y pagos', self.mostrar_membresias),
            ('Accesos', self.mostrar_accesos),
            ('Máquinas', self.mostrar_maquinas),
            ('Rutinas', self.mostrar_rutinas),
            ('Clases', self.mostrar_clases),
            ('Reportes', self.mostrar_reportes),
        ]
        menus = [(t, c) for t, c in todos_los_menus if self.tipo_usuario in ROLES_MENU.get(t, [])]

        for text, command in menus:
            btn = tk.Button(
                self.sidebar,
                text=text,
                command=command,
                bg=SIDEBAR,
                fg=TEXT,
                activebackground=CARD_2,
                activeforeground=TEXT,
                relief='flat',
                bd=0,
                anchor='w',
                padx=16,
                pady=11,
                font=('Segoe UI', 9, 'bold'),
                cursor='hand2'
            )
            btn.pack(fill='x', padx=10, pady=2)
            self.nav_buttons[text] = btn

        sep = tk.Frame(self.sidebar, bg=BORDER, height=1)
        sep.pack(fill='x', padx=14, pady=15)
        tk.Label(self.sidebar, text='Requerimientos', bg=SIDEBAR, fg=MUTED, font=('Segoe UI', 9)).pack(anchor='w', padx=16)
        tk.Label(self.sidebar, text='RF01 → RF50', bg=SIDEBAR, fg=ACCENT, font=('Segoe UI', 18, 'bold')).pack(anchor='w', padx=16, pady=(2, 0))
        tk.Label(self.sidebar, text='Todo funciona dentro\nde esta misma ventana.', bg=SIDEBAR, fg=MUTED, font=('Segoe UI', 9), justify='left').pack(anchor='w', padx=16, pady=(5, 0))

        sep2 = tk.Frame(self.sidebar, bg=BORDER, height=1)
        sep2.pack(fill='x', padx=14, pady=15, side='bottom')
        tk.Button(
            self.sidebar, text='CERRAR SESIÓN', command=self.cerrar_sesion,
            bg=RED, fg='white', activebackground=RED, activeforeground='white',
            relief='flat', bd=0, font=('Segoe UI', 9, 'bold'), pady=9, cursor='hand2'
        ).pack(fill='x', padx=10, pady=(0, 4), side='bottom')
        tk.Label(self.sidebar, text=f'Rol actual: {self.tipo_usuario}', bg=SIDEBAR, fg=MUTED, font=('Segoe UI', 8), justify='left', wraplength=190).pack(anchor='w', padx=16, pady=(0, 6), side='bottom')

                                                                
    def limpiar_contenido(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def cambiar_pagina(self, titulo, subtitulo):
        self.limpiar_contenido()
        self.page_title.set(titulo)
        self.page_subtitle.set(subtitulo)
                                                                          
        self.content_canvas.yview_moveto(0)

    def tarjeta(self, parent):
        frame = tk.Frame(parent, bg=CARD, highlightbackground=BORDER, highlightthickness=1)
        return frame

    def boton(self, parent, texto, comando, color=BLUE, ancho=None):
        opciones = {
            'text': texto,
            'command': comando,
            'bg': color,
            'fg': 'white',
            'activebackground': color,
            'activeforeground': 'white',
            'relief': 'flat',
            'bd': 0,
            'font': ('Segoe UI', 9, 'bold'),
            'padx': 14,
            'pady': 9,
            'cursor': 'hand2'
        }
        if ancho:
            opciones['width'] = ancho
        return tk.Button(parent, **opciones)

    def entrada(self, parent, ancho=32):
        return tk.Entry(
            parent,
            width=ancho,
            bg=INPUT,
            fg=TEXT,
            insertbackground=TEXT,
            relief='flat',
            highlightbackground=BORDER,
            highlightcolor=BLUE,
            highlightthickness=1,
            font=('Segoe UI', 10)
        )

    def campo(self, parent, fila, etiqueta, clave, entries, ancho=32):
        tk.Label(parent, text=etiqueta, bg=CARD, fg=MUTED, font=('Segoe UI', 9, 'bold')).grid(row=fila, column=0, sticky='w', padx=18, pady=7)
        entry = self.entrada(parent, ancho)
        entry.grid(row=fila, column=1, sticky='ew', padx=(6, 18), pady=7)
        entries[clave] = entry
        return entry

    def combo(self, parent, fila, etiqueta, clave, valores, combos, ancho=30):
        tk.Label(parent, text=etiqueta, bg=CARD, fg=MUTED, font=('Segoe UI', 9, 'bold')).grid(row=fila, column=0, sticky='w', padx=18, pady=7)
        combo = ttk.Combobox(parent, values=valores, state='readonly', width=ancho, font=('Segoe UI', 10))
        combo.grid(row=fila, column=1, sticky='ew', padx=(6, 18), pady=7)
        combos[clave] = combo
        if valores:
            combo.set(valores[0])
        return combo

    def tabla(self, parent, columnas, filas, anchos=None):
        box = tk.Frame(parent, bg=CARD)
        box.pack(fill='both', expand=True, padx=14, pady=14)
        tree = ttk.Treeview(box, columns=columnas, show='headings')
        for i, col in enumerate(columnas):
            tree.heading(col, text=col)
            width = anchos[i] if anchos and i < len(anchos) else max(100, len(col) * 10)
            tree.column(col, width=width, minwidth=70, anchor='w')
        for fila in filas:
            tree.insert('', 'end', values=fila)
        scroll = ttk.Scrollbar(box, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side='left', fill='both', expand=True)
        scroll.pack(side='right', fill='y')
        return tree

    def nota(self, parent, texto):
        tk.Label(parent, text=texto, bg=CARD, fg=MUTED, font=('Segoe UI', 9), justify='left', wraplength=780).pack(anchor='w', padx=18, pady=(0, 10))

    def resultado(self, ok, mensaje):
        color = ACCENT if ok else RED
        self.status_var.set(mensaje)
        return color

    @staticmethod
    def limpiar_entries(entries):
        for entry in entries.values():
            try:
                entry.set('')
            except AttributeError:
                entry.delete(0, tk.END)

    def limpiar_busqueda(self, e, edit_frame):
        for entry in e.values():
            try:
                entry.delete(0, tk.END)
            except tk.TclError:
                pass
        edit_frame.pack_forget()

                                                                                          
                                                                                          
    def subnav(self, secciones, por_defecto=0):
        wrapper = tk.Frame(self.content, bg=BG)
        wrapper.pack(fill='both', expand=True)

                                                                                        
                                                                                        
        alto_minimo = 70 + len(secciones) * 70
        sub_sidebar = tk.Frame(wrapper, bg=SUBSIDEBAR, width=185, height=alto_minimo, highlightbackground=BORDER, highlightthickness=1)
        sub_sidebar.pack(side='left', fill='y', padx=(0, 14))
        sub_sidebar.pack_propagate(False)

        sub_content = tk.Frame(wrapper, bg=BG)
        sub_content.pack(side='left', fill='both', expand=True)

        tk.Label(sub_sidebar, text='OPCIONES', bg=SUBSIDEBAR, fg=MUTED, font=('Segoe UI', 9, 'bold')).pack(anchor='w', padx=14, pady=(16, 10))

        botones = {}

        def seleccionar(idx):
            for w in sub_content.winfo_children():
                w.destroy()
            secciones[idx][1](sub_content)
            for i, b in botones.items():
                b.configure(bg=(CARD_2 if i == idx else SUBSIDEBAR), fg=(ACCENT if i == idx else TEXT))
            self.content_canvas.yview_moveto(0)

        for i, (titulo, _fn) in enumerate(secciones):
            btn = tk.Button(
                sub_sidebar, text=titulo, command=lambda i=i: seleccionar(i),
                bg=SUBSIDEBAR, fg=TEXT, activebackground=CARD_2, activeforeground=ACCENT,
                relief='flat', bd=0, anchor='w', padx=12, pady=10,
                font=('Segoe UI', 9, 'bold'), cursor='hand2',
                wraplength=150, justify='left'
            )
            btn.pack(fill='x', padx=8, pady=2)
            botones[i] = btn

        seleccionar(por_defecto)

                                                         
    def mostrar_dashboard(self):
        self.cambiar_pagina('Panel de control', 'Todos los módulos se ejecutan dentro de esta misma ventana, sin abrir páginas nuevas.')

        stats = [
            ('CLIENTES', len(db.todos_clientes()), ACCENT),
            ('EMPLEADOS', len(db.todos_empleados()), BLUE),
            ('ENTRENADORES', len(db.todos_entrenadores()), ORANGE),
            ('MÁQUINAS', len(db.maquinas()), PURPLE),
        ]
        grid = tk.Frame(self.content, bg=BG)
        grid.pack(fill='x')
        for i, (nombre, valor, color) in enumerate(stats):
            grid.columnconfigure(i, weight=1)
            card = self.tarjeta(grid)
            card.grid(row=0, column=i, sticky='nsew', padx=5)
            tk.Label(card, text=nombre, bg=CARD, fg=MUTED, font=('Segoe UI', 9, 'bold')).pack(anchor='w', padx=18, pady=(17, 3))
            tk.Label(card, text=str(valor), bg=CARD, fg=color, font=('Segoe UI', 25, 'bold')).pack(anchor='w', padx=18, pady=(0, 16))

        middle = tk.Frame(self.content, bg=BG)
        middle.pack(fill='both', expand=True, pady=15)

        left = self.tarjeta(middle)
        left.pack(side='left', fill='both', expand=True, padx=(0, 7))
        tk.Label(left, text='50 requerimientos implementados', bg=CARD, fg=TEXT, font=('Segoe UI', 15, 'bold')).pack(anchor='w', padx=20, pady=(20, 8))
        texto = (
            'RF01-RF04  Clientes: registrar, consultar, modificar y eliminar.\n'
            'RF05-RF07  Empleados y entrenadores (con búsqueda/edición/eliminación).\n'
            'RF08-RF13  Membresías, asignación, estado, renovación y pagos.\n'
            'RF14-RF16  Ingreso, salida y control de acceso.\n'
            'RF17-RF19  Máquinas y mantenimiento.\n'
            'RF20-RF21  Rutinas y asignación de entrenador.\n'
            'RF22        Consultar la rutina asignada a un cliente.\n'
            'RF23        Historial de asistencia por cliente.\n'
            'RF24        Reportes básicos del gimnasio.\n'
            'RF25        Inicio de sesión y acceso según tipo de usuario.\n'
            'RF26-RF28  Planes Normal ($50.000/2 clases), Gold ($70.000/4 clases)\n'
            '             y Platino ($100.000/6 clases).\n'
            'RF29        Un cliente solo puede tener una membresía a la vez.\n'
            'RF30-RF33  Clases disponibles por cliente: se descuentan al\n'
            '             participar, se bloquea al agotarlas y se pueden consultar.\n'
            'RF34-RF36  Registrar participación en clase, con fecha e instructor.\n'
            'RF37-RF38  Varios instructores, cada clase asociada a uno de ellos.\n'
            'RF39-RF40  Pago de $10.000 por clase, calculado automáticamente.\n'
            'RF41-RF43  Consultar clases y pago por instructor en el mes, y el\n'
            '             total de clases realizadas en el mes.\n'
            'RF44-RF45  Personas que participaron en clases en el mes, en total\n'
            '             y por cada tipo de membresía.\n'
            'RF46-RF47  Ingresos por tipo de membresía y total vendido en el mes.\n'
            'RF48        Resumen mensual con clases, participantes, ingresos\n'
            '             por membresía y pagos a instructores, todo junto.\n'
            'RF49-RF50  Desactivar un cliente sin borrar su historial, y\n'
            '             consultar si está activo o desactivado.'
        )
        tk.Label(left, text=texto, bg=CARD, fg=MUTED, font=('Segoe UI', 10), justify='left').pack(anchor='w', padx=20, pady=10)
        self.nota(left, 'Las validaciones de datos se realizan antes de guardar. Los errores se muestran en la barra de estado de la misma aplicación.')

        right = self.tarjeta(middle)
        right.pack(side='left', fill='both', expand=True, padx=(7, 0))
        tk.Label(right, text='Acciones rápidas', bg=CARD, fg=TEXT, font=('Segoe UI', 15, 'bold')).pack(anchor='w', padx=20, pady=(20, 12))
        self.boton(right, 'GESTIONAR CLIENTES', self.mostrar_clientes, BLUE).pack(fill='x', padx=20, pady=5)
        self.boton(right, 'MEMBRESÍAS Y PAGOS', self.mostrar_membresias, ACCENT).pack(fill='x', padx=20, pady=5)
        self.boton(right, 'CONTROL DE ACCESO', self.mostrar_accesos, ORANGE).pack(fill='x', padx=20, pady=5)
        self.boton(right, 'CLASES', self.mostrar_clases, PURPLE).pack(fill='x', padx=20, pady=5)
        self.boton(right, 'MÁQUINAS', self.mostrar_maquinas, CARD_2).pack(fill='x', padx=20, pady=5)
        if self.tipo_usuario == 'Administrador':
            self.boton(right, 'VER REPORTES', self.mostrar_reportes, CARD_2).pack(fill='x', padx=20, pady=5)

                                                                  
    def mostrar_clientes(self):
        self.cambiar_pagina('Clientes', 'RF01 registrar • RF02 consultar por ID • RF03 modificar • RF04 eliminar')

        def _registrar(cont):
            top = self.tarjeta(cont)
            top.pack(fill='x')
            tk.Label(top, text='Registrar cliente', bg=CARD, fg=TEXT, font=('Segoe UI', 14, 'bold')).grid(row=0, column=0, columnspan=4, sticky='w', padx=18, pady=(15, 6))
            tk.Label(top, text='Fecha de nacimiento: YYYY-MM-DD. Ejemplo: 2005-08-21. Correo: usuario@gmail.com.', bg=CARD, fg=MUTED, font=('Segoe UI', 9), justify='left').grid(row=1, column=0, columnspan=2, sticky='w', padx=18, pady=(0, 8))
            entries = {}
            self.campo(top, 2, 'Nombre', 'nombre', entries)
            self.campo(top, 3, 'Identificación', 'identificacion', entries)
            self.campo(top, 4, 'Teléfono', 'telefono', entries)
            self.campo(top, 5, 'Correo', 'correo', entries)
            self.campo(top, 6, 'Fecha nacimiento', 'fecha', entries)
            top.columnconfigure(1, weight=1)
            self.boton(top, 'GUARDAR CLIENTE', lambda: self.guardar_cliente(entries), ACCENT).grid(row=7, column=0, columnspan=2, sticky='w', padx=18, pady=(8, 17))
            self.boton(top, 'LIMPIAR', lambda: self.limpiar_entries(entries), CARD_2).grid(row=7, column=1, sticky='e', padx=18, pady=(8, 17))

        def _buscar(cont):
            search = self.tarjeta(cont)
            search.pack(fill='x')
            tk.Label(search, text='Buscar cliente por identificación', bg=CARD, fg=TEXT, font=('Segoe UI', 13, 'bold')).pack(anchor='w', padx=18, pady=(16, 10))

            consult = {}
            row_id = tk.Frame(search, bg=CARD)
            row_id.pack(fill='x', padx=18, pady=4)
            tk.Label(row_id, text='Identificación', bg=CARD, fg=MUTED, width=14, anchor='w', font=('Segoe UI', 9, 'bold')).pack(side='left')
            consult['identificacion'] = self.entrada(row_id, 20)
            consult['identificacion'].pack(side='left')
            self.boton(search, 'BUSCAR', lambda: self.buscar_cliente(consult, edit_frame), BLUE).pack(anchor='w', padx=18, pady=(12, 4))

            edit_frame = tk.Frame(search, bg=CARD)
            tk.Label(edit_frame, text='Datos del cliente encontrado', bg=CARD, fg=MUTED, font=('Segoe UI', 9)).pack(anchor='w', pady=(2, 6))
            for lbl, key in [('Nombre', 'nombre'), ('Teléfono', 'telefono'), ('Correo', 'correo'), ('Fecha nacimiento', 'fecha')]:
                r = tk.Frame(edit_frame, bg=CARD)
                r.pack(fill='x', pady=4)
                tk.Label(r, text=lbl, bg=CARD, fg=MUTED, width=14, anchor='w', font=('Segoe UI', 9, 'bold')).pack(side='left')
                consult[key] = self.entrada(r, 20)
                consult[key].pack(side='left')
            self.boton(edit_frame, 'GUARDAR CAMBIOS', lambda: self.modificar_cliente(consult), ORANGE).pack(fill='x', pady=(10, 5))
            self.boton(edit_frame, 'ELIMINAR CLIENTE', lambda: self.eliminar_cliente(consult), RED).pack(fill='x', pady=5)
            self.boton(edit_frame, 'LIMPIAR BÚSQUEDA', lambda: self.limpiar_busqueda(consult, edit_frame), CARD_2).pack(fill='x', pady=(5, 16))

        def _listado(cont):
            list_card = self.tarjeta(cont)
            list_card.pack(fill='both', expand=True)
            tk.Label(list_card, text='Clientes registrados', bg=CARD, fg=TEXT, font=('Segoe UI', 13, 'bold')).pack(anchor='w', padx=18, pady=(16, 0))
            self.tabla(list_card, ['ID', 'Identificación', 'Nombre', 'Teléfono', 'Correo', 'Nacimiento', 'Estado'], db.todos_clientes(), [50, 110, 150, 110, 185, 105, 90])

        self.subnav([
            ('Registrar cliente', _registrar),
            ('Buscar / gestionar', _buscar),
            ('Listado de clientes', _listado),
        ])

    def validar_cliente(self, e):
        validaciones = [
            v.texto(e['nombre'].get(), 'Nombre'),
            v.numeros(e['identificacion'].get(), 'Identificación'),
            v.numeros(e['telefono'].get(), 'Teléfono'),
            v.correo(e['correo'].get()),
            v.fecha(e['fecha'].get(), 'Fecha de nacimiento')
        ]
        for ok, msg in validaciones:
            if not ok:
                self.resultado(False, msg)
                return False
        return True

    def guardar_cliente(self, e):
        if not self.validar_cliente(e):
            return
        ok, msg = db.insertar_cliente(e['identificacion'].get().strip(), e['nombre'].get().strip(), e['telefono'].get().strip(), e['correo'].get().strip(), e['fecha'].get().strip())
        self.resultado(ok, msg)
        if ok:
            self.mostrar_clientes()

    def buscar_cliente(self, e, edit_frame):
        ident = e['identificacion'].get().strip()
        ok, msg = v.numeros(ident, 'Identificación')
        if not ok:
            self.resultado(False, msg)
            return
        fila = db.buscar_cliente(ident)
        if not fila:
            self.resultado(False, 'Cliente no encontrado.')
            edit_frame.pack_forget()
            return
        for key, value in [('nombre', fila[2]), ('telefono', fila[3]), ('correo', fila[4]), ('fecha', fila[5])]:
            e[key].delete(0, tk.END)
            e[key].insert(0, value)
        edit_frame.pack(fill='x', padx=18, pady=(0, 16))
        self.resultado(True, 'Cliente encontrado correctamente.')

    def modificar_cliente(self, e):
        if not self.validar_cliente(e):
            return
        ok, msg = db.actualizar_cliente(e['identificacion'].get().strip(), e['nombre'].get().strip(), e['telefono'].get().strip(), e['correo'].get().strip(), e['fecha'].get().strip())
        self.resultado(ok, msg)
        if ok:
            self.mostrar_clientes()

    def eliminar_cliente(self, e):
        ident = e['identificacion'].get().strip()
        ok, msg = v.numeros(ident, 'Identificación')
        if not ok:
            self.resultado(False, msg)
            return
        ok, msg = db.eliminar_cliente(ident)
        self.resultado(ok, msg)
        if ok:
            self.mostrar_clientes()

                                                                       
    def mostrar_empleados(self):
        self.cambiar_pagina('Empleados', 'RF05 registrar empleados • RF06 consultar/buscar empleados')

        def _registrar(cont):
            card = self.tarjeta(cont)
            card.pack(fill='x')
            tk.Label(card, text='Registrar empleado', bg=CARD, fg=TEXT, font=('Segoe UI', 14, 'bold')).pack(anchor='w', padx=18, pady=(16, 8))
            entries = {}
            form = tk.Frame(card, bg=CARD)
            form.pack(fill='x', padx=18)
            for i, (lbl, key) in enumerate([('Identificación', 'i'), ('Nombre', 'n'), ('Teléfono', 't'), ('Cargo', 'c')]):
                tk.Label(form, text=lbl, bg=CARD, fg=MUTED, font=('Segoe UI', 9, 'bold')).grid(row=0, column=i, sticky='w', padx=(0, 6))
                entries[key] = self.entrada(form, 18)
                entries[key].grid(row=1, column=i, padx=(0, 12), pady=(5, 10))
            self.boton(card, 'REGISTRAR EMPLEADO', lambda: self.guardar_empleado(entries), ACCENT).pack(anchor='w', padx=18, pady=(3, 16))

        def _buscar(cont):
            search = self.tarjeta(cont)
            search.pack(fill='x')
            tk.Label(search, text='Buscar empleado por identificación', bg=CARD, fg=TEXT, font=('Segoe UI', 13, 'bold')).pack(anchor='w', padx=18, pady=(16, 10))
            consult = {}
            row_id = tk.Frame(search, bg=CARD)
            row_id.pack(fill='x', padx=18, pady=4)
            tk.Label(row_id, text='Identificación', bg=CARD, fg=MUTED, width=14, anchor='w', font=('Segoe UI', 9, 'bold')).pack(side='left')
            consult['i'] = self.entrada(row_id, 20)
            consult['i'].pack(side='left')
            self.boton(search, 'BUSCAR', lambda: self.buscar_empleado(consult, edit_frame), BLUE).pack(anchor='w', padx=18, pady=(12, 4))

            edit_frame = tk.Frame(search, bg=CARD)
            tk.Label(edit_frame, text='Datos del empleado encontrado', bg=CARD, fg=MUTED, font=('Segoe UI', 9)).pack(anchor='w', pady=(2, 6))
            for lbl, key in [('Nombre', 'n'), ('Teléfono', 't'), ('Cargo', 'c')]:
                r = tk.Frame(edit_frame, bg=CARD)
                r.pack(fill='x', pady=4)
                tk.Label(r, text=lbl, bg=CARD, fg=MUTED, width=14, anchor='w', font=('Segoe UI', 9, 'bold')).pack(side='left')
                consult[key] = self.entrada(r, 20)
                consult[key].pack(side='left')
            self.boton(edit_frame, 'GUARDAR CAMBIOS', lambda: self.modificar_empleado(consult), ORANGE).pack(fill='x', pady=(10, 5))
            self.boton(edit_frame, 'ELIMINAR EMPLEADO', lambda: self.eliminar_empleado_ui(consult, edit_frame), RED).pack(fill='x', pady=5)
            self.boton(edit_frame, 'LIMPIAR BÚSQUEDA', lambda: self.limpiar_busqueda(consult, edit_frame), CARD_2).pack(fill='x', pady=(5, 16))

        def _listado(cont):
            list_card = self.tarjeta(cont)
            list_card.pack(fill='both', expand=True)
            tk.Label(list_card, text='Empleados registrados', bg=CARD, fg=TEXT, font=('Segoe UI', 13, 'bold')).pack(anchor='w', padx=18, pady=(14, 0))
            self.tabla(list_card, ['Identificación', 'Nombre', 'Teléfono', 'Cargo'], db.todos_empleados(), [140, 190, 140, 180])

        self.subnav([
            ('Registrar empleado', _registrar),
            ('Buscar / gestionar', _buscar),
            ('Listado de empleados', _listado),
        ])

    def guardar_empleado(self, e):
        checks = [v.numeros(e['i'].get(), 'Identificación'), v.texto(e['n'].get(), 'Nombre'), v.numeros(e['t'].get(), 'Teléfono'), v.texto(e['c'].get(), 'Cargo')]
        for ok, msg in checks:
            if not ok:
                self.resultado(False, msg)
                return
        ok, msg = db.insertar_empleado(e['i'].get().strip(), e['n'].get().strip(), e['t'].get().strip(), e['c'].get().strip())
        self.resultado(ok, msg)
        if ok:
            self.mostrar_empleados()

    def buscar_empleado(self, e, edit_frame):
        ident = e['i'].get().strip()
        ok, msg = v.numeros(ident, 'Identificación')
        if not ok:
            self.resultado(False, msg)
            return
        fila = db.buscar_empleado(ident)
        if not fila:
            self.resultado(False, 'Empleado no encontrado.')
            edit_frame.pack_forget()
            return
        for key, value in [('n', fila[1]), ('t', fila[2]), ('c', fila[3])]:
            e[key].delete(0, tk.END)
            e[key].insert(0, value)
        edit_frame.pack(fill='x', padx=18, pady=(0, 16))
        self.resultado(True, 'Empleado encontrado correctamente.')

    def modificar_empleado(self, e):
        checks = [v.numeros(e['i'].get(), 'Identificación'), v.texto(e['n'].get(), 'Nombre'), v.numeros(e['t'].get(), 'Teléfono'), v.texto(e['c'].get(), 'Cargo')]
        for ok, msg in checks:
            if not ok:
                self.resultado(False, msg)
                return
        ok, msg = db.actualizar_empleado(e['i'].get().strip(), e['n'].get().strip(), e['t'].get().strip(), e['c'].get().strip())
        self.resultado(ok, msg)
        if ok:
            self.mostrar_empleados()

    def eliminar_empleado_ui(self, e, edit_frame):
        ident = e['i'].get().strip()
        ok, msg = v.numeros(ident, 'Identificación')
        if not ok:
            self.resultado(False, msg)
            return
        ok, msg = db.eliminar_empleado(ident)
        self.resultado(ok, msg)
        if ok:
            self.mostrar_empleados()

                                                                 
    def mostrar_entrenadores(self):
        self.cambiar_pagina('Entrenadores', 'RF07 registrar entrenadores y especialidades • RF37 varios instructores • gestionar (buscar/modificar/eliminar)')

        def _registrar(cont):
            card = self.tarjeta(cont)
            card.pack(fill='x')
            tk.Label(card, text='Registrar entrenador / instructor', bg=CARD, fg=TEXT, font=('Segoe UI', 14, 'bold')).pack(anchor='w', padx=18, pady=(16, 8))
            tk.Label(card, text='El sistema admite registrar todos los instructores que necesites (mínimo 4, según RF37).', bg=CARD, fg=MUTED, font=('Segoe UI', 9), wraplength=420, justify='left').pack(anchor='w', padx=18, pady=(0, 8))
            entries = {}
            form = tk.Frame(card, bg=CARD)
            form.pack(fill='x', padx=18)
            for i, (lbl, key) in enumerate([('Identificación', 'i'), ('Nombre', 'n'), ('Especialidad', 's')]):
                tk.Label(form, text=lbl, bg=CARD, fg=MUTED, font=('Segoe UI', 9, 'bold')).grid(row=0, column=i, sticky='w', padx=(0, 6))
                entries[key] = self.entrada(form, 22)
                entries[key].grid(row=1, column=i, padx=(0, 15), pady=(5, 10))
            self.boton(card, 'REGISTRAR ENTRENADOR', lambda: self.guardar_entrenador(entries), ACCENT).pack(anchor='w', padx=18, pady=(3, 16))

        def _buscar(cont):
            search = self.tarjeta(cont)
            search.pack(fill='x')
            tk.Label(search, text='Buscar entrenador por identificación', bg=CARD, fg=TEXT, font=('Segoe UI', 13, 'bold')).pack(anchor='w', padx=18, pady=(16, 10))
            consult = {}
            row_id = tk.Frame(search, bg=CARD)
            row_id.pack(fill='x', padx=18, pady=4)
            tk.Label(row_id, text='Identificación', bg=CARD, fg=MUTED, width=14, anchor='w', font=('Segoe UI', 9, 'bold')).pack(side='left')
            consult['i'] = self.entrada(row_id, 20)
            consult['i'].pack(side='left')
            self.boton(search, 'BUSCAR', lambda: self.buscar_entrenador_ui(consult, edit_frame), BLUE).pack(anchor='w', padx=18, pady=(12, 4))

            edit_frame = tk.Frame(search, bg=CARD)
            tk.Label(edit_frame, text='Datos del entrenador encontrado', bg=CARD, fg=MUTED, font=('Segoe UI', 9)).pack(anchor='w', pady=(2, 6))
            for lbl, key in [('Nombre', 'n'), ('Especialidad', 's')]:
                r = tk.Frame(edit_frame, bg=CARD)
                r.pack(fill='x', pady=4)
                tk.Label(r, text=lbl, bg=CARD, fg=MUTED, width=14, anchor='w', font=('Segoe UI', 9, 'bold')).pack(side='left')
                consult[key] = self.entrada(r, 20)
                consult[key].pack(side='left')
            self.boton(edit_frame, 'GUARDAR CAMBIOS', lambda: self.modificar_entrenador(consult), ORANGE).pack(fill='x', pady=(10, 5))
            self.boton(edit_frame, 'ELIMINAR ENTRENADOR', lambda: self.eliminar_entrenador_ui(consult, edit_frame), RED).pack(fill='x', pady=5)
            self.boton(edit_frame, 'LIMPIAR BÚSQUEDA', lambda: self.limpiar_busqueda(consult, edit_frame), CARD_2).pack(fill='x', pady=(5, 16))

        def _listado(cont):
            list_card = self.tarjeta(cont)
            list_card.pack(fill='both', expand=True)
            tk.Label(list_card, text='Entrenadores / instructores registrados', bg=CARD, fg=TEXT, font=('Segoe UI', 13, 'bold')).pack(anchor='w', padx=18, pady=(14, 0))
            self.tabla(list_card, ['ID', 'Identificación', 'Nombre', 'Especialidad'], db.todos_entrenadores(), [55, 140, 180, 220])

        self.subnav([
            ('Registrar entrenador', _registrar),
            ('Buscar / gestionar', _buscar),
            ('Listado de entrenadores', _listado),
        ])

    def guardar_entrenador(self, e):
        checks = [v.numeros(e['i'].get(), 'Identificación'), v.texto(e['n'].get(), 'Nombre'), v.texto(e['s'].get(), 'Especialidad')]
        for ok, msg in checks:
            if not ok:
                self.resultado(False, msg)
                return
        ok, msg = db.insertar_entrenador(e['i'].get().strip(), e['n'].get().strip(), e['s'].get().strip())
        self.resultado(ok, msg)
        if ok:
            self.mostrar_entrenadores()

    def buscar_entrenador_ui(self, e, edit_frame):
        ident = e['i'].get().strip()
        ok, msg = v.numeros(ident, 'Identificación')
        if not ok:
            self.resultado(False, msg)
            return
        fila = db.buscar_entrenador(ident)
        if not fila:
            self.resultado(False, 'Entrenador no encontrado.')
            edit_frame.pack_forget()
            return
        for key, value in [('n', fila[2]), ('s', fila[3])]:
            e[key].delete(0, tk.END)
            e[key].insert(0, value)
        edit_frame.pack(fill='x', padx=18, pady=(0, 16))
        self.resultado(True, 'Entrenador encontrado correctamente.')

    def modificar_entrenador(self, e):
        checks = [v.numeros(e['i'].get(), 'Identificación'), v.texto(e['n'].get(), 'Nombre'), v.texto(e['s'].get(), 'Especialidad')]
        for ok, msg in checks:
            if not ok:
                self.resultado(False, msg)
                return
        ok, msg = db.actualizar_entrenador(e['i'].get().strip(), e['n'].get().strip(), e['s'].get().strip())
        self.resultado(ok, msg)
        if ok:
            self.mostrar_entrenadores()

    def eliminar_entrenador_ui(self, e, edit_frame):
        ident = e['i'].get().strip()
        ok, msg = v.numeros(ident, 'Identificación')
        if not ok:
            self.resultado(False, msg)
            return
        ok, msg = db.eliminar_entrenador(ident)
        self.resultado(ok, msg)
        if ok:
            self.mostrar_entrenadores()

                                                                    
    def mostrar_membresias(self):
        db.actualizar_estados_membresia()
        self.cambiar_pagina('Membresías y pagos', 'RF08-13 membresías y pagos • RF26-29 planes Normal/Gold/Platino • RF30 clases disponibles')

        def _crear(cont):
            create = self.tarjeta(cont)
            create.pack(fill='x')
            tk.Label(create, text='Crear membresía', bg=CARD, fg=TEXT, font=('Segoe UI', 14, 'bold')).grid(row=0, column=0, columnspan=2, sticky='w', padx=18, pady=(16, 8))
            e = {}
            self.campo(create, 1, 'Nombre', 'n', e)
            tk.Label(create, text='Plan', bg=CARD, fg=MUTED, font=('Segoe UI', 9, 'bold')).grid(row=2, column=0, sticky='w', padx=18, pady=7)
            plan_combo = ttk.Combobox(create, values=list(db.PLANES_MEMBRESIA.keys()), state='readonly', width=29, font=('Segoe UI', 10))
            plan_combo.grid(row=2, column=1, sticky='ew', padx=(6, 18), pady=7)
            plan_combo.set('Normal')
            e['t'] = plan_combo

            info_var = tk.StringVar()
            tk.Label(create, textvariable=info_var, bg=CARD, fg=ACCENT, font=('Segoe UI', 9, 'bold')).grid(row=3, column=0, columnspan=2, sticky='w', padx=18, pady=(0, 4))

            def _actualizar_info(event=None):
                plan = db.PLANES_MEMBRESIA[plan_combo.get()]
                info_var.set(f"Precio: ${plan['precio']:,.0f}  •  Clases incluidas: {plan['clases']}")

            plan_combo.bind('<<ComboboxSelected>>', _actualizar_info)
            _actualizar_info()

            self.campo(create, 4, 'Inicio YYYY-MM-DD', 'i', e)
            self.campo(create, 5, 'Fin YYYY-MM-DD', 'f', e)
            create.columnconfigure(1, weight=1)
            self.boton(create, 'REGISTRAR MEMBRESÍA', lambda: self.guardar_membresia(e), ACCENT).grid(row=6, column=0, columnspan=2, sticky='w', padx=18, pady=(7, 16))

        def _accion(cont):
            actions = self.tarjeta(cont)
            actions.pack(fill='x')
            tk.Label(actions, text='Asignar / renovar / pagar', bg=CARD, fg=TEXT, font=('Segoe UI', 14, 'bold')).grid(row=0, column=0, columnspan=2, sticky='w', padx=18, pady=(16, 8))
            a = {}
            self.campo(actions, 1, 'Identificación cliente', 'ci', a)
            self.campo(actions, 2, 'ID membresía', 'mi', a)
            self.campo(actions, 3, 'Fecha pago YYYY-MM-DD', 'fp', a)
            self.campo(actions, 4, 'Valor pago', 'vp', a)
            self.campo(actions, 5, 'Concepto', 'co', a)
            actions.columnconfigure(1, weight=1)
            self.boton(actions, 'ASIGNAR / RENOVAR Y PAGAR', lambda: self.asignar_renovar_pago(a), BLUE).grid(row=6, column=0, columnspan=2, sticky='w', padx=18, pady=(7, 16))

        def _consultar(cont):
            consulta = self.tarjeta(cont)
            consulta.pack(fill='x')
            tk.Label(consulta, text='Consultar estado / historial de pagos', bg=CARD, fg=TEXT, font=('Segoe UI', 14, 'bold')).grid(row=0, column=0, columnspan=2, sticky='w', padx=18, pady=(16, 8))
            c = {}
            self.campo(consulta, 1, 'Identificación cliente', 'ci', c)
            consulta.columnconfigure(1, weight=1)
            rowb = tk.Frame(consulta, bg=CARD)
            rowb.grid(row=2, column=0, columnspan=2, padx=18, pady=(7, 16), sticky='w')
            self.boton(rowb, 'CONSULTAR ESTADO', lambda: self.consultar_estado(c), ORANGE).pack(side='left', padx=(0, 6))
            self.boton(rowb, 'VER HISTORIAL DE PAGOS', lambda: self.ver_historial(c), CARD_2).pack(side='left', padx=6)

        def _listado(cont):
            bottom = self.tarjeta(cont)
            bottom.pack(fill='both', expand=True)
            tk.Label(bottom, text='Membresías registradas (usa el ID de aquí para asignar)', bg=CARD, fg=TEXT, font=('Segoe UI', 13, 'bold')).pack(anchor='w', padx=18, pady=(14, 0))
            self.tabla(bottom, ['ID', 'Nombre', 'Plan', 'Precio', 'Clases', 'Inicio', 'Fin', 'Estado'], db.membresias(), [45, 130, 90, 90, 65, 95, 95, 95])

        self.subnav([
            ('Crear membresía', _crear),
            ('Asignar / renovar / pagar', _accion),
            ('Consultar estado', _consultar),
            ('Listado de membresías', _listado),
        ])

    def guardar_membresia(self, e):
        checks = [
            v.texto(e['n'].get(), 'Nombre'),
            v.fecha(e['i'].get(), 'Inicio'),
            v.fecha(e['f'].get(), 'Fin')
        ]
        for ok, msg in checks:
            if not ok:
                self.resultado(False, msg)
                return
        if e['f'].get().strip() < e['i'].get().strip():
            self.resultado(False, 'La fecha final no puede ser anterior a la fecha inicial.')
            return
        plan_nombre = e['t'].get()
        plan = db.PLANES_MEMBRESIA.get(plan_nombre)
        if not plan:
            self.resultado(False, 'Selecciona un plan válido (Normal, Gold o Platino).')
            return
        ok, msg = db.crear_membresia(e['n'].get().strip(), plan_nombre, plan['precio'], plan['clases'], e['i'].get().strip(), e['f'].get().strip())
        self.resultado(ok, msg)
        if ok:
            self.mostrar_membresias()

    def asignar_renovar_pago(self, e):
        checks = [v.numeros(e['ci'].get(), 'Identificación'), v.numeros(e['mi'].get(), 'ID membresía'), v.fecha(e['fp'].get(), 'Fecha de pago'), v.positivo(e['vp'].get(), 'Valor'), v.texto(e['co'].get(), 'Concepto')]
        for ok, msg in checks:
            if not ok:
                self.resultado(False, msg)
                return
        ok, msg = db.asignar_membresia_y_pago(e['ci'].get().strip(), int(e['mi'].get()), e['fp'].get().strip(), float(e['vp'].get()), e['co'].get().strip())
        self.resultado(ok, msg)
        if ok:
            self.mostrar_membresias()

    def consultar_estado(self, e):
        ok, msg = v.numeros(e['ci'].get(), 'Identificación')
        if not ok:
            self.resultado(False, msg)
            return
        r = db.estado_membresia(e['ci'].get().strip())
        if not r:
            self.resultado(False, 'Cliente no encontrado o sin membresía asignada.')
            return
        tipo, inicio, fin, estado, clases, disponibles = r
        self.resultado(True, f'Plan: {tipo} | Clases incluidas: {clases} | Clases disponibles: {disponibles} | Inicio: {inicio} | Fin: {fin} | Estado: {estado}')

    def ver_historial(self, e):
        ok, msg = v.numeros(e['ci'].get(), 'Identificación')
        if not ok:
            self.resultado(False, msg)
            return
        datos = db.pagos_cliente(e['ci'].get().strip())
        if not datos:
            self.resultado(True, 'El cliente no tiene pagos registrados.')
            return
        resumen = ' | '.join([f'{d[0]} - ${d[1]:,.0f} - {d[2]}' for d in datos[:5]])
        self.resultado(True, f'Historial: {resumen}')

                                                                 
    def mostrar_accesos(self):
        self.cambiar_pagina('Control de acceso', 'RF14 registrar ingreso • RF15 registrar salida • RF16 bloquear acceso • RF23 asistencia')

        def _registro(cont):
            top = self.tarjeta(cont)
            top.pack(fill='x')
            tk.Label(top, text='Registro de acceso', bg=CARD, fg=TEXT, font=('Segoe UI', 14, 'bold')).pack(anchor='w', padx=18, pady=(16, 5))
            tk.Label(top, text='La fecha y hora se toman automáticamente. El ingreso se bloquea si el cliente está desactivado, si no tiene membresía asignada, o si esta ya venció o aún no inicia.', bg=CARD, fg=MUTED, font=('Segoe UI', 9), wraplength=620, justify='left').pack(anchor='w', padx=18, pady=(0, 13))
            row = tk.Frame(top, bg=CARD)
            row.pack(fill='x', padx=18, pady=(0, 18))
            tk.Label(row, text='Identificación cliente', bg=CARD, fg=MUTED, font=('Segoe UI', 9, 'bold')).pack(side='left')
            entry = self.entrada(row, 22)
            entry.pack(side='left', padx=10)
            self.boton(row, 'REGISTRAR INGRESO', lambda: self.acceso(entry, True), ACCENT).pack(side='left', padx=4)
            self.boton(row, 'REGISTRAR SALIDA', lambda: self.acceso(entry, False), ORANGE).pack(side='left', padx=4)

        def _asistencia(cont):
            card = self.tarjeta(cont)
            card.pack(fill='x')
            tk.Label(card, text='Consultar asistencia (RF23)', bg=CARD, fg=TEXT, font=('Segoe UI', 14, 'bold')).pack(anchor='w', padx=18, pady=(16, 8))
            row = tk.Frame(card, bg=CARD)
            row.pack(fill='x', padx=18, pady=(0, 16))
            tk.Label(row, text='Identificación cliente', bg=CARD, fg=MUTED, font=('Segoe UI', 9, 'bold')).pack(side='left')
            entry = self.entrada(row, 22)
            entry.pack(side='left', padx=10)
            self.boton(row, 'VER ASISTENCIA', lambda: self.ver_asistencia(entry), PURPLE).pack(side='left', padx=4)

        def _estado_cliente(cont):
            card = self.tarjeta(cont)
            card.pack(fill='x')
            tk.Label(card, text='Activar / desactivar cliente (RF49)', bg=CARD, fg=TEXT, font=('Segoe UI', 14, 'bold')).pack(anchor='w', padx=18, pady=(16, 8))
            tk.Label(card, text='Desactivar un cliente no borra su información histórica; solo impide que siga usando el sistema e inscribiéndose en nuevas clases.', bg=CARD, fg=MUTED, font=('Segoe UI', 9), wraplength=620, justify='left').pack(anchor='w', padx=18, pady=(0, 10))
            row = tk.Frame(card, bg=CARD)
            row.pack(fill='x', padx=18, pady=(0, 16))
            tk.Label(row, text='Identificación cliente', bg=CARD, fg=MUTED, font=('Segoe UI', 9, 'bold')).pack(side='left')
            entry = self.entrada(row, 22)
            entry.pack(side='left', padx=10)
            self.boton(row, 'DESACTIVAR CLIENTE', lambda: self.desactivar_cliente(entry), RED).pack(side='left', padx=4)
            self.boton(row, 'ACTIVAR CLIENTE', lambda: self.activar_cliente(entry), BLUE).pack(side='left', padx=4)

            card2 = self.tarjeta(cont)
            card2.pack(fill='x', pady=(10, 0))
            tk.Label(card2, text='Consultar estado del cliente (RF50)', bg=CARD, fg=TEXT, font=('Segoe UI', 14, 'bold')).pack(anchor='w', padx=18, pady=(16, 8))
            tk.Label(card2, text='Indica si el cliente está Activo o Desactivado. Un cliente desactivado no puede registrar ingreso ni inscribirse en nuevas clases.', bg=CARD, fg=MUTED, font=('Segoe UI', 9), wraplength=620, justify='left').pack(anchor='w', padx=18, pady=(0, 10))
            row2 = tk.Frame(card2, bg=CARD)
            row2.pack(fill='x', padx=18, pady=(0, 16))
            tk.Label(row2, text='Identificación cliente', bg=CARD, fg=MUTED, font=('Segoe UI', 9, 'bold')).pack(side='left')
            entry2 = self.entrada(row2, 22)
            entry2.pack(side='left', padx=10)
            self.boton(row2, 'CONSULTAR ESTADO DEL CLIENTE', lambda: self.consultar_estado_cliente(entry2), ORANGE).pack(side='left', padx=4)

        def _listado(cont):
            table_card = self.tarjeta(cont)
            table_card.pack(fill='both', expand=True)
            tk.Label(table_card, text='Estado de clientes', bg=CARD, fg=TEXT, font=('Segoe UI', 13, 'bold')).pack(anchor='w', padx=18, pady=(14, 0))
            self.tabla(table_card, ['ID', 'Identificación', 'Nombre', 'Teléfono', 'Correo', 'Nacimiento', 'Estado'], db.todos_clientes(), [50, 110, 160, 110, 185, 105, 100])

        self.subnav([
            ('Ingreso / salida', _registro),
            ('Asistencia', _asistencia),
            ('Activar / desactivar', _estado_cliente),
            ('Listado de clientes', _listado),
        ])

    def acceso(self, entry, entrada):
        ident = entry.get().strip()
        ok, msg = v.numeros(ident, 'Identificación')
        if not ok:
            self.resultado(False, msg)
            return
        ahora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ok, msg = db.registrar_ingreso(ident, ahora) if entrada else db.registrar_salida(ident, ahora)
        self.resultado(ok, msg)

    def ver_asistencia(self, entry):
        ident = entry.get().strip()
        ok, msg = v.numeros(ident, 'Identificación')
        if not ok:
            self.resultado(False, msg)
            return
        filas = db.asistencia_cliente(ident)
        if not filas:
            self.resultado(True, 'El cliente no tiene asistencias (ingresos/salidas) registradas.')
            return
        resumen = ' | '.join([f'{tipo}: {fecha}' for tipo, fecha in filas[:6]])
        self.resultado(True, f'Asistencia reciente: {resumen}')

    def desactivar_cliente(self, entry):
        ident = entry.get().strip()
        ok, msg = v.numeros(ident, 'Identificación')
        if not ok:
            self.resultado(False, msg)
            return
        ok, msg = db.desactivar_cliente(ident)
        self.resultado(ok, msg)
        if ok:
            self.mostrar_accesos()

    def activar_cliente(self, entry):
        ident = entry.get().strip()
        ok, msg = v.numeros(ident, 'Identificación')
        if not ok:
            self.resultado(False, msg)
            return
        ok, msg = db.activar_cliente(ident)
        self.resultado(ok, msg)
        if ok:
            self.mostrar_accesos()

    def consultar_estado_cliente(self, entry):
        ident = entry.get().strip()
        ok, msg = v.numeros(ident, 'Identificación')
        if not ok:
            self.resultado(False, msg)
            return
        r = db.estado_cliente(ident)
        if not r:
            self.resultado(False, 'Cliente no encontrado.')
            return
        nombre, estado = r
        self.resultado(True, f'{nombre} está: {estado}.')

                                                                  
    def mostrar_maquinas(self):
        self.cambiar_pagina('Máquinas y mantenimiento', 'RF17 registrar • RF18 consultar • RF19 controlar mantenimiento')

        def _registrar(cont):
            card = self.tarjeta(cont)
            card.pack(fill='x')
            tk.Label(card, text='Registrar máquina', bg=CARD, fg=TEXT, font=('Segoe UI', 14, 'bold')).pack(anchor='w', padx=18, pady=(16, 8))
            entries = {}
            form = tk.Frame(card, bg=CARD)
            form.pack(fill='x', padx=18)
            for i, (lbl, key) in enumerate([('Nombre máquina', 'n'), ('Marca', 'm')]):
                tk.Label(form, text=lbl, bg=CARD, fg=MUTED, font=('Segoe UI', 9, 'bold')).grid(row=0, column=i, sticky='w', padx=(0, 6))
                entries[key] = self.entrada(form, 24)
                entries[key].grid(row=1, column=i, padx=(0, 18), pady=(5, 10))
            tk.Label(form, text='Estado', bg=CARD, fg=MUTED, font=('Segoe UI', 9, 'bold')).grid(row=0, column=2, sticky='w')
            estado = ttk.Combobox(form, values=['Disponible', 'Mantenimiento', 'Fuera de servicio'], state='readonly', width=23, font=('Segoe UI', 10))
            estado.grid(row=1, column=2, padx=(0, 18), pady=(5, 10))
            estado.set('Disponible')
            entries['s'] = estado
            self.boton(card, 'REGISTRAR MÁQUINA', lambda: self.guardar_maquina(entries), ACCENT).pack(anchor='w', padx=18, pady=(2, 16))

        def _mantenimiento(cont):
            card = self.tarjeta(cont)
            card.pack(fill='both', expand=True)
            tk.Label(card, text='Cambiar estado de una máquina', bg=CARD, fg=TEXT, font=('Segoe UI', 14, 'bold')).pack(anchor='w', padx=18, pady=(16, 8))
            tree = self.tabla(card, ['ID', 'Nombre', 'Marca', 'Estado'], db.maquinas(), [70, 220, 180, 180])

            sel_row = tk.Frame(card, bg=CARD)
            sel_row.pack(fill='x', padx=18, pady=(0, 6))
            tk.Label(sel_row, text='ID máquina', bg=CARD, fg=MUTED, font=('Segoe UI', 9, 'bold')).pack(side='left')
            id_entry = self.entrada(sel_row, 8)
            id_entry.pack(side='left', padx=8)
            tk.Label(sel_row, text='(haz clic en una fila de la tabla para autocompletar el ID, o escríbelo)', bg=CARD, fg=MUTED, font=('Segoe UI', 8)).pack(side='left')

            def _on_select(event):
                sel = tree.selection()
                if sel:
                    mid = tree.item(sel[0], 'values')[0]
                    id_entry.delete(0, tk.END)
                    id_entry.insert(0, mid)

            tree.bind('<<TreeviewSelect>>', _on_select)

            buttons = tk.Frame(card, bg=CARD)
            buttons.pack(pady=(0, 16))
            self.boton(buttons, 'DISPONIBLE', lambda: self.cambiar_maquina(id_entry, 'Disponible'), ACCENT).pack(side='left', padx=4)
            self.boton(buttons, 'MANTENIMIENTO', lambda: self.cambiar_maquina(id_entry, 'Mantenimiento'), ORANGE).pack(side='left', padx=4)
            self.boton(buttons, 'FUERA DE SERVICIO', lambda: self.cambiar_maquina(id_entry, 'Fuera de servicio'), RED).pack(side='left', padx=4)

        def _listado(cont):
            card = self.tarjeta(cont)
            card.pack(fill='both', expand=True)
            tk.Label(card, text='Máquinas registradas', bg=CARD, fg=TEXT, font=('Segoe UI', 13, 'bold')).pack(anchor='w', padx=18, pady=(14, 0))
            self.tabla(card, ['ID', 'Nombre', 'Marca', 'Estado'], db.maquinas(), [70, 220, 180, 180])

        self.subnav([
            ('Registrar máquina', _registrar),
            ('Cambiar estado', _mantenimiento),
            ('Listado de máquinas', _listado),
        ])

    def guardar_maquina(self, e):
        for clave, etiqueta in [('n', 'Nombre máquina'), ('m', 'Marca')]:
            ok, msg = v.texto(e[clave].get(), etiqueta)
            if not ok:
                self.resultado(False, msg)
                return
        ok, msg = db.registrar_maquina(e['n'].get().strip(), e['m'].get().strip(), e['s'].get())
        self.resultado(ok, msg)
        if ok:
            self.mostrar_maquinas()

    def cambiar_maquina(self, id_entry, estado):
        mid = id_entry.get().strip()
        ok, msg = v.numeros(mid, 'ID máquina')
        if not ok:
            self.resultado(False, 'Selecciona una máquina de la tabla (clic en la fila) o escribe su ID.')
            return
        ok, msg = db.cambiar_estado_maquina(mid, estado)
        self.resultado(ok, msg)
        if ok:
            self.mostrar_maquinas()

                                                                 
    def mostrar_rutinas(self):
        self.cambiar_pagina('Rutinas y entrenadores', 'RF20 registrar rutinas • RF21 asignar entrenador • RF22 consultar rutina del cliente')

        def _registrar(cont):
            routine = self.tarjeta(cont)
            routine.pack(fill='x')
            tk.Label(routine, text='Registrar rutina', bg=CARD, fg=TEXT, font=('Segoe UI', 14, 'bold')).grid(row=0, column=0, columnspan=2, sticky='w', padx=18, pady=(16, 8))
            e = {}
            self.campo(routine, 1, 'Identificación cliente', 'ci', e)
            self.campo(routine, 2, 'Nombre rutina', 'n', e)
            self.campo(routine, 3, 'Descripción', 'd', e)
            self.campo(routine, 4, 'Fecha YYYY-MM-DD', 'f', e)
            routine.columnconfigure(1, weight=1)
            self.boton(routine, 'REGISTRAR RUTINA', lambda: self.guardar_rutina(e), ACCENT).grid(row=5, column=0, columnspan=2, sticky='w', padx=18, pady=(7, 16))

        def _asignar(cont):
            assign = self.tarjeta(cont)
            assign.pack(fill='x')
            tk.Label(assign, text='Asignar entrenador', bg=CARD, fg=TEXT, font=('Segoe UI', 14, 'bold')).grid(row=0, column=0, columnspan=2, sticky='w', padx=18, pady=(16, 8))
            a = {}
            self.campo(assign, 1, 'Identificación cliente', 'ci', a)
            self.campo(assign, 2, 'ID entrenador', 'ei', a)
            tk.Label(assign, text='Consulta el ID en el módulo Entrenadores.', bg=CARD, fg=MUTED, font=('Segoe UI', 9)).grid(row=3, column=0, columnspan=2, sticky='w', padx=18, pady=6)
            assign.columnconfigure(1, weight=1)
            self.boton(assign, 'ASIGNAR ENTRENADOR', lambda: self.asignar_entrenador(a), BLUE).grid(row=4, column=0, columnspan=2, sticky='w', padx=18, pady=(7, 16))

        def _consultar(cont):
            consulta = self.tarjeta(cont)
            consulta.pack(fill='x')
            tk.Label(consulta, text='Consultar rutina de un cliente (RF22)', bg=CARD, fg=TEXT, font=('Segoe UI', 14, 'bold')).pack(anchor='w', padx=18, pady=(16, 8))
            crow = tk.Frame(consulta, bg=CARD)
            crow.pack(fill='x', padx=18, pady=(0, 16))
            tk.Label(crow, text='Identificación cliente', bg=CARD, fg=MUTED, font=('Segoe UI', 9, 'bold')).pack(side='left')
            cons_entry = self.entrada(crow, 20)
            cons_entry.pack(side='left', padx=10)
            self.boton(crow, 'CONSULTAR RUTINA', lambda: self.consultar_rutina(cons_entry), BLUE).pack(side='left')

        def _listado(cont):
            bottom = self.tarjeta(cont)
            bottom.pack(fill='both', expand=True)
            tk.Label(bottom, text='Rutinas registradas', bg=CARD, fg=TEXT, font=('Segoe UI', 13, 'bold')).pack(anchor='w', padx=18, pady=(14, 0))
            self.tabla(bottom, ['ID', 'Identificación', 'Cliente', 'Rutina', 'Descripción', 'Fecha'], db.rutinas(), [50, 110, 150, 140, 280, 100])

        self.subnav([
            ('Registrar rutina', _registrar),
            ('Asignar entrenador', _asignar),
            ('Consultar rutina', _consultar),
            ('Listado de rutinas', _listado),
        ])

    def guardar_rutina(self, e):
        checks = [v.numeros(e['ci'].get(), 'Identificación'), v.texto(e['n'].get(), 'Nombre rutina'), v.texto(e['d'].get(), 'Descripción'), v.fecha(e['f'].get(), 'Fecha')]
        for ok, msg in checks:
            if not ok:
                self.resultado(False, msg)
                return
        ok, msg = db.registrar_rutina(e['ci'].get().strip(), e['n'].get().strip(), e['d'].get().strip(), e['f'].get().strip())
        self.resultado(ok, msg)
        if ok:
            self.mostrar_rutinas()

    def asignar_entrenador(self, e):
        checks = [v.numeros(e['ci'].get(), 'Identificación cliente'), v.numeros(e['ei'].get(), 'ID entrenador')]
        for ok, msg in checks:
            if not ok:
                self.resultado(False, msg)
                return
        ok, msg = db.asignar_entrenador(e['ci'].get().strip(), int(e['ei'].get()))
        self.resultado(ok, msg)
        if ok:
            self.mostrar_rutinas()

    def consultar_rutina(self, entry):
        ci = entry.get().strip()
        ok, msg = v.numeros(ci, 'Identificación')
        if not ok:
            self.resultado(False, msg)
            return
        filas = db.rutinas_cliente(ci)
        if not filas:
            self.resultado(False, 'El cliente no tiene rutinas registradas.')
            return
        resumen = ' | '.join([f'{f[3]} ({f[5]})' for f in filas[:5]])
        self.resultado(True, f'Rutinas del cliente: {resumen}')

                                                                                    
    def mostrar_clases(self):
        self.cambiar_pagina('Clases', 'RF29-33 clases disponibles • RF34-38 participación con fecha e instructor • RF39-43 pagos a instructores')

        def _registrar(cont):
            registrar = self.tarjeta(cont)
            registrar.pack(fill='x')
            tk.Label(registrar, text='Registrar participación en clase', bg=CARD, fg=TEXT, font=('Segoe UI', 14, 'bold')).grid(row=0, column=0, columnspan=2, sticky='w', padx=18, pady=(16, 8))
            tk.Label(registrar, text='Se descuenta 1 clase disponible del cliente. Si ya no le quedan clases, el sistema bloquea el registro.', bg=CARD, fg=MUTED, font=('Segoe UI', 9), wraplength=520, justify='left').grid(row=1, column=0, columnspan=2, sticky='w', padx=18, pady=(0, 8))
            e = {}
            self.campo(registrar, 2, 'Identificación cliente', 'ci', e)
            self.campo(registrar, 3, 'ID instructor (entrenador)', 'ei', e)
            self.campo(registrar, 4, 'Fecha YYYY-MM-DD', 'f', e)
            tk.Label(registrar, text='Consulta el ID del instructor en el módulo Entrenadores.', bg=CARD, fg=MUTED, font=('Segoe UI', 9)).grid(row=5, column=0, columnspan=2, sticky='w', padx=18, pady=(0, 6))
            registrar.columnconfigure(1, weight=1)
            self.boton(registrar, 'REGISTRAR PARTICIPACIÓN', lambda: self.guardar_clase(e), ACCENT).grid(row=6, column=0, columnspan=2, sticky='w', padx=18, pady=(7, 16))

        def _consultar(cont):
            consulta = self.tarjeta(cont)
            consulta.pack(fill='x')
            tk.Label(consulta, text='Consultar clases disponibles (RF33)', bg=CARD, fg=TEXT, font=('Segoe UI', 14, 'bold')).pack(anchor='w', padx=18, pady=(16, 8))
            crow = tk.Frame(consulta, bg=CARD)
            crow.pack(fill='x', padx=18, pady=(0, 6))
            tk.Label(crow, text='Identificación cliente', bg=CARD, fg=MUTED, width=16, anchor='w', font=('Segoe UI', 9, 'bold')).pack(side='left')
            cons_entry = self.entrada(crow, 18)
            cons_entry.pack(side='left', padx=10)
            self.boton(consulta, 'CONSULTAR CLASES DISPONIBLES', lambda: self.consultar_clases_disponibles(cons_entry), BLUE).pack(anchor='w', padx=18, pady=(0, 14))

            tk.Label(consulta, text='Historial de clases del cliente', bg=CARD, fg=TEXT, font=('Segoe UI', 13, 'bold')).pack(anchor='w', padx=18, pady=(0, 6))
            hrow = tk.Frame(consulta, bg=CARD)
            hrow.pack(fill='x', padx=18, pady=(0, 6))
            tk.Label(hrow, text='Identificación cliente', bg=CARD, fg=MUTED, width=16, anchor='w', font=('Segoe UI', 9, 'bold')).pack(side='left')
            hist_entry = self.entrada(hrow, 18)
            hist_entry.pack(side='left', padx=10)
            self.boton(consulta, 'VER HISTORIAL DE CLASES', lambda: self.consultar_clases_cliente(hist_entry), CARD_2).pack(anchor='w', padx=18, pady=(0, 16))

        def _pagos(cont):
            card = self.tarjeta(cont)
            card.pack(fill='both', expand=True)
            tk.Label(card, text='Pagos a instructores por mes (RF39-RF43)', bg=CARD, fg=TEXT, font=('Segoe UI', 14, 'bold')).pack(anchor='w', padx=18, pady=(16, 8))
            tk.Label(card, text=f'Cada clase realizada paga ${db.PAGO_POR_CLASE:,.0f} al instructor. Escribe el mes a consultar en formato YYYY-MM (ejemplo: {datetime.now().strftime("%Y-%m")} para el mes actual).', bg=CARD, fg=MUTED, font=('Segoe UI', 9), wraplength=620, justify='left').pack(anchor='w', padx=18, pady=(0, 10))
            row = tk.Frame(card, bg=CARD)
            row.pack(fill='x', padx=18, pady=(0, 10))
            tk.Label(row, text='Mes (YYYY-MM)', bg=CARD, fg=MUTED, font=('Segoe UI', 9, 'bold')).pack(side='left')
            mes_entry = self.entrada(row, 12)
            mes_entry.insert(0, datetime.now().strftime('%Y-%m'))
            mes_entry.pack(side='left', padx=10)

            resumen_frame = tk.Frame(card, bg=CARD)
            resumen_frame.pack(fill='both', expand=True, padx=18, pady=(0, 16))

            def _consultar_mes():
                mes = mes_entry.get().strip()
                ok, msg = v.anio_mes(mes)
                if not ok:
                    self.resultado(False, msg)
                    return
                for w in resumen_frame.winfo_children():
                    w.destroy()
                datos = db.resumen_pagos_instructores(mes)
                total_clases = db.total_clases_mes(mes)
                total_pagar = db.total_pagar_instructores_mes(mes)
                self.tabla(resumen_frame, ['ID', 'Instructor', 'Especialidad', 'Clases en el mes', 'Pago a recibir'],
                           [(eid, nombre, esp, clases, f'${pago:,.0f}') for eid, nombre, esp, clases, pago in datos],
                           [50, 170, 170, 130, 130])
                self.resultado(True, f'RF43: total de clases realizadas en {mes}: {total_clases}. Total a pagar a todos los instructores: ${total_pagar:,.0f}.')

            self.boton(row, 'CONSULTAR PAGOS DEL MES', _consultar_mes, ACCENT).pack(side='left', padx=4)
            _consultar_mes()

        def _listado(cont):
            bottom = self.tarjeta(cont)
            bottom.pack(fill='both', expand=True)
            tk.Label(bottom, text='Clases realizadas (todas)', bg=CARD, fg=TEXT, font=('Segoe UI', 13, 'bold')).pack(anchor='w', padx=18, pady=(14, 0))
            self.tabla(bottom, ['ID', 'Identificación', 'Cliente', 'Instructor', 'Fecha'], db.todas_clases_realizadas(), [50, 110, 160, 160, 100])

        self.subnav([
            ('Registrar participación', _registrar),
            ('Consultar disponibles / historial', _consultar),
            ('Pagos a instructores', _pagos),
            ('Listado de clases', _listado),
        ])

    def guardar_clase(self, e):
        checks = [
            v.numeros(e['ci'].get(), 'Identificación cliente'),
            v.numeros(e['ei'].get(), 'ID instructor'),
            v.fecha(e['f'].get(), 'Fecha')
        ]
        for ok, msg in checks:
            if not ok:
                self.resultado(False, msg)
                return
        ok, msg = db.registrar_participacion_clase(e['ci'].get().strip(), int(e['ei'].get()), e['f'].get().strip())
        self.resultado(ok, msg)
        if ok:
            self.mostrar_clases()

    def consultar_clases_disponibles(self, entry):
        ci = entry.get().strip()
        ok, msg = v.numeros(ci, 'Identificación')
        if not ok:
            self.resultado(False, msg)
            return
        disponibles = db.clases_disponibles_cliente(ci)
        if disponibles is None:
            self.resultado(False, 'Cliente no encontrado.')
            return
        if disponibles <= 0:
            self.resultado(True, 'El cliente no tiene clases disponibles. Debe renovar o asignar una membresía.')
        else:
            self.resultado(True, f'El cliente tiene {disponibles} clase(s) disponible(s).')

    def consultar_clases_cliente(self, entry):
        ci = entry.get().strip()
        ok, msg = v.numeros(ci, 'Identificación')
        if not ok:
            self.resultado(False, msg)
            return
        filas = db.clases_realizadas_cliente(ci)
        if not filas:
            self.resultado(True, 'El cliente no tiene clases realizadas registradas.')
            return
        resumen = ' | '.join([f'{fecha} con {instructor}' for _, fecha, instructor in filas[:5]])
        self.resultado(True, f'Clases realizadas: {resumen}')

                                                     
    def mostrar_reportes(self):
        self.cambiar_pagina('Reportes', 'RF24 reportes básicos • RF41-43 pagos a instructores • RF44-48 resumen mensual completo')

        def _resumen(cont):
            r = db.reporte_general()
            grid = tk.Frame(cont, bg=BG)
            grid.pack(fill='x')
            datos = [
                ('CLIENTES TOTALES', str(r['total_clientes']), ACCENT),
                ('CLIENTES ACTIVOS', str(r['clientes_activos']), BLUE),
                ('MEMBRESÍAS ACTIVAS', str(r['membresias_activas']), ACCENT),
                ('MEMBRESÍAS POR VENCER', str(r['membresias_por_vencer']), ORANGE),
                ('MEMBRESÍAS VENCIDAS', str(r['membresias_vencidas']), RED),
                ('TOTAL RECAUDADO', f"${r['total_recaudado']:,.0f}", PURPLE),
                ('ASISTENCIAS REGISTRADAS', str(r['total_asistencias']), BLUE),
                ('CLASES REALIZADAS', str(r['total_clases_realizadas']), ACCENT),
                ('MÁQUINAS EN MANTENIMIENTO', str(r['maquinas_mantenimiento']), ORANGE),
            ]
            for i, (nombre, valor, color) in enumerate(datos):
                col = i % 3
                fila = i // 3
                grid.columnconfigure(col, weight=1)
                card = self.tarjeta(grid)
                card.grid(row=fila, column=col, sticky='nsew', padx=5, pady=5)
                tk.Label(card, text=nombre, bg=CARD, fg=MUTED, font=('Segoe UI', 9, 'bold'), wraplength=170, justify='left').pack(anchor='w', padx=16, pady=(14, 3))
                tk.Label(card, text=valor, bg=CARD, fg=color, font=('Segoe UI', 19, 'bold')).pack(anchor='w', padx=16, pady=(0, 14))

            note = self.tarjeta(cont)
            note.pack(fill='x', pady=(10, 0))
            self.nota(note, f"Reporte generado para {self.usuario_actual} ({self.tipo_usuario}). Se recalcula cada vez que abres este módulo, con los datos actuales de la base de datos. Total de máquinas registradas: {r['total_maquinas']}.")

        def _pagos_instructores(cont):
            card = self.tarjeta(cont)
            card.pack(fill='both', expand=True)
            tk.Label(card, text='Pagos a instructores por mes (RF39-RF43)', bg=CARD, fg=TEXT, font=('Segoe UI', 14, 'bold')).pack(anchor='w', padx=18, pady=(16, 8))
            tk.Label(card, text=f'Cada clase paga ${db.PAGO_POR_CLASE:,.0f} al instructor que la impartió. Escribe el mes en formato YYYY-MM.', bg=CARD, fg=MUTED, font=('Segoe UI', 9), wraplength=620, justify='left').pack(anchor='w', padx=18, pady=(0, 10))
            row = tk.Frame(card, bg=CARD)
            row.pack(fill='x', padx=18, pady=(0, 10))
            tk.Label(row, text='Mes (YYYY-MM)', bg=CARD, fg=MUTED, font=('Segoe UI', 9, 'bold')).pack(side='left')
            mes_entry = self.entrada(row, 12)
            mes_entry.insert(0, datetime.now().strftime('%Y-%m'))
            mes_entry.pack(side='left', padx=10)

            resumen_frame = tk.Frame(card, bg=CARD)
            resumen_frame.pack(fill='both', expand=True, padx=18, pady=(0, 16))

            def _consultar_mes():
                mes = mes_entry.get().strip()
                ok, msg = v.anio_mes(mes)
                if not ok:
                    self.resultado(False, msg)
                    return
                for w in resumen_frame.winfo_children():
                    w.destroy()
                datos = db.resumen_pagos_instructores(mes)
                total_clases = db.total_clases_mes(mes)
                total_pagar = db.total_pagar_instructores_mes(mes)
                self.tabla(resumen_frame, ['ID', 'Instructor', 'Especialidad', 'Clases en el mes', 'Pago a recibir'],
                           [(eid, nombre, esp, clases, f'${pago:,.0f}') for eid, nombre, esp, clases, pago in datos],
                           [50, 170, 170, 130, 130])
                self.resultado(True, f'RF43: total de clases realizadas en {mes}: {total_clases}. Total a pagar a todos los instructores: ${total_pagar:,.0f}.')

            self.boton(row, 'CONSULTAR PAGOS DEL MES', _consultar_mes, ACCENT).pack(side='left', padx=4)
            _consultar_mes()

        def _resumen_mensual(cont):
            card = self.tarjeta(cont)
            card.pack(fill='x')
            tk.Label(card, text='Resumen mensual completo (RF44-RF48)', bg=CARD, fg=TEXT, font=('Segoe UI', 14, 'bold')).pack(anchor='w', padx=18, pady=(16, 8))
            tk.Label(card, text='Incluye las clases realizadas, los participantes (totales y por tipo de membresía), los ingresos por membresía y los pagos a los instructores de un mes. Escribe el mes en formato YYYY-MM.', bg=CARD, fg=MUTED, font=('Segoe UI', 9), wraplength=680, justify='left').pack(anchor='w', padx=18, pady=(0, 10))
            row = tk.Frame(card, bg=CARD)
            row.pack(fill='x', padx=18, pady=(0, 16))
            tk.Label(row, text='Mes (YYYY-MM)', bg=CARD, fg=MUTED, font=('Segoe UI', 9, 'bold')).pack(side='left')
            mes_entry = self.entrada(row, 12)
            mes_entry.insert(0, datetime.now().strftime('%Y-%m'))
            mes_entry.pack(side='left', padx=10)

            resultado_frame = tk.Frame(cont, bg=BG)
            resultado_frame.pack(fill='both', expand=True)

            def _generar():
                mes = mes_entry.get().strip()
                ok, msg = v.anio_mes(mes)
                if not ok:
                    self.resultado(False, msg)
                    return
                for w in resultado_frame.winfo_children():
                    w.destroy()
                r = db.resumen_mensual(mes)

                                                                              
                g1 = tk.Frame(resultado_frame, bg=BG)
                g1.pack(fill='x', pady=(0, 10))
                tarjetas = [
                    ('CLASES REALIZADAS (RF43)', str(r['total_clases']), ACCENT),
                    ('PARTICIPANTES ÚNICOS (RF44)', str(r['participantes_unicos']), BLUE),
                    ('INGRESO TOTAL MEMBRESÍAS (RF47)', f"${r['ingreso_total_membresias']:,.0f}", PURPLE),
                    ('PAGO TOTAL A INSTRUCTORES', f"${r['total_pagar_instructores']:,.0f}", ORANGE),
                ]
                for i, (nombre, valor, color) in enumerate(tarjetas):
                    g1.columnconfigure(i, weight=1)
                    c = self.tarjeta(g1)
                    c.grid(row=0, column=i, sticky='nsew', padx=5)
                    tk.Label(c, text=nombre, bg=CARD, fg=MUTED, font=('Segoe UI', 9, 'bold'), wraplength=150, justify='left').pack(anchor='w', padx=14, pady=(14, 3))
                    tk.Label(c, text=valor, bg=CARD, fg=color, font=('Segoe UI', 16, 'bold')).pack(anchor='w', padx=14, pady=(0, 14))

                                                                                         
                tabla_card = self.tarjeta(resultado_frame)
                tabla_card.pack(fill='x', pady=(0, 10))
                tk.Label(tabla_card, text='Participantes e ingresos por tipo de membresía (RF45, RF46)', bg=CARD, fg=TEXT, font=('Segoe UI', 13, 'bold')).pack(anchor='w', padx=18, pady=(14, 8))
                filas_tipo = [
                    (tipo, r['participantes_por_membresia'].get(tipo, 0), f"${r['ingresos_por_membresia'].get(tipo, 0):,.0f}")
                    for tipo in db.PLANES_MEMBRESIA
                ]
                self.tabla(tabla_card, ['Tipo de membresía', 'Personas que participaron', 'Ingresos del mes'], filas_tipo, [160, 220, 160])

                                                 
                pagos_card = self.tarjeta(resultado_frame)
                pagos_card.pack(fill='both', expand=True)
                tk.Label(pagos_card, text='Pagos a instructores de este mes', bg=CARD, fg=TEXT, font=('Segoe UI', 13, 'bold')).pack(anchor='w', padx=18, pady=(14, 8))
                self.tabla(pagos_card, ['ID', 'Instructor', 'Especialidad', 'Clases en el mes', 'Pago a recibir'],
                           [(eid, nombre, esp, clases, f'${pago:,.0f}') for eid, nombre, esp, clases, pago in r['pagos_instructores']],
                           [50, 170, 170, 130, 130])

                self.resultado(True, f"Resumen de {mes} generado (RF48): {r['total_clases']} clases, {r['participantes_unicos']} participantes únicos, ${r['ingreso_total_membresias']:,.0f} en membresías.")

            self.boton(row, 'GENERAR RESUMEN DEL MES', _generar, ACCENT).pack(side='left', padx=4)
            _generar()

        self.subnav([
            ('Resumen general', _resumen),
            ('Pagos a instructores', _pagos_instructores),
            ('Resumen mensual (RF44-48)', _resumen_mensual),
        ])


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()

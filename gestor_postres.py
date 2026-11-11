import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# --- LÓGICA DEL PROGRAMA (Gestor de Datos) ---
class GestorPostres:
    def __init__(self):
        self.postres = []

    def _buscar_indice(self, nombre):
        for i, p in enumerate(self.postres):
            if p['nombre'].lower() == nombre.lower():
                return i
        return -1

    def obtener_ingredientes(self, nombre):
        idx = self._buscar_indice(nombre)
        return self.postres[idx]['ingredientes'] if idx != -1 else None

    def insertar_ingrediente(self, nombre_postre, nuevo_ingrediente):
        idx = self._buscar_indice(nombre_postre)
        if idx == -1: return False, "El postre no existe."
        if nuevo_ingrediente.lower() in [i.lower() for i in self.postres[idx]['ingredientes']]:
            return False, "El ingrediente ya existe."
        self.postres[idx]['ingredientes'].append(nuevo_ingrediente)
        return True, "Ingrediente agregado exitosamente."

    def eliminar_ingrediente(self, nombre_postre, ingrediente_eliminar):
        idx = self._buscar_indice(nombre_postre)
        if idx == -1: return False, "El postre no existe."
        ingredientes = self.postres[idx]['ingredientes']
        for i, ing in enumerate(ingredientes):
            if ing.lower() == ingrediente_eliminar.lower():
                ingredientes.pop(i)
                return True, "Ingrediente eliminado."
        return False, "El ingrediente no está en este postre."

    def alta_postre(self, nombre, ingredientes):
        if not nombre: return False, "El nombre no puede estar vacío."
        if self._buscar_indice(nombre) != -1: return False, "El postre ya existe."
        self.postres.append({'nombre': nombre, 'ingredientes': ingredientes})
        self.postres = sorted(self.postres, key=lambda x: x['nombre'].lower())
        return True, "Postre dado de alta exitosamente."

    def baja_postre(self, nombre):
        idx = self._buscar_indice(nombre)
        if idx == -1: return False, "El postre no existe."
        self.postres.pop(idx)
        return True, "Postre eliminado."

    def eliminar_repetidos(self):
        postres_unicos = []
        nombres_vistos = set()
        eliminados = 0
        for p in self.postres:
            nombre_lower = p['nombre'].lower()
            if nombre_lower not in nombres_vistos:
                nombres_vistos.add(nombre_lower)
                postres_unicos.append(p)
            else:
                eliminados += 1
        self.postres = postres_unicos
        return eliminados

# --- INTERFAZ GRÁFICA MEJORADA ---
class AppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🍰 Menú de Postres Dulces 🍰")
        self.root.geometry("680x520")
        
        # Paleta de Colores
        self.BG_MAIN = "#FFF0F5"       # Lavanda rubor (Fondo principal)
        self.BG_PANEL = "#FFE4E1"      # Rosa bruma (Paneles)
        self.BTN_BG = "#FFB6C1"        # Rosa claro (Botones)
        self.BTN_FG = "#4A2311"        # Marrón chocolate (Texto)
        self.TXT_BG = "#FFFFFF"        # Blanco (Lista)
        
        self.root.configure(bg=self.BG_MAIN)
        self.gestor = GestorPostres()
        
        # Datos iniciales para que no esté vacío
        self.gestor.alta_postre("Pastel de Chocolate", ["Harina", "Huevos", "Cacao", "Azúcar"])
        self.gestor.alta_postre("Flan Napolitano", ["Leche", "Huevos", "Vainilla", "Caramelo"])
        self.gestor.alta_postre("Carlota de Limón", ["Galletas", "Leche evaporada", "Limón"])
        
        self.crear_interfaz()

    def crear_btn(self, parent, text, command):
        """Helper para crear botones con estilo uniforme"""
        btn = tk.Button(parent, text=text, command=command, bg=self.BTN_BG, fg=self.BTN_FG, 
                        font=("Segoe UI", 10, "bold"), relief="groove", cursor="hand2", pady=5)
        return btn

    def crear_interfaz(self):
        # Título superior
        lbl_titulo = tk.Label(self.root, text="🧁 Gestor de Recetas y Postres 🧁", 
                              font=("Segoe UI", 16, "bold"), bg=self.BG_MAIN, fg=self.BTN_FG)
        lbl_titulo.pack(pady=10)

        # Contenedor Principal
        main_frame = tk.Frame(self.root, bg=self.BG_MAIN)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)

        # --- PANEL IZQUIERDO: LISTA DE POSTRES ---
        frame_izq = tk.LabelFrame(main_frame, text=" 📖 Lista de Postres ", 
                                  font=("Segoe UI", 11, "bold"), bg=self.BG_PANEL, fg=self.BTN_FG, padx=10, pady=10)
        frame_izq.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Scrollbar y Listbox
        scroll = tk.Scrollbar(frame_izq)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox_postres = tk.Listbox(frame_izq, yscrollcommand=scroll.set, bg=self.TXT_BG, 
                                          fg=self.BTN_FG, font=("Segoe UI", 11), selectbackground="#FF69B4", 
                                          selectforeground="white", relief="flat", highlightthickness=1)
        self.listbox_postres.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.config(command=self.listbox_postres.yview)

        # --- PANEL DERECHO: CONTROLES ---
        frame_der = tk.Frame(main_frame, bg=self.BG_MAIN)
        frame_der.pack(side=tk.RIGHT, fill=tk.Y)

        # Grupo 1: Gestión de Postres
        grupo_postres = tk.LabelFrame(frame_der, text=" 🍰 Gestión de Postres ", 
                                      font=("Segoe UI", 10, "bold"), bg=self.BG_PANEL, fg=self.BTN_FG, padx=15, pady=10)
        grupo_postres.pack(fill=tk.X, pady=(0, 10))
        
        self.crear_btn(grupo_postres, "➕ Alta de Postre (Nuevo)", self.alta_postre).pack(fill=tk.X, pady=3)
        self.crear_btn(grupo_postres, "❌ Baja de Postre (Eliminar)", self.baja_postre).pack(fill=tk.X, pady=3)

        # Grupo 2: Gestión de Ingredientes
        grupo_ing = tk.LabelFrame(frame_der, text=" 🍫 Gestión de Ingredientes ", 
                                  font=("Segoe UI", 10, "bold"), bg=self.BG_PANEL, fg=self.BTN_FG, padx=15, pady=10)
        grupo_ing.pack(fill=tk.X, pady=10)
        
        self.crear_btn(grupo_ing, "👀 Ver Ingredientes", self.ver_ingredientes).pack(fill=tk.X, pady=3)
        self.crear_btn(grupo_ing, "➕ Agregar Ingrediente", self.agregar_ing).pack(fill=tk.X, pady=3)
        self.crear_btn(grupo_ing, "🗑️ Eliminar Ingrediente", self.eliminar_ing).pack(fill=tk.X, pady=3)

        # Grupo 3: Sistema y Limpieza
        grupo_sis = tk.LabelFrame(frame_der, text=" ⚙️ Herramientas ", 
                                  font=("Segoe UI", 10, "bold"), bg=self.BG_PANEL, fg=self.BTN_FG, padx=15, pady=10)
        grupo_sis.pack(fill=tk.X, pady=10)
        
        self.crear_btn(grupo_sis, "🧹 Limpiar Repetidos (Ej. 2)", self.eliminar_repetidos).pack(fill=tk.X, pady=3)

        self.actualizar_lista_postres()

    # --- MÉTODOS DE LA INTERFAZ ---
    def actualizar_lista_postres(self):
        self.listbox_postres.delete(0, tk.END)
        for p in self.gestor.postres:
            self.listbox_postres.insert(tk.END, f"🍮 {p['nombre']}")

    def obtener_seleccion(self):
        seleccion = self.listbox_postres.curselection()
        if not seleccion:
            messagebox.showwarning("⚠️ Atención", "Por favor, selecciona un postre de la lista haciendo clic en él.")
            return None
        # Limpiamos el emoji para la búsqueda lógica
        nombre_mostrado = self.listbox_postres.get(seleccion[0])
        return nombre_mostrado.replace("🍮 ", "")

    def ver_ingredientes(self):
        nombre = self.obtener_seleccion()
        if nombre:
            ingredientes = self.gestor.obtener_ingredientes(nombre)
            if ingredientes:
                texto = "\n".join(f"🔸 {ing}" for ing in ingredientes)
                messagebox.showinfo(f"📋 Ingredientes de {nombre}", texto)
            else:
                messagebox.showinfo(f"📋 Ingredientes de {nombre}", "No tiene ingredientes registrados.")

    def agregar_ing(self):
        nombre = self.obtener_seleccion()
        if nombre:
            ing = simpledialog.askstring("Nuevo Ingrediente", f"📝 Escribe el nuevo ingrediente para:\n{nombre}")
            if ing:
                exito, msg = self.gestor.insertar_ingrediente(nombre, ing.strip())
                if exito: messagebox.showinfo("✅ Éxito", msg)
                else: messagebox.showerror("❌ Error", msg)

    def eliminar_ing(self):
        nombre = self.obtener_seleccion()
        if nombre:
            ing = simpledialog.askstring("Eliminar Ingrediente", f"🗑️ ¿Qué ingrediente deseas eliminar de:\n{nombre}?")
            if ing:
                exito, msg = self.gestor.eliminar_ingrediente(nombre, ing.strip())
                if exito: messagebox.showinfo("✅ Éxito", msg)
                else: messagebox.showerror("❌ Error", msg)

    def alta_postre(self):
        nombre = simpledialog.askstring("Alta de Postre", "🍰 Escribe el nombre del nuevo postre:")
        if nombre:
            ingredientes_str = simpledialog.askstring("Ingredientes", "🛒 Escribe los ingredientes separados por coma (ej: Leche, Azúcar):")
            ingredientes = [i.strip() for i in ingredientes_str.split(",")] if ingredientes_str else []
            exito, msg = self.gestor.alta_postre(nombre.strip(), ingredientes)
            if exito:
                self.actualizar_lista_postres()
                messagebox.showinfo("✅ Éxito", msg)
            else:
                messagebox.showerror("❌ Error", msg)

    def baja_postre(self):
        nombre = self.obtener_seleccion()
        if nombre:
            if messagebox.askyesno("⚠️ Confirmar Baja", f"¿Estás seguro de eliminar '{nombre}' de forma permanente?"):
                exito, msg = self.gestor.baja_postre(nombre)
                if exito:
                    self.actualizar_lista_postres()
                    messagebox.showinfo("✅ Éxito", msg)

    def eliminar_repetidos(self):
        # Insertamos un duplicado intencional para demostrar la funcionalidad
        if messagebox.askyesno("🧪 Prueba de Mantenimiento", "¿Deseas forzar la creación de un postre duplicado para probar esta función?"):
            if self.gestor.postres:
                duplicado = self.gestor.postres[0].copy()
                self.gestor.postres.append(duplicado)
                self.actualizar_lista_postres()
                messagebox.showinfo("ℹ️ Información", f"Se duplicó '{duplicado['nombre']}'. Ahora pulsa 'Limpiar Repetidos' nuevamente para ver cómo desaparece.")
                return

        eliminados = self.gestor.eliminar_repetidos()
        self.actualizar_lista_postres()
        messagebox.showinfo("🧹 Limpieza Completada", f"Se encontraron y eliminaron {eliminados} postres repetidos en el sistema.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AppGUI(root)
    root.mainloop()
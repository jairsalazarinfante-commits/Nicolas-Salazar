import tkinter as tk
from tkinter import messagebox
from robot import Robot


class AplicacionRobot:

    def __init__(self):
        # Crear ventana
        self.root = tk.Tk()
        self.root.title("Simulador Robot Explorador")
        self.root.geometry("550x520")

        # Crear robot
        self.robot = Robot(callback=self.actualizar_gui)

        # ---- TITULO ----
        tk.Label(self.root, text="ROBOT EXPLORADOR", font=("Arial", 16, "bold")).pack(pady=10)

        # ---- AGREGAR TAREA ----
        tk.Label(self.root, text="Tipo de tarea:").pack()

        # Variable para el tipo de tarea
        self.tipo_tarea = tk.StringVar(value="Sensores")

        frame_tipo = tk.Frame(self.root)
        frame_tipo.pack()
        tk.Radiobutton(frame_tipo, text="Tarea Sensores", variable=self.tipo_tarea,
                        value="Sensores").pack(side="left", padx=10)
        tk.Radiobutton(frame_tipo, text="Tarea Movimiento", variable=self.tipo_tarea,
                        value="Movimiento").pack(side="left", padx=10)

        # Tiempo de ejecucion
        tk.Label(self.root, text="Tiempo de ejecucion (segundos):").pack(pady=(10, 0))
        self.entry_tiempo = tk.Entry(self.root, width=20)
        self.entry_tiempo.pack()

        # ---- BOTONES ----
        tk.Button(self.root, text="Agregar Tarea a la Pila", command=self.agregar_tarea,
                  bg="green", fg="white", width=25).pack(pady=10)

        tk.Button(self.root, text="Iniciar Ejecucion", command=self.robot.iniciar_ejecucion,
                  bg="blue", fg="white", width=25).pack(pady=5)

        tk.Button(self.root, text="Detener Ejecucion", command=self.robot.detener_ejecucion,
                  bg="red", fg="white", width=25).pack(pady=5)

        # ---- ESTADO ----
        tk.Label(self.root, text="ESTADO DEL PROCESADOR", font=("Arial", 12, "bold")).pack(pady=10)

        self.label_estado = tk.Label(self.root, text="Procesador desocupado", font=("Arial", 11))
        self.label_estado.pack()

        self.label_progreso = tk.Label(self.root, text="", font=("Arial", 10))
        self.label_progreso.pack()

        # ---- PILA DE TAREAS ----
        tk.Label(self.root, text="PILA DE TAREAS (cima arriba)", font=("Arial", 12, "bold")).pack(pady=10)

        self.listbox_pila = tk.Listbox(self.root, width=50, height=5)
        self.listbox_pila.pack()

        # ---- HISTORIAL ----
        tk.Label(self.root, text="HISTORIAL", font=("Arial", 12, "bold")).pack(pady=10)

        self.listbox_historial = tk.Listbox(self.root, width=50, height=4)
        self.listbox_historial.pack()

    def agregar_tarea(self):
        tipo = self.tipo_tarea.get()
        tiempo_str = self.entry_tiempo.get().strip()

        if not tiempo_str:
            messagebox.showwarning("Error", "Ingresa el tiempo de ejecucion")
            return

        try:
            tiempo = float(tiempo_str)
            if tiempo <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "El tiempo debe ser un numero positivo")
            return

        tarea = self.robot.agregar_tarea(tipo, tiempo)

        self.entry_tiempo.delete(0, tk.END)
        self.refrescar_pila()
        messagebox.showinfo("OK", f"{tarea.tipo} agregada ({tarea.tiempo_ejecucion}s)")

    def actualizar_gui(self, evento, datos):
        """Se llama desde el hilo del robot. Usa root.after para ser seguro."""
        self.root.after(0, self.procesar_evento, evento, datos)

    def procesar_evento(self, evento, datos):
        if evento == "ejecutando_tarea":
            tarea = datos["tarea"]
            self.label_estado.config(text=f"Ejecutando: {tarea.tipo} (Tarea {tarea.id})")
            self.refrescar_pila()

        elif evento == "progreso_tarea":
            tarea = datos["tarea"]
            restante = datos["restante"]
            total = datos["total"]
            self.label_progreso.config(
                text=f"Tiempo: {total - restante:.1f}s / {total:.1f}s")

        elif evento == "tarea_completada":
            self.refrescar_pila()
            self.refrescar_historial()

        elif evento == "ejecucion_finalizada":
            self.label_estado.config(text="Procesador desocupado")
            self.label_progreso.config(text="")
            self.refrescar_pila()

        elif evento == "sin_tareas":
            messagebox.showinfo("Aviso", "No hay tareas en la pila")

    def refrescar_pila(self):
        self.listbox_pila.delete(0, tk.END)

        # Tarea ejecutandose
        if self.robot.tarea_actual:
            t = self.robot.tarea_actual
            self.listbox_pila.insert(tk.END, f">> Tarea {t.id}: {t.tipo} - {t.tiempo_ejecucion}s - EJECUTANDO")

        # Tareas en la pila (cima primero)
        for t in self.robot.obtener_pila():
            self.listbox_pila.insert(tk.END, f"   Tarea {t.id}: {t.tipo} - {t.tiempo_ejecucion}s - En pila")

    def refrescar_historial(self):
        self.listbox_historial.delete(0, tk.END)
        for t in self.robot.historial:
            self.listbox_historial.insert(tk.END, f"Tarea {t.id}: {t.tipo} - {t.tiempo_ejecucion}s - Completada")

    def ejecutar(self):
        self.root.mainloop()


# ---- PUNTO DE ENTRADA ----
if __name__ == "__main__":
    app = AplicacionRobot()
    app.ejecutar()

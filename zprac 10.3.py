import tkinter as tk
from tkinter import ttk, filedialog
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Clases de superficies
class Superficie3D:
    def __init__(self, x_range, y_range):
        self.x_range = x_range
        self.y_range = y_range
        self.x, self.y = np.meshgrid(np.linspace(x_range[0], x_range[1], 100), 
                                     np.linspace(y_range[0], y_range[1], 100))

    def calcular_z(self):
        raise NotImplementedError("Este método debe ser implementado por las subclases")

    def generar_datos(self):
        self.z = self.calcular_z()
        return self.x, self.y, self.z

class Plano(Superficie3D):
    def __init__(self, x_range, y_range, pendiente):
        super().__init__(x_range, y_range)
        self.pendiente = pendiente

    def calcular_z(self):
        return self.pendiente * self.x

class Paraboloide(Superficie3D):
    def __init__(self, x_range, y_range, coef):
        super().__init__(x_range, y_range)
        self.coef = coef

    def calcular_z(self):
        return self.coef * (self.x**2 + self.y**2)

class Sinusoide(Superficie3D):
    def __init__(self, x_range, y_range, frecuencia):
        super().__init__(x_range, y_range)
        self.frecuencia = frecuencia

    def calcular_z(self):
        return np.sin(self.frecuencia * np.sqrt(self.x**2 + self.y**2))

class Hiperboloide(Superficie3D):
    def __init__(self, x_range, y_range, a, b, c):
        super().__init__(x_range, y_range)
        self.a = a
        self.b = b
        self.c = c

    def calcular_z(self):
        return (self.x**2 / self.a**2 - self.y**2 / self.b**2) * self.c

class Esfera(Superficie3D):
    def __init__(self, x_range, y_range, radio=1):
        super().__init__(x_range, y_range)
        self.radio = radio

    def calcular_z(self):
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        u, v = np.meshgrid(u, v)
        self.x = self.radio * np.cos(u) * np.sin(v)
        self.y = self.radio * np.sin(u) * np.sin(v)
        self.z = self.radio * np.cos(v)
        return self.z

class SchwarzSurface(Superficie3D):
    def __init__(self, x_range, y_range, pendiente=1):
        super().__init__(x_range, y_range)
        self.pendiente = pendiente

    def calcular_z(self):
        return np.sin(self.pendiente * self.x) * np.sin(self.pendiente * self.y)

class MobiusStrip(Superficie3D):
    def __init__(self, x_range, y_range, tamaño=1):
        super().__init__(x_range, y_range)
        self.tamaño = tamaño

    def calcular_z(self):
        theta = np.linspace(0, 2 * np.pi, 100)
        w = np.linspace(-self.tamaño, self.tamaño, 100)
        w, theta = np.meshgrid(w, theta)
        self.x = (1 + w / 2 * np.cos(theta / 2)) * np.cos(theta)
        self.y = (1 + w / 2 * np.cos(theta / 2)) * np.sin(theta)
        self.z = w / 2 * np.sin(theta / 2)
        return self.z

class Toro(Superficie3D):
    def __init__(self, x_range, y_range, R=1, r=0.5):
        super().__init__(x_range, y_range)
        self.R = R
        self.r = r

    def calcular_z(self):
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, 2 * np.pi, 100)
        u, v = np.meshgrid(u, v)
        self.x = (self.R + self.r * np.cos(v)) * np.cos(u)
        self.y = (self.R + self.r * np.cos(v)) * np.sin(u)
        self.z = self.r * np.sin(v)
        return self.z

class Elipsoide(Superficie3D):
    def __init__(self, x_range, y_range, a=1, b=1, c=1):
        super().__init__(x_range, y_range)
        self.a = a
        self.b = b
        self.c = c

    def calcular_z(self):
        u = np.linspace(0, 2 * np.pi, 100)
        v = np.linspace(0, np.pi, 100)
        u, v = np.meshgrid(u, v)
        self.x = self.a * np.cos(u) * np.sin(v)
        self.y = self.b * np.sin(u) * np.sin(v)
        self.z = self.c * np.cos(v)
        return self.z

# Visualizador 3D usando Matplotlib
class Visualizador3D:
    def __init__(self, superficie):
        self.superficie = superficie

    def mostrar_con_matplotlib(self, ax):
        x, y, z = self.superficie.generar_datos()
        ax.plot_surface(x, y, z, cmap='viridis')

# Interfaz gráfica con Tkinter
class GeometryVisualizer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Visualización en 3D")
        self.geometry("800x600")
        
        self.create_widgets()
        
    def create_widgets(self):
        # Title
        ttk.Label(self, text="Visualización en 3D", font=("Helvetica", 16)).pack(pady=10)
        
        # Choose Geometry
        self.geometry_choice = tk.StringVar(value="Esfera")
        geometries = ["Plano", "Paraboloide", "Sinusoide", "Hiperboloide", "Esfera", "Superficie de Schwarz", "Banda de Möbius", "Toro", "Elipsoide"]
        
        ttk.Label(self, text="Elija el cuerpo geométrico").pack(pady=5)
        for geometry in geometries:
            ttk.Radiobutton(self, text=geometry, variable=self.geometry_choice, value=geometry).pack(anchor=tk.W)
        
        # Parameter Scale
        self.parametro = tk.DoubleVar(value=1.0)
        self.parametro2 = tk.DoubleVar(value=1.0)
        self.parametro3 = tk.DoubleVar(value=1.0)
        
        self.parametro_label = ttk.Label(self, text="Ingrese el parámetro 1:")
        self.parametro_label.pack(pady=5)
        self.parametro_scale = ttk.Scale(self, from_=0.1, to_=10.0, variable=self.parametro)
        self.parametro_scale.pack(fill=tk.X, padx=20)
        self.parametro_val_label = ttk.Label(self, text="1.0")
        self.parametro_val_label.pack()
        
        self.parametro_scale.bind("<Motion>", self.update_parametro_label)
        
        # Plot Button
        ttk.Button(self, text="Graficar", command=self.plot_geometry).pack(pady=10)
        
        # 3D Surface
        self.figure = Figure(figsize=(5, 5), dpi=100)
        self.ax = self.figure.add_subplot(111, projection='3d')
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(pady=20)
    
    def update_parametro_label(self, event):
        self.parametro_val_label.config(text=f"{self.parametro.get():.2f}")
    
    def plot_geometry(self):
        geometry = self.geometry_choice.get()
        x_range = (-5, 5)
        y_range = (-5, 5)
        
        if geometry == "Plano":
            superficie = Plano(x_range, y_range, self.parametro.get())
        elif geometry == "Paraboloide":
            superficie = Paraboloide(x_range, y_range, self.parametro.get())
        elif geometry == "Sinusoide":
            superficie = Sinusoide(x_range, y_range, self.parametro.get())
        elif geometry == "Hiperboloide":
            superficie = Hiperboloide(x_range, y_range, self.parametro.get(), self.parametro2.get(), self.parametro3.get())
        elif geometry == "Esfera":
            superficie = Esfera(x_range, y_range, self.parametro.get())
        elif geometry == "Superficie de Schwarz":
            superficie = SchwarzSurface(x_range, y_range, self.parametro.get())
        elif geometry == "Banda de Möbius":
            superficie = MobiusStrip(x_range, y_range, self.parametro.get())
        elif geometry == "Toro":
            superficie = Toro(x_range, y_range, self.parametro.get(), self.parametro2.get())
        elif geometry == "Elipsoide":
            superficie = Elipsoide(x_range, y_range, self.parametro.get(), self.parametro2.get(), self.parametro3.get())
        
        visualizador = Visualizador3D(superficie)
        self.ax.clear()
        visualizador.mostrar_con_matplotlib(self.ax)
        self.canvas.draw()

if __name__ == "__main__":
    app = GeometryVisualizer()
    app.mainloop()

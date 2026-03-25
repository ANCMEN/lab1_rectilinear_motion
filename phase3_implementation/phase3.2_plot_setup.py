"""
Фаза 3.1: Реалізація Інтерфейсу
Тільки метод setup_ui()
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class RectilinearMotionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Моделювання прямолінійного руху")
        self.root.geometry("900x600")
        self.setup_plot()
        
        # Змінні для зберігання значень
        self.x0_var = tk.DoubleVar(value=0.0)
        self.y0_var = tk.DoubleVar(value=0.0)
        self.angle_var = tk.DoubleVar(value=45.0)
        self.v0_var = tk.DoubleVar(value=10.0)
        self.a_var = tk.DoubleVar(value=0.0)
        self.color_var = tk.StringVar(value="blue")
        
        # Кольори для вибору
        self.colors = {
            "Синій": "blue",
            "Червоний": "red",
            "Зелений": "green",
            "Чорний": "black",
            "Помаранчевий": "orange",
            "Фіолетовий": "purple"
        }
        
        # Створення інтерфейсу
        self.setup_ui()
    
    def setup_ui(self):
        """Створення елементів інтерфейсу"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Ліва панель з параметрами
        control_frame = ttk.LabelFrame(main_frame, text="Параметри руху", padding="10")
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        row = 0
        
        # x₀
        ttk.Label(control_frame, text="x₀ (м):").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(control_frame, textvariable=self.x0_var, width=15).grid(row=row, column=1, padx=5, pady=5)
        row += 1
        
        # y₀
        ttk.Label(control_frame, text="y₀ (м):").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(control_frame, textvariable=self.y0_var, width=15).grid(row=row, column=1, padx=5, pady=5)
        row += 1
        
        # Кут
        ttk.Label(control_frame, text="Кут (градуси):").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(control_frame, textvariable=self.angle_var, width=15).grid(row=row, column=1, padx=5, pady=5)
        row += 1
        
        # v₀
        ttk.Label(control_frame, text="v₀ (м/с):").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(control_frame, textvariable=self.v0_var, width=15).grid(row=row, column=1, padx=5, pady=5)
        row += 1
        
        # a
        ttk.Label(control_frame, text="a (м/с²):").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(control_frame, textvariable=self.a_var, width=15).grid(row=row, column=1, padx=5, pady=5)
        row += 1
        
        # Колір
        ttk.Label(control_frame, text="Колір лінії:").grid(row=row, column=0, sticky=tk.W, pady=5)
        color_combo = ttk.Combobox(control_frame, textvariable=self.color_var, 
                                   values=list(self.colors.keys()), width=13)
        color_combo.grid(row=row, column=1, padx=5, pady=5)
        color_combo.current(0)
        row += 1
        
        ttk.Separator(control_frame, orient=tk.HORIZONTAL).grid(row=row, column=0, columnspan=2, sticky=tk.EW, pady=15)
        row += 1
        
        # Кнопки (поки без команд)
        ttk.Button(control_frame, text="Побудувати траєкторію").grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        ttk.Button(control_frame, text="Очистити графік").grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        ttk.Button(control_frame, text="За замовчуванням").grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        ttk.Button(control_frame, text="Вихід", command=self.root.quit).grid(row=row, column=0, columnspan=2, pady=20)
        
        # Права панель з графіком
        plot_frame = ttk.LabelFrame(main_frame, text="Графік траєкторії", padding="5")
        plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.plot_container = ttk.Frame(plot_frame)
        self.plot_container.pack(fill=tk.BOTH, expand=True)

    """
    Фаза 3.2: Налаштовання об'єктів графіка
    Тільки метод setup_ui()
    """
    def setup_plot(self):
        """Створення об'єктів графіка matplotlib"""
       
    
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.ax.set_xlabel('x (м)')
        self.ax.set_ylabel('y (м)')
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
        self.ax.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
    
        self.x_limits = (-10, 60)
        self.y_limits = (-10, 60)
        self.ax.set_xlim(self.x_limits)
        self.ax.set_ylim(self.y_limits)
        self.ax.set_aspect('equal')
    
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_container)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    app = RectilinearMotionApp(root)
    root.mainloop()
    
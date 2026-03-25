# тут буде код програми
"""
Лабораторна робота №1.1
Тема: Моделювання кінематики прямолінійного руху
Виконав: Мусін Михайло Олександрович
Група: 
Дата: 2026

Waterfall Phase 3: Implementation (повна версія з tkinter)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox


class RectilinearMotionApp:
    """
    Головний клас додатку для моделювання прямолінійного руху
    """
    
    def __init__(self, root):
        """
        Ініціалізація головного вікна та елементів інтерфейсу
        Waterfall Phase 2: Design
        """
        self.root = root
        self.root.title("Моделювання прямолінійного руху")
        self.root.geometry("900x600")
        self.root.resizable(True, True)
        
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
        
        # Фіксовані межі графіка
        self.x_limits = (-10, 60)
        self.y_limits = (-10, 60)
        
        # Створення інтерфейсу
        self.setup_ui()
        
        # Ініціалізація графіка
        self.setup_plot()
        
        # Прапорець, чи був вже побудований графік
        self.plot_exists = False
    
    def setup_ui(self):
        """
        Створення елементів інтерфейсу
        Waterfall Phase 3.1: UI Implementation
        """
        # Головний контейнер
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Ліва панель з параметрами
        control_frame = ttk.LabelFrame(main_frame, text="Параметри руху", padding="10")
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Поля введення
        row = 0
        
        # x0
        ttk.Label(control_frame, text="x₀ (м):").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(control_frame, textvariable=self.x0_var, width=15).grid(row=row, column=1, padx=5, pady=5)
        row += 1
        
        # y0
        ttk.Label(control_frame, text="y₀ (м):").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(control_frame, textvariable=self.y0_var, width=15).grid(row=row, column=1, padx=5, pady=5)
        row += 1
        
        # Кут
        ttk.Label(control_frame, text="Кут (градуси):").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(control_frame, textvariable=self.angle_var, width=15).grid(row=row, column=1, padx=5, pady=5)
        row += 1
        
        # Початкова швидкість
        ttk.Label(control_frame, text="v₀ (м/с):").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(control_frame, textvariable=self.v0_var, width=15).grid(row=row, column=1, padx=5, pady=5)
        row += 1
        
        # Прискорення
        ttk.Label(control_frame, text="a (м/с²):").grid(row=row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(control_frame, textvariable=self.a_var, width=15).grid(row=row, column=1, padx=5, pady=5)
        row += 1
        
        # Вибір кольору
        ttk.Label(control_frame, text="Колір лінії:").grid(row=row, column=0, sticky=tk.W, pady=5)
        color_combo = ttk.Combobox(control_frame, textvariable=self.color_var, 
                                   values=list(self.colors.keys()), width=13)
        color_combo.grid(row=row, column=1, padx=5, pady=5)
        color_combo.current(0)  # Синій за замовчуванням
        row += 1
        
        # Розділювач
        ttk.Separator(control_frame, orient=tk.HORIZONTAL).grid(row=row, column=0, columnspan=2, sticky=tk.EW, pady=15)
        row += 1
        
        # Кнопки керування
        ttk.Button(control_frame, text="Побудувати траєкторію", 
                  command=self.plot_trajectory).grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        
        ttk.Button(control_frame, text="Очистити графік", 
                  command=self.clear_plot).grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        
        ttk.Button(control_frame, text="За замовчуванням", 
                  command=self.reset_defaults).grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        
        ttk.Button(control_frame, text="Вихід", 
                  command=self.root.quit).grid(row=row, column=0, columnspan=2, pady=20)
        
        # Права панель з графіком
        plot_frame = ttk.LabelFrame(main_frame, text="Графік траєкторії", padding="5")
        plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Місце для графіка matplotlib
        self.plot_container = ttk.Frame(plot_frame)
        self.plot_container.pack(fill=tk.BOTH, expand=True)
    
    def setup_plot(self):
        """
        Створення об'єктів графіка matplotlib
        Waterfall Phase 3.2: Plot Setup
        """
        # Створення фігури та осей
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        
        # Налаштування графіка за замовчуванням
        self.ax.set_xlabel('x (м)')
        self.ax.set_ylabel('y (м)')
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
        self.ax.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
        
        # Встановлення фіксованих меж графіка
        self.ax.set_xlim(self.x_limits)
        self.ax.set_ylim(self.y_limits)
        
        self.ax.set_aspect('equal')
        
        # Вбудовування графіка в tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_container)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def validate_input(self):
        """
        Перевірка коректності введених даних
        Waterfall Phase 3.3: Validation Module
        
        Повертає: (is_valid, error_message)
        """
        try:
            x0 = self.x0_var.get()
            y0 = self.y0_var.get()
            angle = self.angle_var.get()
            v0 = self.v0_var.get()
            a = self.a_var.get()
            
            # Перевірка на невід'ємність (крім прискорення)
            if x0 < 0:
                return False, f"x₀ = {x0} не може бути від'ємним"
            if y0 < 0:
                return False, f"y₀ = {y0} не може бути від'ємним"
            if angle < 0:
                return False, f"Кут = {angle} не може бути від'ємним"
            if v0 < 0:
                return False, f"v₀ = {v0} не може бути від'ємним"
            
            # Прискорення може бути будь-яким (від'ємне - гальмування)
            
            return True, "Дані коректні"
            
        except tk.TclError:
            return False, "Помилка: всі поля мають містити числа"
    
    def calculate_trajectory(self):
        """
        Обчислення траєкторії руху
        Waterfall Phase 3.4: Calculation Module
        
        Повертає: (x_array, y_array, t_array)
        """
        # Отримання значень
        x0 = self.x0_var.get()
        y0 = self.y0_var.get()
        angle = self.angle_var.get()
        v0 = self.v0_var.get()
        a = self.a_var.get()
        
        # Перетворення кута в радіани
        alpha = np.radians(angle)
        
        # Проекції швидкості
        vx = v0 * np.cos(alpha)
        vy = v0 * np.sin(alpha)
        
        # Проекції прискорення
        ax = a * np.cos(alpha)
        ay = a * np.sin(alpha)
        
        # Визначення часу моделювання
        t_max = 20.0
        
        if abs(vx) > 0.01:
            t_from_x = 50.0 / abs(vx)
            t_max = min(t_max, t_from_x)
        
        # Генерація часу (500 точок для плавності)
        t = np.linspace(0, t_max, 500)
        
        # Обчислення координат
        x = x0 + vx * t + 0.5 * ax * t**2
        y = y0 + vy * t + 0.5 * ay * t**2
        
        return x, y, t
    
    def plot_trajectory(self):
        """
        Побудова траєкторії на графіку
        Waterfall Phase 3.5: Visualization Module
        """
        # Валідація даних
        is_valid, message = self.validate_input()
        if not is_valid:
            messagebox.showerror("Помилка введення", message)
            return
        
        try:
            # Обчислення траєкторії
            x, y, t = self.calculate_trajectory()
            
            # Отримання кольору
            color_name = self.color_var.get()
            color = self.colors.get(color_name, "blue")
            
            # Очищення попереднього графіка (тільки ліній, не осей)
            for line in self.ax.lines:
                line.remove()
            
            # Побудова нової траєкторії
            self.ax.plot(x, y, color=color, linewidth=2, label='Траєкторія')
            
            # Позначення початкової точки
            self.ax.plot(x[0], y[0], 'go', markersize=8, 
                        label=f'Початок ({x[0]:.2f}, {y[0]:.2f})')
            
            # Позначення кінцевої точки
            self.ax.plot(x[-1], y[-1], 'ro', markersize=8, 
                        label=f'Кінець ({x[-1]:.2f}, {y[-1]:.2f})')
            
            # Оновлення легенди
            self.ax.legend()
            
            # Оновлення графіка (межі залишаються фіксованими)
            self.canvas.draw()
            
            # Встановлення прапорця, що графік існує
            self.plot_exists = True
            
        except Exception as e:
            messagebox.showerror("Помилка обчислення", f"Сталася помилка: {str(e)}")
    
    def clear_plot(self):
        """
        Очищення графіка
        Waterfall Phase 3.6: Clear Function
        """
        # Видалення всіх ліній з графіка
        for line in self.ax.lines:
            line.remove()
        
        # Оновлення графіка
        self.canvas.draw()
        self.plot_exists = False
    
    def reset_defaults(self):
        """
        Скидання до значень за замовчуванням
        """
        self.x0_var.set(0.0)
        self.y0_var.set(0.0)
        self.angle_var.set(45.0)
        self.v0_var.set(10.0)
        self.a_var.set(0.0)
        self.color_var.set("Синій")
        
        # Очищення графіка
        self.clear_plot()


def main():
    """
    Головна функція програми
    Waterfall Phase 3.7: Main Function Integration
    """
    root = tk.Tk()
    app = RectilinearMotionApp(root)
    
    # Центрування вікна
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
    root.mainloop()


if __name__ == "__main__":
    main()
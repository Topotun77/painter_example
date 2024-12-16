import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw


class DrawingApp:
    """  Класс для GUI-приложения  """
    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def set_brush(self, choice):
        self.brush_size_scale.set(int(choice))

    def setup_ui(self):
        """  Виджеты управления  """
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        self.brush_size_scale = tk.Scale(control_frame, from_=1, to=20, orient=tk.HORIZONTAL)
        self.brush_size_scale.pack(side=tk.LEFT)

        sizes = [1, 2, 5, 10, 20]
        variable = tk.StringVar()
        variable.set(str(sizes[4]))
        self.menu_brush = tk.OptionMenu(control_frame, variable, *sizes, command=self.set_brush)
        self.menu_brush.pack(side=tk.LEFT)

    def paint(self, event):
        """
        Функция вызывается при движении мыши с нажатой левой кнопкой по холсту.
        Рисует линии на холсте Tkinter и параллельно на объекте Image из Pillow.
        Линии рисуются между текущей и последней зафиксированной позициями курсора,
        что создает непрерывное изображение.
        :param event: Событие содержит координаты мыши, которые используются для рисования.
        """
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size_scale.get(), fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.brush_size_scale.get())

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        """
        Сбрасывает последние координаты кисти. Необходимо для корректного начала
        новой линии после того, как пользователь отпустил кнопку мыши и снова начал рисовать.
        :param event: Событие содержит координаты мыши.
        """
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        """
        Очищает холст, удаляя все нарисованное, и пересоздает объекты Image и ImageDrawдля нового изображения.
        """
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self):
        """
        Открывает стандартное диалоговое окно выбора цвета и устанавливает выбранный цвет как текущий для кисти.
        """
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]

    def save_image(self):
        """
        Позволяет пользователю сохранить изображение, используя стандартное диалоговое окно для сохранения файла.
        В случае успешного сохранения выводится сообщение об этом.
        """
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
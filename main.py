import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw, ImageTk
from settings import *
from utilities import image_to_icon


class DrawingApp:
    """  Класс для GUI-приложения  """
    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")
        self.root.minsize(610, 450)
        try:
            self.root.iconbitmap(default="./icon/favicon.ico")
            # TODO Для компиляции с помощью auto-py-to-exe заменить строку выше на:
            # self.root.iconbitmap(default=path.join(sys._MEIPASS, "./icon/favicon.ico"))
        except:
            pass

        self.bg_color = 'white'
        self.width = 600
        self.height = 400
        self.image = Image.new("RGB", (self.width, self.height), color=self.bg_color)
        self.draw = ImageDraw.Draw(self.image)

        self.icon_save = image_to_icon(ICON_SAVE)
        self.icon_insert = image_to_icon(ICON_INSERT)
        self.icon_new = image_to_icon(ICON_NEW)
        self.icon_brash = image_to_icon(ICON_BRASH)
        # self.icon_pipette = image_to_icon(ICON_PIPETTE)
        self.icon_palette = image_to_icon(ICON_PALETTE)
        self.icon_eraser = image_to_icon(ICON_ERASER)

        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg=self.bg_color)
        self.canvas.pack(expand=True)

        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'
        self.pen_color_save = self.pen_color

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<Button-3>', self.pick_color)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def set_brush(self, choice):
        """  Выбор размера кисти  """
        self.brush_size_scale.set(int(choice))

    def setup_ui(self):
        """  Виджеты управления  """
        control_frame = tk.Frame(self.root, relief=tk.RAISED, border=2)
        control_frame.pack(fill=tk.BOTH)

        save_button = tk.Button(control_frame, image=self.icon_save, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, image=self.icon_insert, text="Вставить", command=self.image_insert)
        save_button.pack(side=tk.LEFT)

        clear_button = tk.Button(control_frame, image=self.icon_new, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, image=self.icon_palette, text="Палитра", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        # pipette_button = tk.Button(control_frame, image=self.icon_pipette, text="Пипетка", command=self.choose_color)
        # pipette_button.pack(side=tk.LEFT)

        pen_button = tk.Button(control_frame, image=self.icon_brash, text="Кисть", command=self.pen_image)
        pen_button.pack(side=tk.LEFT)

        eraser_button = tk.Button(control_frame, image=self.icon_eraser, text="Ластик", command=self.eraser_image)
        eraser_button.pack(side=tk.LEFT)

        self.brush_size_scale = tk.Scale(control_frame, from_=5, to=20, orient=tk.HORIZONTAL)
        self.brush_size_scale.pack(side=tk.LEFT)

        sizes = [1, 2, 5, 10, 20]
        variable = tk.StringVar()
        variable.set(str(sizes[2]))
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
        self.image = Image.new("RGB", (self.width, self.height), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self):
        """
        Открывает стандартное диалоговое окно выбора цвета и устанавливает выбранный цвет как текущий для кисти.
        """
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]
        self.pen_color_save = self.pen_color

    def pick_color(self, event):
        """
        Инструмент в виде пипетки для выбора цвета.
        """
        self.pen_color = "#{:02X}{:02X}{:02X}".format(*self.image.getpixel((event.x, event.y)))
        self.pen_color_save = self.pen_color

    def pen_image(self):
        """
        Выбирает инструмент кисть. Возвращает сохраненное значение цвета кисти.
        """
        self.pen_color = self.pen_color_save

    def eraser_image(self):
        """
        Устанавливает цвет кисти в цвет фона для инструмента ластик.
        """
        self.pen_color = self.bg_color

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

    def image_insert(self):
        """
        Вставить картинку из файла.
        """
        image = Image.open(filedialog.askopenfile(filetypes=[("JPG files", ".jpg"), ("PNG files", ".png")]).name)
        self.photo = ImageTk.PhotoImage(image)
        # self.image.paste(self.photo, (0, 0, 600, 400))
        # for x in range(self.photo.width()):
        #     for y in range(self.photo.height()):
        #         self.image.putpixel((x, y), self.photo.(x, y))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, simpledialog, font
from PIL import Image, ImageDraw, ImageTk, ImageFont, ImageGrab
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
        self.pen_color = 'black'
        self.width = 600
        self.height = 400
        self.text = ''
        self.font = 'Times 20'
        self.image = Image.new("RGB", (self.width, self.height), color=self.bg_color)
        self.draw = ImageDraw.Draw(self.image)

        self.icon_save = image_to_icon(ICON_SAVE)
        self.icon_insert = image_to_icon(ICON_INSERT)
        self.icon_new = image_to_icon(ICON_NEW)
        self.icon_brash = image_to_icon(ICON_BRASH)
        # self.icon_pipette = image_to_icon(ICON_PIPETTE)
        self.icon_palette = image_to_icon(ICON_PALETTE)
        self.icon_eraser = image_to_icon(ICON_ERASER)
        self.icon_resize = image_to_icon(ICON_RESIZE)
        self.icon_text = image_to_icon(ICON_TEXT)
        self.icon_fon = image_to_icon(ICON_FON)

        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg=self.bg_color)
        self.canvas.pack(expand=True)

        self.last_x, self.last_y = None, None
        self.pen_color_save = self.pen_color

        self.setup_ui()

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<Button-3>', self.pick_color)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.root.bind('<Control-s>', self.save_image)
        self.root.bind('<Control-c>', self.choose_color)

    def set_brush(self, choice):
        """  Выбор размера кисти  """
        self.brush_size_scale.set(int(choice))

    def setup_ui(self):
        """  Виджеты управления  """
        control_frame = tk.Frame(self.root, relief=tk.RAISED, border=2)
        control_frame.pack(fill=tk.BOTH)

        save_button = tk.Button(control_frame, image=self.icon_save, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        insert_button = tk.Button(control_frame, image=self.icon_insert, text="Вставить", command=self.image_insert)
        insert_button.pack(side=tk.LEFT)

        clear_button = tk.Button(control_frame, image=self.icon_new, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        resize_button = tk.Button(control_frame, image=self.icon_resize, text="Изменить размер",
                                  command=self.image_resize)
        resize_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, image=self.icon_palette, text="Палитра", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        fon_button = tk.Button(control_frame, image=self.icon_fon, text="Фон", command=self.choose_fon)
        fon_button.pack(side=tk.LEFT)

        pen_button = tk.Button(control_frame, image=self.icon_brash, text="Кисть", command=self.pen_image)
        pen_button.pack(side=tk.LEFT)

        eraser_button = tk.Button(control_frame, image=self.icon_eraser, text="Ластик", command=self.eraser_image)
        eraser_button.pack(side=tk.LEFT)

        text_button = tk.Button(control_frame, image=self.icon_text, text="Текст", command=self.insert_text)
        text_button.pack(side=tk.LEFT)

        self.canvas_color = tk.Canvas(control_frame, width=20, height=20, bg=self.pen_color)
        self.canvas_color.pack(side=tk.RIGHT, padx=8)

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
        self.image = Image.new("RGB", (self.width, self.height), color=self.bg_color)
        self.draw = ImageDraw.Draw(self.image)

    def image_resize(self):
        """
        Изменяет размер холста. При изменении размера картинка масштабируется.
        После чего можно продолжить рисовать.
        """
        try:
            x, y = map(int, simpledialog.askstring('Изменение размера изображения', 'Введите ширину и высоту изображения (разделитель - пробел):',
                                                   parent=self.root).split())
        except ValueError:
            messagebox.showerror(title='Ошибка', message='Вы ввели неверные значения')
            return
        except AttributeError:
            return
        self.width, self.height = x, y
        self.image = self.image.resize((x, y))
        # self.image.show()
        self.photo = ImageTk.PhotoImage(self.image)
        self.draw = ImageDraw.Draw(self.image)
        self.canvas.config(width=self.width, height=self.height)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

    def choose_color(self, event=None):
        """
        Открывает стандартное диалоговое окно выбора цвета и устанавливает выбранный цвет как текущий для кисти.
        """
        pen_color = colorchooser.askcolor(color=self.pen_color, title='Цвет кисти')[1]
        if pen_color:
            self.pen_color = pen_color
            self.pen_color_save = self.pen_color
            self.canvas_color['bg'] = self.pen_color

    def choose_fon(self, event=None):
        """
        Открывает стандартное диалоговое окно выбора цвета фона.
        """
        bg_color = colorchooser.askcolor(color=self.bg_color, title='Цвет фона')[1]
        if bg_color:
            self.bg_color = bg_color
            self.canvas.config(background=self.bg_color)

    def pick_color(self, event):
        """
        Инструмент в виде пипетки для выбора цвета.
        """
        self.pen_color = "#{:02X}{:02X}{:02X}".format(*self.image.getpixel((event.x, event.y)))
        self.pen_color_save = self.pen_color
        self.canvas_color['bg'] = self.pen_color

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

    def insert_text(self):
        """
        Вставить текст. Запрашиваем текст для вставки и параметры шрифта.
        Цвет текста берется из цвета кисти.
        """
        self.text = simpledialog.askstring('Добавить текст', 'Введите текст для вставки:',
                                           initialvalue=self.text, parent=self.root)
        if self.text:
            self.root.tk.call("tk", "fontchooser", "configure", "-font", self.font,
                              "-command", self.root.register(self.font_changed))
            self.root.tk.call("tk", "fontchooser", "show")
            self.canvas.bind('<Button-1>', self.put_text)

    def font_changed(self, font):
        """
        Сохранить полученное значение шрифта.
        :param font: Выбранный шрифт.
        """
        self.font = font

    def put_text(self, event):
        """
        Вставить текст в изображение.
        :param event: Событие с координатами точки клика мыши.
        """
        x, y = event.x, event.y
        self.draw.text((x, y), text=self.text, fill=self.pen_color)
        self.canvas.create_text(x, y, text=self.text, fill=self.pen_color, font=self.font)
        self.canvas.unbind('<Button-1>')

    def save_image(self, event=None):
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
        self.image = Image.open(filedialog.askopenfile(filetypes=[("JPG files", ".jpg"), ("PNG files", ".png")]).name)
        self.photo = ImageTk.PhotoImage(self.image)
        self.draw = ImageDraw.Draw(self.image)
        self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
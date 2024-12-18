from PIL import ImageTk, Image


def image_to_icon(file: str, min_x=20, min_y=20):
    """
    Изменение размера картинки для иконки.
    :param file: Имя файла.
    :param min_x: Размер по горизонтали.
    :param min_y: Размер по вертикали.
    :return: Объект ImageTk.PhotoImage.
    """
    try:
        im = Image.open(file)
        im = im.resize((min_x, min_y))
    except:
        return None
    return ImageTk.PhotoImage(im)

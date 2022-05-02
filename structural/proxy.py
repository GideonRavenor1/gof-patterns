"""
Паттерн Заместитель (Proxy) предоставляет объект-заместитель,
который управляет доступом к другому объекту. То есть создается
объект-суррогат, который может выступать в роли другого объекта и замещать его.
Когда использовать прокси?

    1. Когда надо осуществлять взаимодействие по сети, а объект-проси должен
    имитировать поведения объекта в другом адресном пространстве.
    Использование прокси позволяет снизить накладные издержки при передаче
    данных через сеть. Подобная ситуация еще называется удалённый заместитель
    (remote proxies)

    2. Когда нужно управлять доступом к ресурсу, создание которого требует
    больших затрат. Реальный объект создается только тогда, когда он
    действительно может понадобиться, а до этого все запросы к нему
    обрабатывает прокси-объект. Подобная ситуация еще называется виртуальный
    заместитель (virtual proxies)

    3. Когда необходимо разграничить доступ к вызываемому объекту в
    зависимости от прав вызывающего объекта.
    Подобная ситуация еще называется защищающий заместитель
    (protection proxies)

    4. Когда нужно вести подсчет ссылок на объект или обеспечить
    потокобезопасную работу с реальным объектом. Подобная ситуация
    называется "умные ссылки" (smart reference)

Недостатки:
    1. Увеличение времени отклика от сервиса/модуля.
    2. Усложнение кода
"""
from abc import (
    ABC,
    abstractmethod,
)
from functools import partial


class ImageBase(ABC):
    """Абстрактное изображение"""

    @abstractmethod
    def draw(self, x, y, color):
        """Рисует точку заданным цветом"""
        pass

    @abstractmethod
    def fill(self, color):
        """Заливка цветом"""
        pass

    @abstractmethod
    def save(self, filename):
        """Сохраняет изображение в файл"""
        pass


class Image(ImageBase):
    """Изображение"""

    def __init__(self, width, height):
        self._width = int(width)
        self._height = int(height)
        print(
            'Создаю изображение шириной %s и высотой %s' % (
                self._width,
                self._height,
            )
        )

    def draw(self, x, y, color):
        print('Рисуем точку; координаты: (%s, %s); цвет: %s' % (x, y, color))

    def fill(self, color):
        print('Заливка цветом %s' % color)

    def save(self, filename):
        print('Сохраняем изображение в файл %s' % filename)


class ImageProxy(ImageBase):
    """
    Заместитель изображения.
    Откладывает выполнение операций над изображением до момента его сохранения.
    """

    def __init__(self, *args, **kwargs):
        self._image = Image(*args, **kwargs)
        self.operations = []

    def draw(self, *args):
        func = partial(self._image.draw, *args)
        self.operations.append(func)

    def fill(self, *args):
        func = partial(self._image.fill, *args)
        self.operations.append(func)

    def save(self, filename):
        # выполняем все операции над изображением
        [func() for func in self.operations]
        # сохраняем изображение
        self._image.save(filename)


if __name__ == '__main__':
    img = ImageProxy(200, 200)
    img.fill('gray')
    img.draw(0, 0, 'green')
    img.draw(0, 1, 'green')
    img.draw(1, 0, 'green')
    img.draw(1, 1, 'green')
    img.save('image.png')

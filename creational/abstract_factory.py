"""
Паттерн "Абстрактная фабрика" (Abstract Factory) предоставляет интерфейс для
создания семейств взаимосвязанных объектов с определенными интерфейсами
без указания конкретных типов данных объектов.
Когда использовать абстрактную фабрику

    1. Когда система не должна зависеть от способа создания и
    компоновки новых объектов

    2. Когда создаваемые объекты должны использоваться вместе и
    являются взаимосвязанными

Недостатки: Усложнение кода программы за счет добавления множества
дополнительных классов.
"""

from abc import (
    ABC,
    abstractmethod,
)

"""
Базовые классы графического пользовательского интерфейса
"""


class StatusBar(ABC):
    def __init__(
        self,
        system: str,
    ):
        self._system = system

    @abstractmethod
    def create(self):
        pass


class MainMenu(ABC):
    def __init__(
        self,
        system: str,
    ):
        self._system = system

    @abstractmethod
    def create(self):
        pass


class MainWindow(ABC):
    def __init__(
        self,
        system: str,
    ):
        self._system = system

    @abstractmethod
    def create(self):
        pass


"""
Производные классы графического пользовательского интерфейса
для операционной системы Windows
"""


class WindowsStatusBar(StatusBar):
    def __init__(self):
        super().__init__('Windows')

    def create(self):
        print(f'Created status bar for {self._system}')


class WindowsMainMenu(MainMenu):
    def __init__(self):
        super().__init__('Windows')

    def create(self):
        print(f'Created main menu for {self._system}')


class WindowsMainWindow(MainWindow):
    def __init__(self):
        super().__init__('Windows')

    def create(self):
        print(f'Created MainWindow for {self._system}')


"""
Производные классы графического пользовательского интерфейса
для операционной системы Linux
"""


class LinuxStatusBar(StatusBar):
    def __init__(self):
        super().__init__('Linux')

    def create(self):
        print(f'Created status bar for {self._system}')


class LinuxMainMenu(MainMenu):
    def __init__(self):
        super().__init__('Linux')

    def create(self):
        print(f'Created main menu for {self._system}')


class LinuxMainWindow(MainWindow):
    def __init__(self):
        super().__init__('Linux')

    def create(self):
        print(f'Created MainWindow for {self._system}')


"""
Базовый класс абстрактной фабрики
"""


class GuiAbstractFactory(ABC):
    @abstractmethod
    def get_status_bar(self) -> StatusBar:
        pass

    @abstractmethod
    def get_main_menu(self) -> MainMenu:
        pass

    @abstractmethod
    def get_main_window(self) -> MainWindow:
        pass


"""
Производные классы абстрактной фабрики,
конкретные реализации для каждой из операционных систем
"""


class WindowsGuiFactory(GuiAbstractFactory):
    def get_status_bar(self) -> StatusBar:
        return WindowsStatusBar()

    def get_main_menu(self) -> MainMenu:
        return WindowsMainMenu()

    def get_main_window(self) -> MainWindow:
        return WindowsMainWindow()


class LinuxGuiFactory(GuiAbstractFactory):
    def get_status_bar(self) -> StatusBar:
        return LinuxStatusBar()

    def get_main_menu(self) -> MainMenu:
        return LinuxMainMenu()

    def get_main_window(self) -> MainWindow:
        return LinuxMainWindow()


"""
Клиентский класс, использующий фабрику для создания GUI
"""


class Application:
    def __init__(self, factory: GuiAbstractFactory):
        self._gui_factory = factory

    def create_gui(self):
        main_window = self._gui_factory.get_main_window()
        status_bar = self._gui_factory.get_status_bar()
        main_menu = self._gui_factory.get_main_menu()
        main_window.create()
        main_menu.create()
        status_bar.create()


def create_factory(system_name: str) -> GuiAbstractFactory:
    factory_dict = {
        'Windows': WindowsGuiFactory,
        'Linux': LinuxGuiFactory
    }
    return factory_dict[system_name]()


if __name__ == '__main__':
    system_name = 'Linux'
    ui = create_factory(system_name)
    app = Application(ui)
    app.create_gui()

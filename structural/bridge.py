"""
Мост (Bridge) - структурный шаблон проектирования, который позволяет отделить
абстракцию от реализации таким образом, чтобы и абстракцию,
и реализацию можно было изменять независимо друг от друга.

Даже если мы отделим абстракцию от конкретных реализаций, то у нас все равно
все наследуемые классы будут жестко привязаны к интерфейсу,
определяемому в базовом абстрактном классе.
Для преодоления жестких связей и служит паттерн Мост.
Когда использовать данный паттерн?

    1. Когда надо избежать постоянной привязки абстракции к реализации

    2. Когда наряду с реализацией надо изменять и абстракцию независимо друг
    от друга. То есть изменения в абстракции не должно привести к изменениям
    в реализации

Общая реализация паттерна состоит в объявлении классов абстракций и классов
реализаций в отдельных параллельных иерархиях классов.

Недостатки: Усложнение кода программы за счет добавления множества
дополнительных классов.
"""

import time
from abc import (
    ABC,
    abstractmethod,
)


class Pizza:
    """
    Класс пиццы для приготовления
    """

    def __init__(self, name: str, cook_time: int, temperature: int):
        self.name = name
        self.cook_time = cook_time
        self.cook_temperature = temperature
        self.__is_cook = False

    def cook(self) -> None:
        self.__is_cook = True

    def is_cooked(self) -> bool:
        return self.__is_cook


class IOvenImplementor(ABC):
    """
    Интерфейс для реализации печей различного типа
    """

    @abstractmethod
    def warm_up(self, temperature: int) -> None:
        pass

    @abstractmethod
    def cool_down(self, temperature: int) -> None:
        pass

    @abstractmethod
    def cook_pizza(self, pizza: Pizza) -> None:
        pass

    @abstractmethod
    def get_temperature(self) -> int:
        pass

    @abstractmethod
    def get_oven_type(self) -> str:
        pass


class ClassicOvenImplementor(IOvenImplementor):
    def __init__(self, temperature: int = 0):
        self.temperature = temperature
        self.type = 'ClassicStove'

    def warm_up(self, temperature: int) -> None:
        # разогрев классической печи
        time.sleep((temperature - self.temperature) / 10)
        print(
            f'Temperature warm up from {self.temperature}' f' to {temperature}'
        )
        self.temperature = temperature

    def cool_down(self, temperature: int) -> None:
        # остужаем классическую печь
        time.sleep((self.temperature - temperature) / 5)
        print(
            f'Temperature cool down from {self.temperature}'
            f' to {temperature}'
        )
        self.temperature = temperature

    def cook_pizza(self, pizza: Pizza) -> None:
        time.sleep(pizza.cook_time / 10)
        pizza.cook()

    def get_oven_type(self) -> str:
        return self.type

    def get_temperature(self) -> int:
        return self.temperature


class ElectricalOvenImplementor(IOvenImplementor):
    def __init__(self, temperature: int = 0):
        self.temperature = temperature
        self.type = 'ElectricalStove'

    def warm_up(self, temperature: int) -> None:
        # разогрев электрической печи
        time.sleep((temperature - self.temperature) / 30)
        print(
            f'Temperature warm up from {self.temperature}' f' to {temperature}'
        )
        self.temperature = temperature

    def cool_down(self, temperature: int) -> None:
        # остужаем электрическую печь
        time.sleep((self.temperature - temperature) / 20)
        print(
            f'Temperature cool down from {self.temperature}'
            f' to {temperature}'
        )
        self.temperature = temperature

    def cook_pizza(self, pizza: Pizza) -> None:
        time.sleep(pizza.cook_time / 10)
        pizza.cook()

    def get_oven_type(self) -> str:
        return self.type

    def get_temperature(self) -> int:
        return self.temperature


class Oven:
    def __init__(self, implementor: IOvenImplementor):
        self.__implementor = implementor

    def __prepare_stove(self, temperature: int):
        if self.__implementor.get_temperature() > temperature:
            self.__implementor.cool_down(temperature)
        elif self.__implementor.get_temperature() < temperature:
            self.__implementor.warm_up(temperature)
        else:
            print('Ideal temperature')
        print('Oven prepared!')

    def cook_pizza(self, pizza: Pizza) -> None:
        self.__prepare_stove(pizza.cook_temperature)
        print(
            f'Cooking {pizza.name} pizza for {pizza.cook_time}'
            f' minutes at {pizza.cook_temperature} C'
        )
        self.__implementor.cook_pizza(pizza)
        if pizza.is_cooked():
            print('Pizza is ready!!!')
        else:
            print('O_o ... some wrong ...')
        print('---------------------------')

    def change_implementor(self, implementor: IOvenImplementor) -> None:
        self.__implementor = implementor
        print('Implementor changed')

    def get_temperature(self) -> int:
        return self.__implementor.get_temperature()

    def get_implementor_name(self) -> str:
        return self.__implementor.get_oven_type()


if __name__ == '__main__':
    first_pizza = Pizza('Margarita', 10, 220)
    second_pizza = Pizza('Salami', 9, 180)

    implementor = ClassicOvenImplementor()
    oven = Oven(implementor)
    print(f'Implementor type: {oven.get_implementor_name()}')
    oven.cook_pizza(first_pizza)
    oven.cook_pizza(second_pizza)
    # замена реализации
    new_implementor = ElectricalOvenImplementor(oven.get_temperature())
    first_pizza = Pizza('Margarita', 9, 225)
    second_pizza = Pizza('Salami', 10, 175)
    oven.change_implementor(new_implementor)
    print(f'Implementor type: {oven.get_implementor_name()}')
    oven.cook_pizza(first_pizza)
    oven.cook_pizza(second_pizza)

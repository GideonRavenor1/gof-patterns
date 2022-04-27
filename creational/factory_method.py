"""
Фабричный метод (Factory Method) - это паттерн, который определяет интерфейс
для создания объектов некоторого класса, но непосредственное решение о том,
объект какого класса создавать происходит в подклассах.
То есть паттерн предполагает, что базовый класс делегирует создание объектов
классам-наследникам.
Когда надо применять паттерн

    1. Когда заранее неизвестно, объекты каких типов необходимо создавать

    2. Когда система должна быть независимой от процесса создания новых
    объектов и расширяемой: в нее можно легко вводить новые классы,
    объекты которых система должна создавать.

    3. Когда создание новых объектов необходимо делегировать из
    базового класса классам наследникам
"""

from enum import Enum


class PizzaType(Enum):
    """
    Перечисление текущих рецептов пицц в пиццерии,
    которые можно приготовить
    """
    MARGARITA = 0
    MEXICO = 1
    STELLA = 2


class Pizza:
    """
    Базовый класс для пицц, которые можно
    приготовить в пиццерии
    """

    def __init__(
        self,
        price: float,
    ):
        self.__price = price  # цена пиццы

    def get_price(self) -> float:
        return self.__price


class PizzaMargarita(Pizza):
    def __init__(self):
        super().__init__(3.5)


class PizzaMexico(Pizza):
    def __init__(self):
        super().__init__(17.5)


class PizzaStella(Pizza):
    def __init__(self):
        super().__init__(5.5)


def create_pizza(pizza_type: PizzaType) -> Pizza:
    """
    Factory Method
    """
    factory_dict = {
        PizzaType.MARGARITA: PizzaMargarita,
        PizzaType.MEXICO: PizzaMexico,
        PizzaType.STELLA: PizzaStella,
    }
    return factory_dict[pizza_type]()


if __name__ == '__main__':
    for pizza in PizzaType:
        my_pizza = create_pizza(pizza)
        print(f'Pizza type: {pizza}, price: {my_pizza.get_price()}')

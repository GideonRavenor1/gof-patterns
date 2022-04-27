"""
Строитель (Builder) - шаблон проектирования, который инкапсулирует создание
объекта и позволяет разделить его на различные этапы.
Когда использовать паттерн Строитель?

    1. Когда процесс создания нового объекта не должен зависеть от того,
    из каких частей этот объект состоит и как эти части связаны между собой

    2. Когда необходимо обеспечить получение различных вариаций объекта
    в процессе его создания

Версия без Директора(Director)
"""


from typing import ClassVar

from creational.builder_with_director import (
    PizzaSauceType,
    PizzaBase,
    PizzaDoughDepth,
    PizzaDoughType,
    PizzaTopLevelType,
)
"""
Класс компонуемого продукта
"""


class Pizza:
    def __init__(
        self, 
        builder: ClassVar,
    ):
        self.name = builder.name
        self.dough = builder.dough
        self.sauce = builder.sauce
        self.topping = builder.topping
        self.cooking_time = builder.cooking_time  # in minute

    def __str__(self):
        info: str = (
            f'Pizza name: {self.name} \n'
            f'dough type: {self.dough.DoughDepth.name} & '
            f'{self.dough.DoughType.name}\n'
            f"sauce type: {self.sauce.name} \n"
            f'topping: {[element.name for element in self.topping]} \n'
            f'cooking time: {self.cooking_time} minutes'
        )
        return info

    @staticmethod
    def get_builder():
        return _Builder()


"""
Реализация строителя (шеф-поваров) для сборки пицц
"""


class _Builder:
    def __init__(self):
        self.cooking_time = None
        self.topping = None
        self.sauce = None
        self.dough = None
        self.name = None

    def set_name(
        self,
        name: str,
    ):
        self.name = name

    def set_dough(
        self,
        pizza_base: PizzaBase,
    ):
        self.dough = pizza_base

    def set_sauce(
        self,
        sauce: PizzaSauceType,
    ):
        self.sauce = sauce

    def set_topping(
        self,
        topping: list,
    ):
        self.topping = topping

    def set_cooking_time(
        self,
        time: int,
    ):
        self.cooking_time = time

    def build(self):
        return Pizza(self)


if __name__ == '__main__':
    # Готовим пиццу Маргарита
    pizza_base = PizzaBase(
        PizzaDoughDepth.THICK,
        PizzaDoughType.WHEAT,
    )
    builder = Pizza.get_builder()
    builder.set_name('Margarita')
    builder.set_dough(pizza_base)
    builder.set_sauce(PizzaSauceType.TOMATO)
    builder.set_topping(
        [
            it for it in (
                PizzaTopLevelType.MOZZARELLA,
                PizzaTopLevelType.MOZZARELLA,
                PizzaTopLevelType.BACON,
            )
        ]
    )
    builder.set_cooking_time(10)
    pizza = builder.build()
    print(pizza)

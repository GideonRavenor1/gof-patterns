"""
Паттерн Прототип (Prototype) позволяет создавать объекты на основе уже ранее
созданных объектов-прототипов. То есть по сути данный паттерн предлагает
технику клонирования объектов.

Когда использовать Прототип?

    1. Когда конкретный тип создаваемого объекта должен определяться
    динамически во время выполнения

    2. Когда нежелательно создание отдельной иерархии классов фабрик
    для создания объектов-продуктов из параллельной иерархии классов
    (как это делается, например, при использовании
    паттерна Абстрактная фабрика)

    3. Когда клонирование объекта является более предпочтительным вариантом,
    нежели его создание и инициализация с помощью конструктора.
    Особенно когда известно, что объект может принимать небольшое ограниченное
    число возможных состояний.

Недостатки: Из-за ссылочной модели данных в питоне, сложно осуществить процесс
создания составных объектов, имеющие ссылки на другие объекты.
"""

from abc import (
    ABC,
    abstractmethod,
)
from typing import List
import copy
from creational.builder_with_director import (
    PizzaSauceType,
    PizzaBase,
    PizzaDoughDepth,
    PizzaDoughType,
    PizzaTopLevelType,
)


class IPrototype(ABC):
    @abstractmethod
    def clone(self): pass


"""
Класс компонуемого продукта
"""


class Pizza(IPrototype):
    def __init__(
        self,
        name,
        dough: PizzaBase = PizzaBase(
            PizzaDoughDepth.THICK,
            PizzaDoughType.WHEAT,
        ),
        sauce: PizzaSauceType = PizzaSauceType.TOMATO,
        topping: List[PizzaTopLevelType] = None,
        cooking_time: int = 10
    ):
        self.name = name
        self.dough = dough
        self.sauce = sauce
        self.topping = topping
        self.cooking_time = cooking_time  # in minute

    def __str__(self):
        toppings = (
            [it.name for it in self.topping]
            if self.topping is not None else 'None'
        )
        info: str = (
            f'Pizza name: {self.name} \n'
            f'dough type: {self.dough.DoughDepth.name} & '
            f'{self.dough.DoughType.name}\n'
            f'sauce type: {self.sauce.name} \n'
            f'topping: {toppings} \n'
            f'cooking time: {self.cooking_time} minutes\n'
            f'-----------------------------------------'
        )

        return info

    def clone(self):
        topping = self.topping.copy() if self.topping is not None else None
        return type(self)(
            self.name,
            self.dough,
            self.sauce,
            topping,
            self.cooking_time,
        )


if __name__ == '__main__':
    pizza = Pizza(
        'Margarita', topping=[
            PizzaTopLevelType.MOZZARELLA,
            PizzaTopLevelType.MOZZARELLA,
            PizzaTopLevelType.BACON
        ]
    )

    print(pizza)
    new_pizza = pizza.clone()  # клонируем объект
    new_pizza.name = 'New_Margarita'
    print(new_pizza)
    # Вместо паттерна можно использовать метод deepcopy
    # из встроенной библиотеки copy
    salami_pizza = copy.deepcopy(new_pizza)
    salami_pizza.name = 'Salami'
    salami_pizza.sauce = PizzaSauceType.BARBEQUE
    salami_pizza.topping.append(PizzaTopLevelType.SALAMI)
    print(salami_pizza)

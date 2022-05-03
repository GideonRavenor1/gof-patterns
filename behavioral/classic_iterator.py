"""
Паттерн Итератор (Iterator) предоставляет абстрактный интерфейс для
последовательного доступа ко всем элементам составного объекта
без раскрытия его внутренней структуры.
Когда использовать итераторы?
    1. Когда необходимо осуществить обход объекта без раскрытия его внутренней
    структуры

    2. Когда имеется набор составных объектов, и надо обеспечить единый
    интерфейс для их перебора

    3. Когда необходимо предоставить несколько альтернативных вариантов
    перебора одного и того же объекта
Недостатки: Если достаточно цикла, его применение не оправданно.
"""

from abc import (
    ABC, 
    abstractmethod,
)


class PizzaItem:
    def __init__(self, number):
        self.number = number

    def __str__(self):
        return f'кусочек пиццы под номером: {self.number}'


class Iterator(ABC):
    @abstractmethod
    def next(self) -> PizzaItem:
        pass

    @abstractmethod
    def has_next(self) -> bool:
        pass


class PizzaSliceIterator(Iterator):
    def __init__(self, pizza: list[PizzaItem]):
        self._pizza = pizza
        self._index = 0

    def next(self) -> PizzaItem:
        pizza_item = self._pizza[self._index]
        self._index += 1
        return pizza_item

    def has_next(self) -> bool:
        return False if self._index >= len(self._pizza) else True


class PizzaAggregate:
    def __init__(self, amount_slices: int = 10):
        self.slices = [PizzaItem(it + 1) for it in range(amount_slices)]
        print(f'Приготовили пиццу и порезали ' f'на {amount_slices} кусочков')

    def amount_slices(self) -> int:
        return len(self.slices)

    def iterator(self) -> Iterator:
        return PizzaSliceIterator(self.slices)


if __name__ == '__main__':
    pizza = PizzaAggregate(5)
    iterator = pizza.iterator()
    while iterator.has_next():
        item = iterator.next()
        print('Это ' + str(item))
    print('*' * 20)
    iterator = pizza.iterator()
    iterator.next()
    while iterator.has_next():
        item = iterator.next()
        print('Это ' + str(item))

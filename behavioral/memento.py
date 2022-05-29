"""
Паттерн Хранитель (Memento) позволяет выносить внутреннее состояние объекта за
его пределы для последующего возможного восстановления объекта без нарушения
принципа инкапсуляции.

Когда использовать Memento?

    1. Когда нужно сохранить состояние объекта для возможного последующего
    восстановления

    2. Когда сохранение состояния должно проходить без нарушения принципа
    инкапсуляции

То есть ключевыми понятиями для данного паттерна являются сохранение
внутреннего состояния и инкапсуляция, и важно соблюсти баланс между ними.
Ведь, как правило, если мы не нарушаем инкапсуляцию, то состояние объекта
хранится в объекте в приватных переменных. И не всегда для доступа к этим
переменным есть методы или свойства с сеттерами и геттерами.
Например, в игре происходит управление героем, все состояние которого
заключено в нем самом - оружие героя, показатель жизней, силы, какие-то
другие показатели. И нередко может возникнуть ситуация, сохранить все эти
показатели во вне, чтобы в будущем можно было откатиться к предыдущему уровню
и начать игру заново. В этом случае как раз и может помочь паттерн Хранитель.

Недостатки:
Требуется много памяти при создании большого количества снимков объекта.
"""


from typing import List


class Memento:
    """
    Класс Хранитель, фиксирующий текущее
    состояние наличия ингредиентов в пицце"""

    def __init__(self, state: List[str]) -> None:
        self.__state = state

    def get_state(self) -> List[str]:
        return self.__state[:]


class Pizza:
    """
    Класс приготовляемой шеф-поваром пиццы
    """

    def __init__(self) -> None:
        self.__state: List[str] = ['base']

    def add_ingredient(self, ingredient: str) -> None:
        print(f"В пиццу добавлен ингредиент: {ingredient}")
        self.__state.append(ingredient)

    def create_memento(self) -> Memento:
        return Memento(self.__state[:])

    def set_memento(self, memento: Memento) -> None:
        self.__state = memento.get_state()

    def __str__(self) -> str:
        return f"Текущее состояние пиццы: {self.__state}"


class Chief:
    def __init__(self, pizza: Pizza) -> None:
        self.pizza = pizza
        self.pizza_states: List[Memento] = []

    def add_ingredient_to_pizza(self, ingredient: str) -> None:
        self.pizza_states.append(self.pizza.create_memento())
        self.pizza.add_ingredient(ingredient)

    def undo_add_ingredient(self) -> None:
        if len(self.pizza_states) == 1:
            self.pizza.set_memento(self.pizza_states[0])
            print("Пицца вернулась в своё исходное состояние!")
            print(self.pizza)
        else:
            print("Отмена предыдущего действия")
            state = self.pizza_states.pop()
            self.pizza.set_memento(state)
            print(self.pizza)


if __name__ == "__main__":
    pizza = Pizza()
    chief = Chief(pizza)
    print(pizza)
    print("*" * 8 + "Добавляем ингридиенты в пиццу" + 8 * "*")
    chief.add_ingredient_to_pizza('соус')
    chief.add_ingredient_to_pizza('оливки')
    chief.add_ingredient_to_pizza('салями')
    chief.add_ingredient_to_pizza('сыр')
    print(pizza)
    print("*" * 4 + "Отменяем произведенные ранее действия" + 4 * "*")
    chief.undo_add_ingredient()
    chief.undo_add_ingredient()
    chief.undo_add_ingredient()
    chief.undo_add_ingredient()
    print("*" * 5 + "Вновь добавляем ингридиенты в пиццу" + 5 * "*")
    chief.add_ingredient_to_pizza('соус')
    chief.add_ingredient_to_pizza('4 сыра')
    print(pizza)

"""
Паттерн Стратегия (Strategy) представляет шаблон проектирования,
который определяет набор алгоритмов, инкапсулирует каждый из них и
обеспечивает их взаимозаменяемость.
В зависимости от ситуации мы можем легко заменить один используемый алгоритм
другим. При этом замена алгоритма происходит независимо от объекта, который
использует данный алгоритм.

Когда использовать стратегию?
    1. Когда есть несколько родственных классов, которые отличаются
    поведением. Можно задать один основной класс, а разные варианты поведения
    вынести в отдельные классы и при необходимости их применять

    2. Когда необходимо обеспечить выбор из нескольких вариантов алгоритмов,
    которые можно легко менять в зависимости от условий

    3. Когда необходимо менять поведение объектов на стадии выполнения
    программы

    4. Когда класс, применяющий определенную функциональность, ничего не
    должен знать о ее реализации
Недостатки:

    1. Для правильной настройки системы пользователь должен знать об
    особенностях всех алгоритмов.
    2. Число классов в системе, построенной с применением паттерна Strategy,
    возрастает.
"""


from abc import ABC, abstractmethod
from enum import Enum


class ChiefMood(Enum):
    """
    Настроение начальника
    """

    GOOD = 1
    BAD = 2
    BETTER_STAY_AWAY = 3


class Strategy(ABC):
    """
    Интерфейс стратегии
    """

    @abstractmethod
    def check_mood_chief(self, mood: ChiefMood) -> bool:
        ...

    @abstractmethod
    def order_processing(self, money: int) -> str:
        ...


class GoodStrategy(Strategy):
    def check_mood_chief(self, mood: ChiefMood) -> bool:
        if mood is ChiefMood.GOOD or mood is ChiefMood.BAD:
            return True
        return False

    def order_processing(self, money: int) -> str:
        return "Самый лучший напиток, который возможен!"


class BadStrategy(Strategy):
    def check_mood_chief(self, mood: ChiefMood) -> bool:
        if mood is ChiefMood.BETTER_STAY_AWAY or mood is ChiefMood.BAD:
            return True
        return False

    def order_processing(self, money: int) -> str:
        return "И стакан воды сойдет!"


class NormalStrategy(Strategy):
    def check_mood_chief(self, mood: ChiefMood) -> bool:
        # может у шефа и плохое настроение
        # но клиенты то тут не при чем
        return True

    def order_processing(self, money: int) -> str:
        match money:
            case _ if money < 5:
                return "Вежливо отказаться от заказа клиента"
            case _ if money < 10:
                return "Приготовить espresso"
            case _ if money < 20:
                return "Приготовить капучино"
            case _ if money < 50:
                return "Приготовить отменный кофе"
            case _:
                return "Самый лучший напиток, который возможен!"


class Barista:
    def __init__(self, strategy: Strategy, chief_mood: ChiefMood):
        self._strategy = strategy
        self._chief_mood = chief_mood
        print(f"Изначальное настроение шефа: {chief_mood.name}")

    def get_chief_mood(self) -> ChiefMood:
        return self._chief_mood

    def set_chief_mood(self, chief_mood: ChiefMood) -> None:
        print(f"Текущее настроение шефа: {chief_mood.name}")
        self._chief_mood = chief_mood

    def set_strategy(self, strategy: Strategy) -> None:
        self._strategy = strategy

    def take_order(self, money: int) -> None:
        print(f"Клиент отдает за заказ {money} рублей")
        if self._strategy.check_mood_chief(self._chief_mood):
            print(self._strategy.order_processing(money))
        else:
            print("Сделать вид, что не заметил клиента!")


if __name__ == "__main__":
    barista = Barista(NormalStrategy(), ChiefMood.BETTER_STAY_AWAY)
    barista.take_order(20)
    barista.take_order(50)
    barista.set_strategy(BadStrategy())
    barista.take_order(40)
    barista.take_order(200)
    barista.set_strategy(GoodStrategy())
    barista.take_order(40)
    barista.set_chief_mood(ChiefMood.GOOD)
    barista.take_order(0)

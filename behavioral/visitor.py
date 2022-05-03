"""
Паттерн Посетитель (Visitor) позволяет определить операцию для объектов
других классов без изменения этих классов.

При использовании паттерна Посетитель определяются две иерархии классов:
одна для элементов, для которых надо определить новую операцию,
и вторая иерархия для посетителей, описывающих данную операцию.

Когда использовать данный паттерн?
    1. Когда имеется много объектов разнородных классов с разными
    интерфейсами, и требуется выполнить ряд операций над каждым из этих
    объектов

    2. Когда классам необходимо добавить одинаковый набор операций без
    изменения этих классов

    3. Когда часто добавляются новые операции к классам, при этом общая
    структура классов стабильна и практически не изменяется

Недостатки:
    1. Вероятность нарушения инкапсуляции элементов.
    2. Неоправданность применения при частом изменении иерархии элементов.
"""


from abc import (
    ABC,
    abstractmethod,
)


class OrderItemVisitor(ABC):
    """
    Интерфейс посетителя
    """

    @abstractmethod
    def visit(self, item) -> float:
        pass


class ItemElement(ABC):
    """
    Интерфейс для заказываемых продуктов
    """

    @abstractmethod
    def accept(self, visitor: OrderItemVisitor) -> float:
        pass


class Pizza(ItemElement):
    """
    Класс заказываемой пиццы
    """

    def __init__(self, name: str, price: float):
        self.name = name
        self.price = price

    def get_price(self) -> float:
        return self.price

    def accept(self, visitor: OrderItemVisitor) -> float:
        return visitor.visit(self)


class Coffee(ItemElement):
    """
    Класс заказываемого кофе
    """

    def __init__(self, name: str, price: float, capacity: float):
        self.name = name
        self.price = price  # цена за литр кофе
        self.capacity = capacity

    def get_price(self) -> float:
        return self.price

    def get_capacity(self) -> float:
        return self.capacity

    def accept(self, visitor: OrderItemVisitor) -> float:
        return visitor.visit(self)


class WithOutDiscountVisitor(OrderItemVisitor):
    """
    Посчитываем сумму заказа с
    без учета скидки
    """

    def visit(self, item: ItemElement) -> float:
        cost = 0
        if isinstance(item, Pizza):
            cost = item.get_price()
        elif isinstance(item, Coffee):
            cost = item.get_capacity() * item.get_price()
        return cost


class OnlyPizzaDiscountVisitor(OrderItemVisitor):
    """
    Посчитываем сумму заказа с
    учетом скидки на всю пиццу в 15%
    """

    def visit(self, item: ItemElement) -> float:
        cost = 0
        if isinstance(item, Pizza):
            cost = item.get_price()
            cost -= cost * 0.15
        elif isinstance(item, Coffee):
            cost = item.get_capacity() * item.get_price()
        return cost


class OnlyCoffeeDiscountVisitor(OrderItemVisitor):
    """
    Посчитываем сумму заказа с
    учетом скидки на всё кофе в 35%
    """

    def visit(self, item: ItemElement) -> float:
        cost = 0
        if isinstance(item, Pizza):
            cost = item.get_price()
        elif isinstance(item, Coffee):
            cost = item.get_capacity() * item.get_price()
            cost -= cost * 0.35
        return cost


class AllDiscountVisitor(OrderItemVisitor):
    """
    Посчитываем сумму заказа с
    учетом скидки на всё в 20
    """

    def visit(self, item: ItemElement) -> float:
        cost = 0
        if isinstance(item, Pizza):
            cost = item.get_price()
        elif isinstance(item, Coffee):
            cost = item.get_capacity() * item.get_price()
        cost -= cost * 0.20
        return cost


class Waiter:
    def __init__(self, discount: OrderItemVisitor):
        self.order: list[ItemElement] = []
        self.discount_calculator = discount

    def set_order(self, order: list[ItemElement]) -> None:
        self.order = order

    def set_discount(self, discount: OrderItemVisitor) -> None:
        self.discount_calculator = discount

    def calculate_finish_price(self) -> float:
        price = 0
        if self.order:
            for item in self.order:
                price += item.accept(self.discount_calculator)
        return round(price, 2)


if __name__ == '__main__':
    order: list[ItemElement] = [
        Pizza('Маргарита', 12.3),
        Coffee('Латте', 5, 0.3),
        Pizza('4Сыра', 10.5),
        Pizza('Салями', 15.2),
        Coffee('Капучино', 4, 0.27),
    ]
    discount = WithOutDiscountVisitor()
    waiter = Waiter(discount)
    waiter.set_order(order)
    print(
        f'Сумма заказа без учета скидок: {waiter.calculate_finish_price()}'
    )
    discount = OnlyPizzaDiscountVisitor()
    waiter.set_discount(discount)
    print(
        'Сумма заказа c учетом скидки на пиццу: '
        f'{waiter.calculate_finish_price()}'
    )
    discount = OnlyCoffeeDiscountVisitor()
    waiter.set_discount(discount)
    print(
        'Сумма заказа c учетом скидки на кофе: '
        f'{waiter.calculate_finish_price()}'
    )
    discount = AllDiscountVisitor()
    waiter.set_discount(discount)
    print(
        'Сумма заказа c учетом скидки на всё: '
        f'{waiter.calculate_finish_price()}'
    )

"""
Мост (Bridge) - структурный шаблон проектирования, который позволяет отделить
абстракцию от реализации таким образом, чтобы и абстракцию, и реализацию можно
было изменять независимо друг от друга.

Даже если мы отделим абстракцию от конкретных реализаций, то у нас все равно
все наследуемые классы будут жестко привязаны к интерфейсу,
определяемому в базовом абстрактном классе.
Для преодоления жестких связей и служит паттерн Мост.
Когда использовать данный паттерн?

    1. Когда надо избежать постоянной привязки абстракции к реализации

    2. Когда наряду с реализацией надо изменять и абстракцию независимо друг
    от друга.
    То есть изменения в абстракции не должно привести к изменениям в реализации

Общая реализация паттерна состоит в объявлении классов абстракций и классов
реализаций в отдельных параллельных иерархиях классов.

Недостатки:
    1. В зависимости от конкретной ситуации и структуры проекта в целом,
    возможно негативное влияние на продуктивность программы (например,
    если нужно инициализировать большее количество объектов).
    2. Трудности наложения ограничений и состав композиции, которые могут
    входить в композицию из-за общего дизайна интерфейса классов.
"""


from abc import (
    ABC,
    abstractmethod,
)


class IProduct(ABC):
    """
    Интерфейс продуктов
    входящих в пиццу
    """

    @abstractmethod
    def cost(self) -> float:
        pass

    @abstractmethod
    def name(self) -> str:
        pass


class Product(IProduct):
    """
    Класс продукта
    """

    def __init__(self, name: str, cost: float):
        self.__cost = cost
        self.__name = name

    def cost(self) -> float:
        return self.__cost

    def name(self) -> str:
        return self.__name


class CompoundProduct(IProduct):
    """
    Класс компонуемых продуктов
    """

    def __init__(self, name: str):
        self.__name = name
        self.products = []

    def cost(self):
        cost = 0
        for it in self.products:
            cost += it.cost()
        return cost

    def name(self) -> str:
        return self.__name

    def add_product(self, product: IProduct):
        self.products.append(product)

    def remove_product(self, product: IProduct):
        self.products.remove(product)

    def clear(self):
        self.products = []


class Pizza(CompoundProduct):
    """
    Класс пиццы
    """

    def __init__(self, name: str):
        super(Pizza, self).__init__(name)

    def cost(self):
        cost = 0
        for it in self.products:
            cost_it = it.cost()
            print(f'Стоимость {it.name()} = {cost_it} тугриков')
            cost += cost_it
        print(f'Стоимость пиццы {self.name()} = {cost} тугриков')
        return cost


if __name__ == '__main__':
    dough = CompoundProduct('тесто')
    dough.add_product(Product('мука', 3))
    dough.add_product(Product('яйцо', 2.3))
    dough.add_product(Product('соль', 1))
    dough.add_product(Product('сахар', 2.1))
    sauce = Product('Барбекю', 12.1)
    topping = CompoundProduct('топпинг')
    topping.add_product(Product('Дор блю', 14))
    topping.add_product(Product('Пармезан', 12.3))
    topping.add_product(Product('Моцарелла', 9.54))
    topping.add_product(Product('Маасдам', 7.27))
    pizza = Pizza('4 сыра')
    pizza.add_product(dough)
    pizza.add_product(sauce)
    pizza.add_product(topping)
    print(pizza.cost())

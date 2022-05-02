"""
Паттерн Приспособленец (Flyweight, так же известен как Легковес и Кеш) -
структурный шаблон проектирования, который позволяет использовать
разделяемые объекты сразу в нескольких контекстах. Данный паттерн используется
преимущественно для оптимизации работы с памятью.

В качестве стандартного применения данного паттерна можно
привести следующий пример. Текст состоит из отдельных символов.
Каждый символ может встречаться на одной странице текста много раз.
Однако в компьютерной программе было бы слишком накладно выделять память для
каждого отдельного символа в тексте. Гораздо проще было бы определить
полный набор символов, например, в виде таблицы из 128 знаков
(алфавитно-цифровые символы в разных регистрах, знаки препинания и т.д.).
А в тексте применить этот набор общих разделяемых символов,
вместо сотен и тысяч объектов, которые могли бы использоваться в тексте.
И как следствие подобного подхода будет уменьшение количества используемых
объектов и уменьшение используемой памяти.

Паттерн Приспособленец следует применять при соблюдении всех следующих условий:

    1. Когда приложение использует большое количество однообразных объектов,
    из-за чего происходит выделение большого количества памяти

    2. Когда часть состояния объекта, которое является изменяемым,
    можно вынести во вне. Вынесение внешнего состояния позволяет заменить
    множество объектов небольшой группой общих разделяемых объектов.

Недостатки: Требуется дополнительное время (процессорные ресурсы) на поиск уже
существующего или вычисления контекста для создания нового объекта.

"""


class PizzaOrderFlyWeight:
    def __init__(self, shared_state):
        self.shared_state = shared_state

    def __repr__(self):
        return str(self.shared_state)


class PizzaOrderContext:
    def __init__(self, unique_state, flyweight: PizzaOrderFlyWeight):
        self.unique_state = unique_state
        self.flyweight = flyweight

    def __repr__(self):
        return (
            f'уникальное состояние: {self.unique_state} \n'
            f'разделяемое состояние: {self.flyweight}'
        )


class FlyWeightFactory:
    def __init__(self):
        self.flyweights = []

    def get_flyweight(self, shared_state) -> PizzaOrderFlyWeight:

        flyweights = list(
            filter(lambda x: x.shared_state == shared_state, self.flyweights)
        )
        if flyweights:
            return flyweights[0]
        else:
            flyweight = PizzaOrderFlyWeight(shared_state)
            self.flyweights.append(flyweight)
            return flyweight

    @property
    def total(self):
        return len(self.flyweights)


class PizzaOrderMaker:
    def __init__(self, flyweight_factory: FlyWeightFactory):
        self.flyweight_factory = flyweight_factory
        self.contexts = []

    def make_pizza_order(
        self, unique_state, shared_state
    ) -> PizzaOrderContext:
        flyweight = self.flyweight_factory.get_flyweight(shared_state)
        context = PizzaOrderContext(unique_state, flyweight)
        self.contexts.append(context)

        return context


if __name__ == '__main__':
    flyweight_factory = FlyWeightFactory()
    pizza_maker = PizzaOrderMaker(flyweight_factory)

    shared_states = [
        (30, 'Большая пицца'),
        (25, 'Средняя пицца'),
        (10, 'Маленькая пицца'),
    ]
    unique_states = ['Маргарита', 'Салями', '4 сыра']

    orders = [
        pizza_maker.make_pizza_order(x, y)
        for x in unique_states
        for y in shared_states
    ]

    print('Количество созданных пицц:', len(orders))
    print('Количество разделяемых объектов:', flyweight_factory.total)
    for index, pizza in enumerate(orders):
        print('-' * 20)
        print(f'Номер пиццы в списке: {index}')
        print(pizza)

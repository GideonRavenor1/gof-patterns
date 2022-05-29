"""
Паттерн "Наблюдатель" (Observer) представляет поведенческий шаблон
проектирования, который использует отношение "один ко многим".
В этом отношении есть один наблюдаемый объект и множество наблюдателей.
И при изменении наблюдаемого объекта автоматически происходит оповещение всех
наблюдателей.

Данный паттерн еще называют Publisher-Subscriber (издатель-подписчик),
поскольку отношения издателя и подписчиков характеризуют действие данного
паттерна: подписчики подписываются email-рассылку определенного сайта.
Сайт-издатель с помощью email-рассылки уведомляет всех подписчиков об
изменениях. А подписчики получают изменения и производят определенные
действия: могут зайти на сайт, могут проигнорировать уведомления и т.д.

Когда использовать паттерн Наблюдатель?
    1. Когда система состоит из множества классов, объекты которых должны
    находиться в согласованных состояниях

    2. Когда общая схема взаимодействия объектов предполагает две стороны:
    одна рассылает сообщения и является главным, другая получает сообщения и
    реагирует на них. Отделение логики обеих сторон позволяет их рассматривать
    независимо и использовать отдельно друга от друга.

    3. Когда существует один объект, рассылающий сообщения, и множество
    подписчиков, которые получают сообщения. При этом точное число подписчиков
    заранее неизвестно и процессе работы программы может изменяться.

Недостатки:
Основной недостаток “Наблюдателя”, как и большинства других паттернов, связан
с усложнением кода и увеличением числа классов, которые в нем нуждаются.
Но при работе с шаблонами с этим обстоятельством приходится мириться,
поскольку оно является средством достижения абстракции в коде.
"""


from abc import ABC, abstractmethod
from enum import Enum
from random import choice
from typing import List, Optional


class OrderType(Enum):
    """
    Типы возможных заказов
    """

    CAPPUCCINO = 1
    LATTE = 2
    ESPRESSO = 3


class Order:
    """
    Класс заказа
    """

    order_id: int = 1

    def __init__(self, order_type: OrderType) -> None:
        self.id = Order.order_id
        self.type = order_type
        Order.order_id += 1

    def __str__(self) -> str:
        return f"заказ под #{self.id} ({self.type.name})"


class Observer(ABC):
    @abstractmethod
    def update(self, order_id: int) -> None:
        ...


class Subject(ABC):
    def __init__(self) -> None:
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, order_id: int) -> None:
        for observer in self._observers:
            observer.update(order_id)


class Barista(Subject):
    def __init__(self) -> None:
        super().__init__()
        self.__orders: List[Order] = []
        self.__finish_order: List[Order] = []

    def take_order(self, order: Order) -> None:
        print(f"Бариста принял {order}")
        self.__orders.append(order)

    def get_order(self, order_id: int) -> Order:
        order = None
        for it in self.__finish_order:
            if it.id == order_id:
                order = it
                break
        self.__finish_order.remove(order)
        return order

    def processing_order(self) -> None:
        if self.__orders:
            order = choice(self.__orders)
            self.__orders.remove(order)
            self.__finish_order.append(order)
            print(f"Бариста выполнил {order}")
            self.notify(order.id)
        else:
            print("Бариста от нечего делать натирает кофемашину")


class Client(Observer):
    def __init__(self, name: str, barista: Barista) -> None:
        self.__barista = barista
        self.__name = name
        self.order: Optional[Order] = None

    def update(self, order_id: int) -> None:
        """принимаем номер текущего выполненного заказа
        и отписываемся от оповещения баристы"""
        if self.order is not None:
            if order_id == self.order.id:
                print(
                    f"Клиент {self.__name} забрал(а) "
                    f"{self.__barista.get_order(order_id)}"
                )
                self.__barista.detach(self)

    def create_order(self) -> None:
        """Метод для формирования заказа
        и подписки на оповещения от баристы
        по выполненному заказу"""
        order_type = choice(
            [OrderType.LATTE, OrderType.CAPPUCCINO, OrderType.ESPRESSO]
        )
        self.order = Order(order_type)
        print(f"Клиент {self.__name} сделал(а) {self.order}")
        self.__barista.attach(self)
        self.__barista.take_order(self.order)


if __name__ == "__main__":
    names = ['Анастасия', 'Анна', 'Роман', 'Ростислав', 'Руслан']
    barista = Barista()
    clients = [Client(name, barista) for name in names]
    for client in clients:
        print("*" * 30)
        client.create_order()
    print("*" * 4 + "Бариста приступает к выполнению заказов" + 4 * "*")
    for _ in range(6):
        print("*" * 30)
        barista.processing_order()

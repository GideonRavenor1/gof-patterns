"""
Одиночка (Singleton, Синглтон) - порождающий паттерн, который гарантирует,
что для определенного класса будет создан только один объект,
а также предоставит к этому объекту точку доступа.
Синглтон позволяет создать объект только при его необходимости.
Если объект не нужен, то он не будет создан.
В этом отличие синглтона от глобальных переменных.

Когда надо использовать Синглтон?
    1. Когда необходимо, чтобы для класса существовал только один экземпляр

Недостатки: Бездумное использование данного паттерна может привести к
плохому дизайну архитектуры.
Считается антипаттерном.
"""


class SingletonBaseClass(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonBaseClass, cls).\
                __call__(*args, **kwargs)
        return cls._instances[cls]


class MySingleton(metaclass=SingletonBaseClass):
    def __init__(self):
        self.name = 'Singleton'
        self.value_a = 3
        self.value_b = 5

    def add_a_b(self) -> int:
        return self.value_a + self.value_b

    def get_name(self) -> str:
        return self.name

    def set_name(
        self,
        name: str,
    ):
        self.name = name


if __name__ == '__main__':
    my_singleton1 = MySingleton()
    my_singleton2 = MySingleton()
    print('Singleton1 name: ' + my_singleton1.get_name())
    my_singleton1.set_name('New Singleton')
    print('Singleton2 name: ' + my_singleton2.get_name())
    assert my_singleton1 == my_singleton2
    assert id(my_singleton1) == id(my_singleton2)

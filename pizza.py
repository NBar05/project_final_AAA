import pytest
from typing import List, Dict, Set, Union


class Pizza:
    """
    Базовый класс для реализации разных видов пицц

    Args for init:
    - recipe: лист ингредиентов для пиццы
    - emoji: значок, обозначающий пиццу (обычно эмодзи, но может быть любая строка)
    - size: размер пиццы, возможны два варианта L и XL

    """
    def __init__(self, recipe: List[str], emoji: str, size: str = 'L') -> None:
        if size not in ['L', 'XL']:
            raise Exception('Wrong size, you can choose from only two options: L or XL')

        self.size = size

        self.recipe = recipe
        self.emoji = emoji

    def dict(self) -> Dict[str, str]:
        """Возвращение имени класса со значком в качестве ключа и рецептом в качестве значения"""
        return {f'{self.__class__.__name__} {self.emoji}': ' '.join(self.recipe)}

    def __eq__(self, other: object) -> Union[Set, bool]:
        """
        Сравнение двух пицц

        Args:
        - other: другой класс пиццы

        Return:
        - нет; печатается различие в рецептах + недостающие ингредиенты для получения первой пиццы

        """
        if not isinstance(other, Pizza):
            return NotImplemented

        print('Products in common:', set(self.recipe).intersection(set(other.recipe)))
        print(f'What else need for {self.__class__.__name__}:', set(self.recipe).difference(set(other.recipe)))

        return set(self.recipe).intersection(set(other.recipe))


class Margherita(Pizza):
    """Маргарита"""
    def __init__(self, size: str = 'L') -> None:
        super().__init__(['tomato sauce', 'mozzarella', 'tomatoes'], '🧀', size)


class Pepperoni(Pizza):
    """Пеперони"""
    def __init__(self, size: str = 'L') -> None:
        super().__init__(['tomato sauce', 'mozzarella', 'pepperoni'], '🍕', size)


class Hawaiian(Pizza):
    """Гавайская"""
    def __init__(self, size: str = 'L') -> None:
        super().__init__(['tomato sauce', 'mozzarella', 'chicken', 'pineapples'], '🍍', size)


def test_1_Pizza():
    pizza = Pizza(['mozzarella', 'chicken'], 'emoji', 'L')
    assert pizza.dict() == {'Pizza emoji': 'mozzarella chicken'}


def test_2_Margherita():
    pizza_m = Margherita()
    assert pizza_m.dict() == {'Margherita 🧀': 'tomato sauce mozzarella tomatoes'}


def test_3_Pepperoni():
    pizza_p = Pepperoni('L')
    assert pizza_p.dict() == {'Pepperoni 🍕': 'tomato sauce mozzarella pepperoni'}


def test_4_Hawaiian():
    pizza_h = Hawaiian('XL')
    assert pizza_h.dict() == {'Hawaiian 🍍': 'tomato sauce mozzarella chicken pineapples'}


def test_5_size_exception():
    with pytest.raises(Exception) as exc_info:
        _ = Hawaiian('XXL')

    assert str(exc_info.value) == 'Wrong size, you can choose from only two options: L or XL'


def test_6_eq_operator():
    pizza_p = Pepperoni('L')
    pizza_h = Hawaiian('XL')

    assert (pizza_p == pizza_h) == {'mozzarella', 'tomato sauce'}


def test_7_eq_operator():
    pizza_p = Pepperoni('L')
    pizza_h = 'Hawaiian'

    assert (pizza_p == pizza_h) is False


if __name__ == '__main__':
    print(Margherita().dict())
    print(Pepperoni('L').dict())
    print(Hawaiian('XL').dict())

import pytest
import random
from typing import Callable
from functools import partial

import click
from pizza import *


def log(text: str = '{}') -> Callable:
    """
    Вызов декоратора с определённым текстом

    Args:
    - text: предполагаемое сообщение со скобками для заполнения временем выполнения

    Return:
    - декоратор

    """
    def command_decorator(func: Callable) -> Callable:

        def log_with_text(*args, **kwargs) -> None:
            func(*args, **{k: v for k, v in kwargs.items() if k != 'text'})
            print(text.format(random.randint(1, 10)))

        return partial(log_with_text, text=text)

    return command_decorator


@log('👨‍🍳 Приготовили за {}с!')
def _bake(pizza) -> None:
    """Готовит пиццу"""


@log('🛵 Доставили за {}с!')
def _delivery(pizza) -> None:
    """Доставляет пиццу"""


@log('🏠 Забрали за {}с!')
def _pickup(pizza) -> None:
    """Самовывоз"""


@click.group()
def cli():
    pass


def order_base(pizza: str, size: str, delivery: bool) -> None:
    """Готовит и доставляет пиццу"""
    # перебираем имеющиеся виды пицц
    # при наличии останавливаем цикл и ошибка не выводится
    for pizza_cls in Pizza.__subclasses__():
        if pizza_cls.__name__.lower() == pizza.lower():
            break
    else:
        raise Exception('No such pizza in menu')

    pizza = pizza_cls(size)

    _bake(pizza)
    if delivery:
        _delivery(pizza)
    else:
        _pickup(pizza)


@cli.command()
@click.option('--delivery', default=False, is_flag=True)
@click.option('--size', default='L', show_default=True)
@click.argument('pizza', nargs=1)
def order(pizza: str, size: str, delivery: bool) -> None:
    """Готовит и доставляет пиццу"""
    order_base(pizza=pizza, size=size, delivery=delivery)


def menu_base() -> None:
    """Выводит меню"""
    for pizza_cls in Pizza.__subclasses__():
        print('-', pizza_cls().dict())


@cli.command()
def menu() -> None:
    """Выводит меню"""
    menu_base()


def test_menu(capfd):
    menu_base()

    out, err = capfd.readouterr()
    out = out.strip().split('\n')

    assert out == [
        "- {'Margherita 🧀': 'tomato sauce mozzarella tomatoes'}",
        "- {'Pepperoni 🍕': 'tomato sauce mozzarella pepperoni'}",
        "- {'Hawaiian 🍍': 'tomato sauce mozzarella chicken pineapples'}"
    ]


def test_bake(capfd):
    pizza = Margherita()

    _bake(pizza)

    out, err = capfd.readouterr()
    assert out[:18] == '👨‍🍳 Приготовили за'


def test_delivery(capfd):
    pizza = Pepperoni('L')

    _delivery(pizza)

    out, err = capfd.readouterr()
    assert out[:14] == '🛵 Доставили за'


def test_pickup(capfd):
    pizza = Hawaiian('XL')

    _pickup(pizza)

    out, err = capfd.readouterr()
    assert out[:12] == '🏠 Забрали за'


def test_order_base_with_delivery(capfd):
    order_base(pizza='Margherita', size='L', delivery=True)

    out, err = capfd.readouterr()

    first_print, second_print = out.strip().split('\n')
    assert [first_print[:18], second_print[:14]] == ['👨‍🍳 Приготовили за', '🛵 Доставили за']


def test_order_base_no_delivery(capfd):
    order_base(pizza='Pepperoni', size='XL', delivery=False)

    out, err = capfd.readouterr()

    first_print, second_print = out.strip().split('\n')
    assert [first_print[:18], second_print[:12]] == ['👨‍🍳 Приготовили за', '🏠 Забрали за']


def test_order_base_name_exception():
    with pytest.raises(Exception) as exc_info:
        order_base(pizza='Peroni', size='XL', delivery=False)

    assert str(exc_info.value) == 'No such pizza in menu'


def test_order_base_size_exception():
    with pytest.raises(Exception) as exc_info:
        order_base(pizza='Pepperoni', size='XXXXL', delivery=False)

    assert str(exc_info.value) == 'Wrong size, you can choose from only two options: L or XL'


if __name__ == '__main__':
    cli()

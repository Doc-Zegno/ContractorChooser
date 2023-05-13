from typing import Callable

import collection_utils as cu

from supplier import Supplier
from product import Product
from period import Period
from supply import Supply
from pair import Pair


def _sum_supplies(supplier: Supplier, products: list[Product], period: Period) -> Supply:
    aggregated_quantities = {}
    for product in products:
        aggregated_quantity = Pair()
        cu.extend(supplier.supplies, until_length=period.length, with_value=Supply)
        for month_index in range(period.length):
            supply = supplier.supplies[month_index]
            quantity = cu.get_or_put(supply.quantities, key=product.name, default=Pair)
            aggregated_quantity.expected += quantity.expected
            aggregated_quantity.actual += quantity.actual
        aggregated_quantities[product.name] = aggregated_quantity
    return Supply(aggregated_quantities)


def _calculate_criterion1(supplier: Supplier, products: list[Product], period: Period) -> float:
    aggregated_supply = _sum_supplies(supplier, products, period)  # product.name -> Q(exp), Q(act)
    denominator = 0.0
    nominator = 0.0
    for product in products:
        price = cu.get_or_put(supplier.prices, key=product.name, default=Pair)
        quantity = aggregated_supply.quantities[product.name]
        denominator += price.actual * quantity.expected
        nominator += price.actual * quantity.actual
    return abs(1 - nominator / denominator)


def _calculate_criterion2(supplier: Supplier, products: list[Product], period: Period) -> float:
    aggregated_supply = _sum_supplies(supplier, products, period)  # product.name -> Q(exp), Q(act)
    denominator = 0.0
    nominator = 0.0
    for product in products:
        price = cu.get_or_put(supplier.prices, key=product.name, default=Pair)
        quantity = aggregated_supply.quantities[product.name]
        denominator += price.expected * quantity.actual
        nominator += price.actual * quantity.actual
    return nominator / denominator


def _calculate_criterion3(supplier: Supplier, products: list[Product], period: Period) -> float:
    cu.extend(supplier.supplies, until_length=period.length, with_value=Supply)
    denominator = 0.0
    nominator = 0.0
    for product in products:
        for month_index in range(period.length):
            supply = supplier.supplies[month_index]
            quantity = cu.get_or_put(supply.quantities, key=product.name, default=Pair)
            nominator += abs(quantity.actual - quantity.expected)
            denominator += quantity.expected
    return nominator / denominator


def _calculate_criterion4(supplier: Supplier, products: list[Product], period: Period) -> float:
    cu.extend(supplier.supplies, until_length=period.length, with_value=Supply)
    result = 0.0
    for product in products:
        for month_index in range(period.length):
            supply = supplier.supplies[month_index]
            quantity = cu.get_or_put(supply.quantities, key=product.name, default=Pair)
            result += abs(1.0 - quantity.actual / quantity.expected)
    return result


_EVALUATORS: dict[str, Callable[[Supplier, list[Product], Period], float]] = {
    "Объем": _calculate_criterion1,
    "Цена": _calculate_criterion2,
    "Ассортимент": _calculate_criterion3,
    "Ритмичность": _calculate_criterion4,
}


# Criterion.name -> score
def evaluate(supplier: Supplier, products: list[Product], period: Period) -> dict[str, float]:
    return {criterion_name: evaluator(supplier, products, period) for criterion_name, evaluator in _EVALUATORS.items()}

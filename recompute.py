#!/usr/bin/env python3
"""Recompute every plate cost, basket and index value of plate_cost_index.csv from the other two files.

Usage: python3 recompute.py   (run in this folder; standard library only; exit 1 on any difference)
"""
import csv
import sys

TOL_CENTS, TOL_INDEX = 0.006, 0.06


def rows(name):
    with open(name, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


prices = {}
for r in rows("ingredient_prices.csv"):
    prices.setdefault(r["ingredient"], {})[r["month"]] = float(r["unit_price_usd"])
recipes = {}
for r in rows("dish_recipes.csv"):
    recipes.setdefault(r["dish"], []).append((r["ingredient"], float(r["amount"]), r["unit"]))


def plate_cost(dish, month):
    total = 0.0
    for ingredient, amount, unit in recipes[dish]:
        price = prices.get(ingredient, {}).get(month)
        if price is None:
            return None  # BLS published no price that month; the index leaves the cell empty
        total += amount / 16 * price if unit == "oz" else amount * price
    return total


index_rows = rows("plate_cost_index.csv")
base = next(float(r["basket_usd"]) for r in index_rows if r["basket_usd"])
problems = []
for r in index_rows:
    costs = {d: plate_cost(d, r["month"]) for d in recipes}
    for d, c in costs.items():
        want = r.get(d, "")
        if (c is None) != (want == "") or (c is not None and abs(c - float(want)) > TOL_CENTS):
            problems.append(f"{r['month']} {d}: {c} vs {want!r}")
    if r["basket_usd"] and None not in costs.values():
        basket = sum(costs.values())
        if abs(basket - float(r["basket_usd"])) > TOL_CENTS * len(costs):
            problems.append(f"{r['month']} basket: {basket:.2f} vs {r['basket_usd']}")
        if abs(basket / base * 100 - float(r["index"])) > TOL_INDEX:
            problems.append(f"{r['month']} index: {basket / base * 100:.1f} vs {r['index']}")

print("\n".join(problems) or f"PASS: {len(index_rows)} months, {len(recipes)} plates recomputed")
sys.exit(1 if problems else 0)

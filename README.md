# Plate Cost Index

The ingredient cost of 12 fixed U.S. diner plates, month by month from January 2023 to
October 2026, at average U.S. retail prices from the Bureau of Labor Statistics (BLS), and an index of
the whole basket (May 2023 = 100). Published by Bardach Technologies LLC; the same numbers, with
charts, are on https://tools.bardach-technologies.com/data/plate-cost-index?utm_source=github&utm_medium=dataset&utm_campaign=b29-open-data.

## Files

- `plate_cost_index.csv`: one row per month: `index`, `basket_usd` (all 12 plates) and the cost of each plate in USD. Empty
  cells are months in which BLS published no price for one of the plate's ingredients; they are never filled in.
- `ingredient_prices.csv`: every price used: the BLS series id, the BLS value as published (`bls_value_usd`), the divisor to a
  per-unit price (`per`: lb, egg or fl oz) and a link to the BLS series.
- `dish_recipes.csv`: what goes on each plate: ingredient, amount and unit (oz, eggs or fl oz).
- `recompute.py`: rebuilds the index from the two files above (see below).

## Method

Plate cost in a month = the sum over its recipe lines of amount / 16 x price per lb (oz lines), amount x price per egg,
or amount x price per fl oz. The basket is the sum of the 12 plates; the index is the basket divided by the basket of
the base month, times 100. Every value in `plate_cost_index.csv` can be recomputed from the other two files.

## Limits

Retail store prices, not what a restaurant pays a distributor, and the dollar amounts are not any restaurant's plate
cost; the index shows the direction of retail ingredient prices. The plates hold main ingredients only (no oil,
seasoning, sauces, labor or rent), and the recipes are ours, written to stay fixed. Ingredients covered: bacon, beans, beef for stew, bread, butter, cheddar cheese, chicken breast, chicken legs, eggs, flour, ground beef, ham, lettuce, milk, pork chops, potatoes, rice, spaghetti and macaroni, steak, tomatoes.

## Source and licence

Prices: U.S. Bureau of Labor Statistics, CPI Average Price Data, U.S. city average (public domain). BLS does not endorse
this index. Index, recipes and this card: CC BY 4.0. Suggested credit: Plate Cost Index, Bardach Technologies LLC, from BLS
Average Price Data, https://tools.bardach-technologies.com/data/plate-cost-index.

Built 2026-11-12, basket version 2026-11.

## How to cite

> Plate Cost Index, Bardach Technologies LLC, from BLS Average Price Data. https://github.com/bardachtech/plate-cost-index

A Zenodo DOI is pending; this section will carry it once it exists.

## Mirrors and charts

- Hugging Face: https://huggingface.co/datasets/bardachtech/plate-cost-index
- Charts and the same numbers: https://tools.bardach-technologies.com/data/plate-cost-index?utm_source=github&utm_medium=dataset&utm_campaign=b29-open-data

## Recompute every number

Run `python3 recompute.py` in this folder (standard library only). It rebuilds every plate cost, basket and index value
from `ingredient_prices.csv` and `dish_recipes.csv` and exits 1 on any difference beyond rounding.

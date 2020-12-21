from functools import reduce
from collections import defaultdict
from pathlib import Path


def parse_ingredients(line):
    ingredients = line.split('(')[0].split()
    allergens = line.split('contains ')[1].replace(')', '').replace(',', '').split()
    return set(ingredients), allergens


def create_ingredients_indexes(ingr_with_all):
    ingr_indexes = defaultdict(list)
    for idx, (_, allergens) in enumerate(ingr_with_all):
        for allergen in allergens:
            ingr_indexes[allergen].append(idx)
    return ingr_indexes


def create_common_ingr_by_all(ingr_with_all):
    ingr_indexes = create_ingredients_indexes(ingr_with_all)

    result = []
    for allergen, idxs in ingr_indexes.items():
        intrs = reduce(set.intersection, (ingr_with_all[idx][0] for idx in idxs))
        result.append((allergen, intrs))

    return result


def create_allergens_dict(ingr_with_all):
    common_ingredients = create_common_ingr_by_all(ingr_with_all)
    allergen_dict = {}
    len_allergen_dict = -1

    while len(allergen_dict) > len_allergen_dict:
        len_allergen_dict = len(allergen_dict)
        for allergen, ingredients in common_ingredients:
            diff = ingredients - set(allergen_dict.keys())
            if len(diff) == 1:
                ingr = next(iter(diff))
                allergen_dict[ingr] = allergen

    return allergen_dict


def count_not_allergen(ingr_with_all, allergens_dict):
    return sum(
        sum(1 for ingr in ingredients if ingr not in allergens_dict)
        for ingredients, _ in ingr_with_all
    )


def get_canonical_dangerous_ingr(allergens_dict):
    return ','.join(ingr for ingr, allergen in sorted(allergens_dict.items(), key=lambda t: t[1]))


lines = Path('input.txt').read_text().splitlines()

ingr_with_all = list(map(parse_ingredients, lines))
allergens_dict = create_allergens_dict(ingr_with_all)

result_part1 = count_not_allergen(ingr_with_all, allergens_dict)
result_part2 = get_canonical_dangerous_ingr(allergens_dict)

print(result_part1)
print(result_part2)

assert result_part1 == 1882
assert result_part2 == 'xgtj,ztdctgq,bdnrnx,cdvjp,jdggtft,mdbq,rmd,lgllb'

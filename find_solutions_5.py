"""Copied from find_solutions_4k1 and slightly tweaked to just consider
powers of 5
"""

from collections import Counter, defaultdict
from math import prod

from utils import generate_primes, sum_2_squ_from_primes, sym_points


def fill_examples(k: int, circle_points, examples):
    """Fill your boots!! Or in this case the results dictionary"""

    primes = [5] * k
    r2 = prod(primes)  #  the radius^2

    for m in generate_primes():
        # is the lattice modulus

        # tweak the break as needed, lower for quicker search, higher for more results
        if m > 3:
            break

        con_class = [(x % m, y % m) for x, y in circle_points]
        summary = Counter(con_class)

        for cc, cnt in summary.items():

            centre = (-cc[0] % m, -cc[1] % m)
            points = tuple(
                [
                    (x + centre[0], y + centre[1])
                    for x, y in circle_points
                    if x % m == cc[0] and y % m == cc[1]
                ]
            )
            example = (k, m, r2, centre, points)
            examples[cnt].add(example)


def print_examples(examples):
    """Output the results in console"""
    show_missing = True
    for n in range(1, max(examples.keys())):
        if n in examples:
            print()
            print(f"N = {n}")
            for ex in examples[n]:
                print(f"k={ex[0]}")
                print(f"radius={5 ** ex[0]}")
                print(f"centre={str(ex[3]):10}")
                print(f"lattice mod={ex[1]}")
                print(f"points={ex[4]}")

        else:
            if n > 1 and show_missing:
                print()
                print("------------------------------")
                print(f"Missing {n}")
                print("------------------------------")
                show_missing = False


def print_examples_2(examples):
    """Output the results in console - only solutions where radius^2 = n-1"""
    show_missing = True
    for n in range(1, max(examples.keys())):
        if n in examples:
            print()
            print(f"N={n} radius^2=5^{n-1}={5 ** (n-1)}")
            for ex in examples[n]:
                if ex[0] == n - 1:
                    print(
                        f"lattice mod={ex[1]}     centre={str(ex[3]):10} points={ex[4]}"
                    )

        else:
            if n > 1:
                break


def search(upto=6):
    """Find solutions for powers of 5
    Populate examples which is a dictionary keyed on (N) where each entry has
    a set of example solutions
    """
    examples = defaultdict(set)

    for k in range(1, upto + 1):
        primes = [5] * k
        sols = sum_2_squ_from_primes(primes)
        circle_points = set()
        for sol in sols:
            circle_points.update({x for x in sym_points(sol)})

        fill_examples(k, circle_points, examples)

    print_examples_2(examples)


search()

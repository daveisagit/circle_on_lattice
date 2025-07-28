"""Basic idea is to create larger and larger circle with more integer points
For each look at all prime lattice sizes and all integer offsets of them to
see how many lattice points are touched.
"""

from collections import Counter, defaultdict
from math import prod

from utils import all_primes_up_to, generate_primes, sum_2_squ_from_primes, sym_points


def fill_examples(primes, circle_points, examples):
    """Fill your boots!! Or in this case the results dictionary"""

    r2 = prod(primes)  #  the radius^2

    for m in generate_primes():
        # is the lattice modulus

        # tweak the break as needed, lower for quicker search, higher for more results
        if m > 100:
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
            example = (tuple(primes), m, r2, centre, points)
            examples[cnt].add(example)


def print_examples(examples):
    """Output the results in console"""
    show_missing = True
    for n in range(1, max(examples.keys())):
        if n in examples:
            print()
            print(f"N = {n}")
            for ex in examples[n]:
                print(f"primes={ex[0]}")
                print(f"radius={ex[2]:}")
                print(f"centre={str(ex[3]):10}")
                print(f"lattice mod={ex[1]}")
                print(f"points={ex[4]}")
                break  # remove if you more/all the examples found

        else:
            if show_missing:
                print()
                print("------------------------------")
                print(f"Missing {n}")
                print("------------------------------")
                show_missing = False
            # break  # remove to see rest for higher n


def search(prime_count_from=1, prime_count_to=5):
    """Find solutions on a range of amount prime numbers of the form 4k+1
    1.  5
    2.  13
    3.  17
    4.  29 etc.

    Populate examples which is a dictionary keyed on (N) where each entry has
    a set of example solutions
    """
    examples = defaultdict(set)

    # Optional code for loading previously found results

    # try:
    #     with open("examples.pkl", "rb") as f:
    #         examples = pickle.load(f)
    # except:
    #     examples = {}

    pl = all_primes_up_to(1000)  # 1000 is arbitrary

    pl = [p for p in pl if p % 4 == 1]
    for k in range(prime_count_from, prime_count_to + 1):
        primes = pl[:k]
        sols = sum_2_squ_from_primes(primes)
        circle_points = set()
        for sol in sols:
            circle_points.update({x for x in sym_points(sol)})

        fill_examples(primes, circle_points, examples)

    # Optional code for saving results

    # # examples = sorted(examples.items(), key=lambda x: x[0])
    # with open("examples.pkl", "wb") as f:
    #     pickle.dump(examples, f)
    # print("Done")

    print_examples(examples)


search()

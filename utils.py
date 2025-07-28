from math import ceil, isqrt, sqrt


def generate_primes():
    """Generate an infinite sequence of prime numbers."""
    # Maps composites to primes witnessing their compositeness.
    # This is memory efficient, as the sieve is not "run forward"
    # indefinitely, but only as long as required by the current
    # number being tested.
    #
    D = {}

    # The running integer that's checked for primeness
    q = 2

    while True:
        if q not in D:
            # q is a new prime.
            # Yield it and mark its first multiple that isn't
            # already marked in previous iterations
            #
            yield q
            D[q * q] = [q]
        else:
            # q is composite. D[q] is the list of primes that
            # divide it. Since we've reached q, we no longer
            # need it in the map, but we'll mark the next
            # multiples of its witnesses to prepare for larger
            # numbers
            #
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]

        q += 1


def all_primes_up_to(n):
    """Return all the primes <= n as a list"""
    l = []
    for p in generate_primes():
        if p > n:
            break
        l.append(p)
    return l


def is_perfect_square(n: int) -> bool:
    """Return True is n is a perfect square"""
    return isqrt(n) ** 2 == n


def sym_points(p):
    """Given x,y generate the 8 symmetric points on the circle
    (±x , ±y) and (±y , ±x)
    """
    x, y = p
    yield x, y
    yield -x, y
    yield -x, -y
    yield x, -y
    y, x = p
    yield x, y
    yield -x, y
    yield -x, -y
    yield x, -y


def sum_two_squares_solutions(n: int) -> set:
    """Return a list of positive solutions p,q to p^2 + q^2 = n
    Such that p<q, so no repeat i.e. q,p"""
    sols = set()
    for p in range(0, ceil(sqrt(n / 2))):
        q2 = n - p * p
        if is_perfect_square(q2):
            sols.add((p, isqrt(q2)))
    return sols


def sum_2_squ_combine(sols_for_N, P):
    """Given a complete set of solutions to x^2+y^2=N
    where 0 <= x < y
    Return all the solutions to x^2+y^2=N x P
    Where P is a prime = 1 mod 4
    """
    p, q = P
    new_sols = set()
    for a, b in sols_for_N:
        x = a * p + b * q
        y = abs(a * q - b * p)
        t = (x, y)
        t = tuple(sorted(t))
        new_sols.add(t)
        x = b * p + a * q
        y = abs(b * q - a * p)
        t = (x, y)
        t = tuple(sorted(t))
        new_sols.add(t)
    return new_sols


def sum_2_squ_from_primes(primes):
    """Return a set of solutions x^2 + y^2 = p1.p2.p3. ..
    Where primes are all 4k+1
    0 <= x < y
    """
    primes = [p for p in primes]
    sols = sum_two_squares_solutions(primes[0])
    for p in primes[1:]:
        pq = list(sum_two_squares_solutions(p))
        assert len(pq) == 1
        sols = sum_2_squ_combine(sols, pq[0])
    return set(sols)

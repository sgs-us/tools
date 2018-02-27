import os

from argparse import ArgumentParser

import matplotlib.pylab as plt
import numpy as np
from numpy.polynomial.legendre import leggauss

from initialize_matplotlib import initialize_plotting_style, load_color, savefig,\
    load_marker, insert_legend


def phi(x, points):
    """
    Evaluates the remainder polynomial (polynomial interpolation)
    @param x: evaluation point
    @param points: point set
    """
    return np.prod(np.abs(x - points))


if __name__ == "__main__":
    parser = ArgumentParser(description='Get a program and run it with input', version='%(prog)s 1.0')
    parser.add_argument('--n', default=10, type=int, help="number for L2-Leja points")
    parser.add_argument('--out', default=False, action='store_true', help='save plots to file')
    args = parser.parse_args()

    initialize_plotting_style(macros="commands.tex")

    xs = np.linspace(-1, 1, 1000)

    for ni in xrange(1, args.n + 1):
        points, _ = leggauss(ni)
        print "plot Gauss points: %i/%i" % (ni, args.n)

        fig = plt.figure()
        plt.plot(xs, [phi(xi, points) for xi in xs],
                 color=load_color(np.random.randint(0, 10)))
        plt.scatter(points, np.zeros(points.shape),
                    color=load_color(np.random.randint(0, 10)),
                    marker=load_marker(np.random.randint(0, 5)),
                    label=r"Gauss points $\{\rvi\}_{i=1}^{%i}$" % ni)

        plt.xlabel(r"$\rv$")
        plt.ylabel(r"$\Phi_{%i}(\rv) := \prod_{i=1}^{%i} |\rv - \rvi|$" % (ni, ni))

        lgd = insert_legend(loc="bottom", ncol=1, has_axis=True)

        if args.out:
            savefig(fig,
                    os.path.join("gauss_n%i" % ni),
                    lgd=lgd,
                    crop=True,
                    sizes=(8.25, 5))
            plt.close(fig)
        else:
            plt.show()

from wad18 import SCALE


def diagonal_eigenvalues(matrix):
    """
    Exact eigenvalue diagnostic for the diagonal metric used by this
    capsule's normative baseline.

    General dense eigensolvers are deliberately excluded from the
    normative WAD path because generic algebraic eigenvalues need not
    have finite WAD-18 representations.
    """

    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if i != j and value != 0:
                raise ValueError(
                    "normative eigenvalue path requires diagonal metric"
                )

    return [matrix[i][i] for i in range(len(matrix))]


def minimum_eigenvalue(matrix):
    return min(diagonal_eigenvalues(matrix))
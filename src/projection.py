def project_metric(metric, floor):
    projected = [row[:] for row in metric]

    for i in range(len(projected)):
        if projected[i][i] < floor:
            projected[i][i] = floor

    return projected


def projection_magnitude(raw, projected):
    total = 0

    for r, p in zip(raw, projected):
        for a, b in zip(r, p):
            total += abs(b - a)

    return total
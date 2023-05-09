from scipy.optimize import minimize

def pack_circles_square(n):
    initial_guess = np.random.uniform(size=2*n)

    def circle_constraint(coords, i, j):
        xi, yi = coords[i], coords[i+n]
        xj, yj = coords[j], coords[j+n]
        return (xi-xj)**2 + (yi-yj)**2 - 4.0 <= 0.0

    cons = []
    for i in range(n):
        cons.append({'type': 'ineq', 'fun': (lambda x, i=i, j=j: circle_constraint(x, i, j)), 'args':(i, j) for j in range(i+1, n)})
        cons.append({'type': 'ineq', 'fun': (lambda x, i=i: x[i] - r), 'args':(i,)})
        cons.append({'type': 'ineq', 'fun': (lambda x, i=i: x[i+n] - r), 'args':(i,)})
        cons.append({'type': 'ineq', 'fun': (lambda x, i=i: r - x[i]), 'args':(i,)})
        cons.append({'type': 'ineq', 'fun': (lambda x, i=i: r - x[i+n]), 'args':(i,)})

    def circle_packing(x):
        r = x[-1]
        return -r

    bounds = [(0.0, 1.0) for i in range(2*n)]
    bounds.append((0.0, 1.0))

    sol = minimize(circle_packing, initial_guess, method='SLSQP', bounds=bounds, constraints=cons)

    return sol.x

print(pack_circles_square(5))
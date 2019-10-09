import numpy
import random
import math
import matplotlib.pyplot as plt
from scipy.optimize import minimize

################
# Inputs #######
################

# init seed (debugging)
numpy.random.seed(100)

# 2 clusters of class A (+1)
classA = numpy.concatenate(
    (numpy.random.randn(10, 2) * 0.35 + [1.5, 0.5],
     numpy.random.randn(10, 2) * 0.35 + [-1.5, 0.5]))

# 1 cluster of class B (-1)
classB = numpy.random.randn(20, 2) * 0.35 + [0.0, -0.5]

# training set (data samples and labels)
inputs = numpy.concatenate((classA, classB))
targets = numpy.concatenate(
    (numpy.ones(classA.shape[0]),
     -numpy.ones(classB.shape[0])))
N = inputs.shape[0]

# shuffle training set
permute = list(range(N))
random.shuffle(permute)
inputs = inputs[permute]
targets = targets[permute]

# plot training set
plt.plot([p[0] for p in classA],
         [p[1] for p in classA],
         'b.')
plt.plot([p[0] for p in classB],
         [p[1] for p in classB],
         'r.')

# configure
plt.axis([-2, 2, -2, 2])
plt.title('training set 3')

# save and show plot
# plt.savefig('plots/training_set_3.jpg')
plt.show()


#####################
# SVM training ######
#####################

# functions (they use global variables defined below)
def linear_kernel(x, y):
    return numpy.dot(x, y)


def polynomial_kernel(x, y, p):
    return (numpy.dot(x, y) + 1) ** p


def radial_kernel(x, y, sigma):
    return math.exp(- numpy.linalg.norm(numpy.array(x) - y)**2 / (2 * sigma**2))


def objective(a):
    return 1/2 * numpy.dot(a, numpy.dot(P, a)) - numpy.sum(a)


def zerofun(a):
    return numpy.dot(a, targets)


def ind(y):
    return numpy.sum([x['alpha'] * x['target'] * K(y, x['point']) for x in support_vectors]) - b


# choose kernel
K = linear_kernel
# p = 2
# K = lambda x, y: polynomial_kernel(x, y, p)
# sigma = 1e0
# K = lambda x, y: radial_kernel(x, y, sigma)

# soft margins
C = None

# matrix to avoid computing the same quantities a lot of times
P = numpy.array([[targets[i] * targets[j] * K(inputs[i], inputs[j]) for j in range(N)] for i in range(N)])

# optimization (minimization of dual problem)
ret = minimize(objective, numpy.zeros(N), bounds=[(0, C) for x in range(N)], constraints={'type': 'eq', 'fun': zerofun})
if not ret['success']:
    print('No solution found by minimize()')
    print(ret['message'])
    exit(-1)
alpha = ret['x']

# extract non-zero alpha
support_vectors = [{'point': inputs[i], 'alpha': alpha[i], 'target': targets[i]}
                   for i in range(N) if abs(alpha[i]) > 1e-5]
if len(support_vectors) < 1:
    print('No support vectors')
    exit(-1)

# compute b
s = support_vectors[0]
b = numpy.sum([x['alpha'] * x['target'] * K(s['point'], x['point']) for x in support_vectors]) - s['target']


####################
# Analysis #########
####################

# plot training set
plt.plot([p[0] for p in classA],
         [p[1] for p in classA],
         'b.')
plt.plot([p[0] for p in classB],
         [p[1] for p in classB],
         'r.')

# plot support vectors
plt.plot([x['point'][0] for x in support_vectors],
         [x['point'][1] for x in support_vectors],
         'yo')

# plot decision boundary and margin
xgrid = numpy.linspace(-5, 5)
ygrid = numpy.linspace(-5, 5)
grid = numpy.array([[ind([x, y]) for x in xgrid] for y in ygrid])
plt.contour(xgrid, ygrid, grid,
            (-1.0, 0.0, 1.0),
            colors=('red', 'black', 'blue'),
            linewidths=(1, 3, 1),
            linestyles=('dashed', 'solid', 'dashed'))

# configure
plt.axis([-2, 2, -2, 2])
plt.title('SVM with ' + K.__name__.replace('_', ' '))

# save and show plot
# plt.savefig('plots/linear_kernel_3.jpg')
plt.show()

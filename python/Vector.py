import operator
import math
from decimal import Decimal, getcontext

getcontext().prec = 5

class Vector(object):
 
    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(coordinates)
        except ValueError:
            raise ValueError('The coorinates must be non-empty')
        except TypeError:
            raise TypeError('The coorinates must be an iterable')
    
    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordiantes == v.coordinates

    def __add__(self, v):
        # method 1
        return tuple(map(operator.add, self.coordinates, v.coordinates))

    def plus(self, v):
        # method 2
        #new_coordinates = [x + y for x, y in zip(self.coordinates, v.coordinates)]
        # method 3
        new_coordinates = []
        n = len(self.coordinates)
        for i in range(n):
            new_coordinates.append(self.coordinates[i] + v.coordinates[i])
        return Vector(new_coordinates)

    def __sub__(self, v):
        # method 1
        return tuple(map(operator.sub, self.coordinates, v.coordinates))

    def minus(self, v):
        # method 2
        #new_coordinates = [x - y for x, y in zip(self.coordinates, v.coordinates)]
        # method 3
        new_coordinates = []
        n = len(self.coordinates)
        for i in range(n):
            new_coordinates.append(self.coordinates[i] - v.coordinates[i])
        return Vector(new_coordinates)

    def __mul__(self, s):
        #method 1
        return tuple(x*s for x in self.coordinates)

    def times_scalar(self, s):
        # method 2
        new_coordinates = [Decimal(s) * x for x in self.coordinates]
        return Vector(new_coordinates)

    def calcMagnitude(self):
        # method 1
        # mag = 0
        #for x in self.coordinates:
        #    mag += x ** 2
        #return math.sqrt(mag)
        #method 2
        coordinates_squared = [ x**2 for x in self.coordinates]
        return math.sqrt(sum(coordinates_squared))

    def normalizeVector(self):
        try:
            mag = self.calcMagnitude()
            return self.times_scalar( Decimal('1.0') / Decimal(mag))
        except ZeroDivisionError:
            raise Exception(CANNOT_NORMALIZE_ZERO_VECTOR_MSG)

    def innerProduct(self, v):
        coordinates_prod = [x * y for x, y in zip(self.coordinates, v.coordinates)]
        return sum(coordinates_prod)

    def thetaRadian(self, v):
        try:
            selfNorm = self.normalizeVector()
            vNorm = v.normalizeVector()
            return math.acos(selfNorm.innerProduct(vNorm))
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_THE_ZERO_VECTOR_MSG:
                raise Exception('Cannot compute an angle with the zero vector')
            else:
                raise e

    def thetaDegree(self, v):
        try:
            return math.degrees(self.thetaRadian(v))
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_THE_ZERO_VECTOR_MSG:
                raise Exception('Cannot compute an angle with the zero vector')
            else:
                raise e

    def isZeroVector(self):
        n = len(self.coordinates)
        for i in range(n):
            if self.coordinates[i] != Decimal(0):
                return False
        return True

    def isParallel(self, v):
        if self.isZeroVector() or v.isZeroVector():
            return True
        div_coordinates = []
        n = len(self.coordinates)
       
        for i in range(n):
            if v.coordinates[i] != Decimal(0):
                div_coordinates.append(self.coordinates[i] / v.coordinates[i])
            else:
                return False

        rate = div_coordinates[0]
        for i in range(n):
            if div_coordinates[i] != rate:
                return False
        return True

    def isOrthogonal(self, v):
        if self.isZeroVector() or v.isZeroVector():
            return True

        if self.innerProduct(v) == Decimal(0):
            return True
        else:
            return False       

    def projection(self, v):
        try:
            norm = v.normalizeVector()
            s = self.innerProduct(norm)
            return norm.times_scalar(s)
        except Exception as e:
            raise e 

    def orthogonal(self, v):
        try:
            return self - self.projection(v)

        except Exception as e:
            raise e

    def crossProduct(self, v):
        cp_vector = []
        cp_vector.append(self.coordinates[1] * v.coordinates[2] - \
                   self.coordinates[2] * v.coordinates[1])
        cp_vector.append(-(self.coordinates[0] * v.coordinates[2] - \
                   self.coordinates[2] * v.coordinates[0]))
        cp_vector.append(self.coordinates[0] * v.coordinates[1] - \
                   self.coordinates[1] * v.coordinates[0])
        return cp_vector

    def areaOfParallelogram(self, v):
        cpv = Vector(self.crossProduct(v))
        return cpv.calcMagnitude()

    def areaOfTriangle(self, v):
        return (self.areaOfParallelogram(v) / 2)

vector_add1 = Vector([8.218, -9.341])
vector_add2 = Vector([-1.129, 2.111])

print ' '.join(format(f, '.3f') for f in (vector_add1 + vector_add2))
print vector_add1.plus(vector_add2)

vector_sub1 = Vector([7.119, 8.215])
vector_sub2 = Vector([-8.223, 0.878])
print vector_sub1.minus(vector_sub2)

print ' '.join(format(f, '.3f') for f in (vector_sub1 - vector_sub2))

vector_mul = Vector([1.671, -1.012, -0.318])

#print ' '.join(format(f, '.3f') for f in (vector_mul * 7.41))
print vector_mul.times_scalar(7.41)

vector_mag1 = Vector([-0.221, 7.437])
vector_mag2 = Vector([8.813, -1.331, -6.247])

print vector_mag1.calcMagnitude()
print vector_mag2.calcMagnitude()

vector_norm1 = Vector([5.581, -2.136])
vector_norm2 = Vector([1.996, 3.108, -4.554])

print vector_norm1.normalizeVector()
print vector_norm2.normalizeVector()

vector_inner1 = Vector([7.887, 4.138])
vector_inner2 = Vector([-8.802, 6.776])
vector_inner3 = Vector([-5.955, -4.904, -1.874])
vector_inner4 = Vector([-4.496, -8.755, 7.103])

print vector_inner1.innerProduct(vector_inner2)
print vector_inner3.innerProduct(vector_inner4)

vector_angle1 = Vector([3.183, -7.627])
vector_angle2 = Vector([-2.668, 5.319])
vector_angle3 = Vector([7.35, 0.221, 5.188])
vector_angle4 = Vector([2.751, 8.259, 3.985])

print vector_angle1.thetaRadian(vector_angle2)
print vector_angle3.thetaDegree(vector_angle4)

vector_v1 = Vector([-7.579, -7.88])
vector_v2 = Vector([-2.029, 9.97, 4.172])
vector_v3 = Vector([-2.328, -7.284, -1.214])
vector_v4 = Vector([2.118, 4.827])

vector_w1 = Vector([22.737, 23.64])
vector_w2 = Vector([-9.231, -6.639, -7.245])
vector_w3 = Vector([-1.821, 1.072, -2.94])
vector_w4 = Vector([0, 0])

print "isParallel"
print vector_v1.isParallel(vector_w1)
print vector_v2.isParallel(vector_w2)
print vector_v3.isParallel(vector_w3)
print vector_v4.isParallel(vector_w4)

print "isOrthogonal"
print vector_v1.isOrthogonal(vector_w1)
print vector_v2.isOrthogonal(vector_w2)
print vector_v3.isOrthogonal(vector_w3)
print vector_v4.isOrthogonal(vector_w4)

vector_v1 = Vector([3.039, 1.879])
vector_v2 = Vector([-9.88, -3.264, -8.159])
vector_v3 = Vector([3.009, -6.172, 3.692, -2.51])

vector_u1 = Vector([0.825, 2.036])
vector_u2 = Vector([-2.155, -9.353, -9.473])
vector_u3 = Vector([6.404, -9.144, 2.759, 8.718])

print "project1=",vector_v1.projection(vector_u1)
print "orthognal1=",vector_v2.orthogonal(vector_u2)

print "projecti2=",vector_v3.projection(vector_u3)
print "orthogonal2=",vector_v3.orthogonal(vector_u3)

vector_v1 = Vector([8.462, 7.893, -8.187])
vector_v2 = Vector([-8.987, -9.838, 5.031])
vector_v3 = Vector([1.5000, 9.547, 3.691])

vector_w1 = Vector([6.984, -5.975, 4.778])
vector_w2 = Vector([-4.268, -1.861, -8.866])
vector_w3 = Vector([-6.007, 0.124, 5.772])

print "crossProduct=",vector_v1.crossProduct(vector_w1)
print "AreaOfParallel=",vector_v2.areaOfParallelogram(vector_w2)
print "AreaOfTriangle=",vector_v3.areaOfTriangle(vector_w3)



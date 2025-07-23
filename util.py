import math

def scale(x1, x2, x3, y1, y2):
    return y1 + (y2-y1) * (x2-x1)/(x3-x1)

def scale_limit(x1, x2, x3, y1, y2):
    value = y1 + (y2-y1) * (x2-x1)/(x3-x1)
    if y1 < y2:
        if value < y1:
            return y1
        elif value > y2:
            return y2
        else:
            return value
    else:
        if value > y1:
            return y1
        elif value < y2:
            return y2
        else:
            return value

def vec_norm(vec):
    x, y = vec
    d = math.sqrt(x**2 + y**2)
    return (x/d, y/d)

def vec_sub(vec1, vec2):
    x1, y1 = vec1
    x2, y2 = vec2
    return (x1-x2, y1-y2)

def vec_add(vec1, vec2):
    x1, y1 = vec1
    x2, y2 = vec2
    return (x1+x2, y1+y2)

def vec_mult(scalar, vec):
    return (vec[0]*scalar, vec[1]*scalar)

def vec_mag(vec):
    x, y = vec
    return math.sqrt(x**2 + y**2)

if __name__ == "__main__":
    print(scale_limit(2.0, 3.0, 1.0, 10.0, 0.0))
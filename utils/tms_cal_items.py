def girth(length, width, height):
    """围长"""
    result = length + (width + height) * 2
    return result


def perimeter(length, width, height):
    """周长"""
    result = length + width + height
    return result


def two_sides_length(length, width):
    """两边长"""
    result = length + width
    return result


def volume(length, width, height):
    result = length * width * height
    return result


def density(weight, volume):
    return weight / volume * 1728



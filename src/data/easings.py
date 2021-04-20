# 'x' represents the absolute progress of the animation in the bounds of 0 (beginning of animation) and 1 (end of animation)

def in_out_cubic(x: float):
    if x < 0.5:
        return 4 * (x ** 3)

    return 1 - (((-2 * x + 2) ** 3) / 2)

def in_out_quad(x: float):
    if x < 0.5:
        return  2 * (x ** 2)
        
    return 1 - (((-2 * x + 2) ** 2) / 2)

functions = {
    'in_out_cubic': in_out_cubic,
    'in_out_quad': in_out_quad,
}
LOW = 1
MEDIUM = 3
HIGH = 7


def scale_to_weight(scale):
    if scale == 0:
        return LOW
    if scale == 1:
        return MEDIUM
    if scale == 2:
        return HIGH


def weight_to_scale(weight):
    if weight == LOW:
        return 0
    if weight == MEDIUM:
        return 1
    if weight == HIGH:
        return 2
VALUE0 = 1
VALUE1 = 5
VALUE2 = 11

VALUE0_TEXT = "low"
VALUE1_TEXT = "high"
VALUE2_TEXT = "crucial"


def scale_to_weight(scale):
    if scale == 0:
        return VALUE0
    if scale == 1:
        return VALUE1
    if scale == 2:
        return VALUE2


def weight_to_text(weight):
    if weight == VALUE0:
        return VALUE0_TEXT
    elif weight == VALUE1:
        return VALUE1_TEXT
    elif weight == VALUE2:
        return VALUE2_TEXT
    else:
        return str(weight)


def weight_to_scale(weight):
    if weight == VALUE0:
        return 0
    elif weight == VALUE1:
        return 1
    elif weight == VALUE2:
        return 2
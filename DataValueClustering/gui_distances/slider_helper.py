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


def maptoscale(metriclist):
    resultlist = []
    metriclist2 = metriclist.copy()
    l = len(metriclist)

    # order metriclist, >1/10 to max, >1/3 to min
    metriclist2.sort()
    for metric in metriclist:
        if metriclist2.index(metric) < l/10:
            resultlist.append(VALUE2)
        elif metriclist2.index(metric) < l/3:
            resultlist.append(VALUE1)
        else:
            resultlist.append(VALUE0)

    return resultlist


def calculate_default_scales(abstractvalues, charlist):
    metriclist = []
    l = len(abstractvalues)
    for chars in charlist:
        num = len(chars)
        n, total = char_occurences_in_wordlist(abstractvalues, chars)
        part = n/l
        av = total/l
        av_per_occ = total/n

        # TODO ???
        metric = part / av_per_occ / num

        metriclist.append(metric)
    scalelist = maptoscale(metriclist)

    return scalelist


def char_occurences_in_word(str, chars):
    res = 0
    for c in chars:
      res += str.count(c)
    return res > 0, res


def char_occurences_in_wordlist(words, chars):
    n = 0
    res = 0
    for w in words:
        t, k = char_occurences_in_word(w, chars)
        n += t
        res += k
    return n, res



if __name__ == "__main__":
    values = ["a", "b", "a.", "b.", "c01", "c2"]
    charlist = ["a", "b", "ab", "0", "012"]
    print(
        calculate_default_scales(values, charlist)
    )

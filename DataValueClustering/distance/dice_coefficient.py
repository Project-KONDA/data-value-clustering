'''Apply dice coefficient distance function.'''
def dice_coefficient_distance(seq1, seq2):
    if not len(seq1) or not len(seq2): return 0.0
    if len(seq1) == 1:
        seq1 = seq1 + u'.'
    if len(seq2) == 1:
        seq2 = seq2 + u'.'

    a_bigram_list = []
    for i in range(len(seq1) - 1):
        a_bigram_list.append(seq1[i:i + 2])
    b_bigram_list = []
    for i in range(len(seq2) - 1):
        b_bigram_list.append(seq2[i:i + 2])

    a_bigrams = set(a_bigram_list)
    b_bigrams = set(b_bigram_list)
    overlap = len(a_bigrams & b_bigrams)
    dice_coeff = overlap * 2.0 / (len(a_bigrams) + len(b_bigrams))
    return dice_coeff

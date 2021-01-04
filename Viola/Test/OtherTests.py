from scipy.spatial.distance import pdist, squareform

def test1(a,b):
    print(a)
    #print(b)

def test2(t1):
    t1("hello")

#test2(test1)
test2(lambda a : test1(a, "world"))

def dice_coefficient(a, b):
    """dice coefficient 2nt/(na + nb)."""
    a_bigrams = set(a)
    b_bigrams = set(b)
    overlap = len(a_bigrams & b_bigrams)
    return overlap * 2.0/(len(a_bigrams) + len(b_bigrams))

#a = "Viola"
#a_bigram_list=[]
#for i in range(len(a)-1):
  #a_bigram_list.append(a[i:i+2])
#print(a_bigram_list)

#test1("x")

p = pdist([["1", "0.5"],["2.5", "1.5"],["10", "0.85"]])
print(p)
print(squareform(p))
print(squareform(squareform(p)))
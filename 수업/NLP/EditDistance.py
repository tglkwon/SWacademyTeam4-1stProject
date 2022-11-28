# Edit Distance : Hamming Distance

sum([i != j for i,j in zip(list('안녕하세요'), list('아녕하세요'))])

# Leven distance
def lev_dist(s1, s2):
    if len(s2) == 0:
        return len(s1)

    if len(s1) == 0:
        return len(s1)

    if s1[0] == s2[0]:
        return lev_dist(s1[1:], s2[1:])

    return min(0.5 + lev_dist(s1[1:], s2), 0.5 + lev_dist(s1, s2[1:]), 1 + lev_dist(s1[1:], s2[1:]))

lev_dist('ㅁㅓㅊㅓㅇㅇㅣ', 'ㄷㅐㅌㅗㅇㄹㅕㅇ')
lev_dist('012345689ABC', '0123456789A')
lev_dist('안녕하세요', '아녕하세요')

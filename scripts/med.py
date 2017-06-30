# -*- coding: utf-8 -*-

def memoize(func):
    """
    
    :param func: 
    :return: 
    """
    memo = {}

    def helper(*args, **kwargs):
        x = str(args) + str(kwargs)

        if x not in memo:
            memo[x] = func(*args, **kwargs)
        return memo[x]

    return helper

@memoize
def med_main(string_one, string_two, sub = 1):
    """
    
    :param string_one: 
    :param string_two: 
    :param sub: 
    :return: 
    """
    m = len(string_one)
    n = len(string_two)
    if min(m, n) == 0:
        return max(m, n)
    else:
        subst = 0 if string_one[m-1] == string_two[n-1] else sub
        substr_one = string_one[:m-1]
        substr_two = string_two[:n-1]
        return min(med_main(substr_one, string_two[:n], sub) + 1,
                   med_main(string_one[:m], substr_two, sub) + 1,
                   med_main(substr_one, substr_two, sub) + subst)

@memoize
def med_dl_main(string_one, string_two, sub = 1):
    """
    
    :param string_one: 
    :param string_two: 
    :param sub: 
    :return: 
    """
    m = len(string_one)
    n = len(string_two)
    if min(m, n) == 0:
        return max(m, n)
    elif m > 1 and n > 1 and string_one[m-2] == string_two[n-1] and \
            string_one[m-1] == string_two[n-2]:
        subst = 0 if string_one[m - 1] == string_two[n - 1] else sub
        substr_one = string_one[:-1]
        substr_two = string_two[:-1]
        return min(med_dl_main(substr_one, string_two, sub) + 1,
                   med_dl_main(string_one, substr_two, sub) + 1,
                   med_dl_main(substr_one, substr_two, sub) + subst,
                   med_dl_main(substr_one[:-1], substr_two[:-1], sub) + 1)
    else:
        subst = 0 if string_one[m-1] == string_two[n-1] else 1
        substr_one = string_one[:m-1]
        substr_two = string_two[:n-1]
        return min(med_dl_main(substr_one, string_two[:n], sub) + 1,
                   med_dl_main(string_one[:m], substr_two, sub) + 1,
                   med_dl_main(substr_one, substr_two, sub) + subst)

if __name__ == '__main__':
    misspelling = "пступком"
    candidate = "поступком"
    print(med_dl_main(misspelling, candidate))
# File KMP.py
# import time

def kmpMatch(text, pattern):
    n = len(text)
    m = len(pattern)

    fail = computeFail(pattern)

    i = 0
    j = 0

    while (i < n):
        if (pattern[j] == text[i]):
            if (j == m - 1):
                return i - m + 1
            i += 1
            j += 1
        elif (j > 0):
            j = fail[j-1]
        else:
            i += 1
    return -1

def computeFail(pattern):
    fail = [0 for i in range(len(pattern))]
    
    m =  len(pattern)
    j = 0
    i = 1

    while (i < m):
        if (pattern[j] == pattern[i]):
            fail[i] = j + 1
            i += 1
            j += 1
        elif (j > 0):
            j = fail[j-1]
        else:
            fail[i] = 0
            i += 1
    return fail

# start_time = time.time()
# for i in range(1000):
#     computeFail("HELLOWORLD")
# print("\n--- %s seconds ---" % (time.time() - start_time))
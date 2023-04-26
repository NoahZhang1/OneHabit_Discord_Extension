def div_zero(n, d):
     return n / d if d else 0


def calculateprogress(response_list):


    res = {}

    for itemIdx, item in enumerate(response_list):
        user = item['username']
        progress = item['progress']

        if user in res:
            res[user] += progress
        else:
            res[user] = progress
    return res
 
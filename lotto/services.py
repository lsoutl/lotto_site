import random

def quick_pick():
    return sorted(random.sample(range(1, 46), 6))

def score(picks, winning):
    """
    picks: [int]*6  사용자 선택 번호
    winning: [int]*6  당첨 번호
    return: {"match_count": int, "rank": int}  # rank: 1~4, 0=꽝
    """
    m = len(set(picks) & set(winning))
    if m == 6:
        rank = 1
    elif m == 5:
        rank = 2
    elif m == 4:
        rank = 3
    elif m == 3:
        rank = 4
    else:
        rank = 0
    return {"match_count": m, "rank": rank}
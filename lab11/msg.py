def msg(move=None, next=False, point=False, cards=None, abandon=False):
    return {
        "move": move,
        "next": next,
        "point": point,
        "cards": cards,
        "abandon": abandon
    }

import itertools


def play_game(init_positions):
    positions = init_positions.copy()
    scores = [0] * len(positions)
    die = itertools.count()
    while True:
        for player_idx in range(len(positions)):
            to_add = sum(next(die) % 100 + 1 for _ in range(3))
            positions[player_idx] = (positions[player_idx] + to_add - 1) % 10 + 1
            scores[player_idx] += positions[player_idx]

            if scores[player_idx] >= 1000:
                return scores, next(die)


players = [3, 4]

scores, die = play_game(players)

assert min(scores) * die == 995904

def spend_time(player, time, amount):
    multiplier = 1.0
    if player.is_broken_leg:
        multiplier = 2.0
    time -= amount * multiplier
    return time

def time_left(time):
    minutes = round(time // 60)
    seconds = round(time % 60)
    result = f"{minutes}:{seconds:02d}"
    return result
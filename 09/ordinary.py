import time
from profile_decorator import profile_deco


class Window:
    pass


class Floor:
    pass


class Room:
    pass


class Door:
    pass


class Flat:

    def __init__(self, windows, floor, rooms, door):
        self.windows = windows
        self.floor = floor
        self.rooms = rooms
        self.door = door


@profile_deco
def run():
    times_of_run = 2_000_000

    all_windows = []
    all_floors = []
    all_rooms = []
    all_doors = []

    for _ in range(times_of_run):
        all_windows.append(Window())
        all_floors.append(Floor())
        all_rooms.append(Room())
        all_doors.append(Door())

    time_1 = time.time()

    flats = [Flat(all_windows[i], all_floors[i], all_rooms[i], all_doors[i])
             for i in range(times_of_run)
             ]

    time_2 = time.time()
    print(f"time of creating {times_of_run} objects "
          f"--- {time_2 - time_1} seconds ---")

    for i in range(times_of_run):
        if flats[i].floor is not None:
            pass

        if flats[i].windows is not None:
            pass

        if flats[i].rooms is not None:
            pass

        if flats[i].door is not None:
            pass

    time_3 = time.time()
    print(f"time of access to {times_of_run} objects "
          f"--- {time_3 - time_2} seconds ---")

    for i in range(times_of_run):
        flats[i].floor = all_floors[i - 1]
        flats[i].windows = all_windows[i - 1]
        flats[i].rooms = all_rooms[i - 1]
        flats[i].door = all_doors[i - 1]

    time_4 = time.time()
    print(f"time of modifying {times_of_run} objects "
          f"--- {time_4 - time_3} seconds ---")

    for i in range(times_of_run):
        del flats[i].floor
        del flats[i].windows
        del flats[i].rooms
        del flats[i].door

    time_5 = time.time()
    print(f"time of deleting {times_of_run} objects "
          f"--- {time_5 - time_4} seconds ---")


if __name__ == '__main__':
    run()

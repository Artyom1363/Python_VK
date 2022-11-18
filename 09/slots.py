import weakref
import time


class Window:
    pass
    # def __init__(self, flat):
    #     self.flat = weakref.ref(flat)


class Floor:
    pass
    # def __init__(self, flat):
    #     self.flat = weakref.ref(flat)


class Room:
    pass
    # def __init__(self, flat):
    #     self.flat = weakref.ref(flat)


class Door:
    pass
    # def __init__(self, flat):
    #     self.flat = weakref.ref(flat)


class Flat:
    __slots__ = ("windows", "floor", "rooms", "door")

    def __init__(self, windows, floor, rooms, door):
        self.windows = windows
        self.floor = floor
        self.rooms = rooms
        self.door = door


def run():
    N = 2_000_000

    all_windows = []
    all_floors = []
    all_rooms = []
    all_doors = []
    flats = []

    for _ in range(N):
        all_windows.append(Window())
        all_floors.append(Floor())
        all_rooms.append(Room())
        all_doors.append(Door())

    time_1 = time.time()

    for i in range(N):
        flat = Flat(all_windows[i], all_floors[i], all_rooms[i], all_doors[i])
        flats.append(flat)

    time_2 = time.time()
    print(f"time of creating {N} objects --- {time_2 - time_1} seconds ---")

    for i in range(N):
        if flats[i].floor is not None:
            pass

        if flats[i].windows is not None:
            pass

        if flats[i].rooms is not None:
            pass

        if flats[i].door is not None:
            pass

    time_3 = time.time()
    print(f"time of access to {N} objects --- {time_3 - time_2} seconds ---")

    for i in range(N):
        flats[i].floor = all_floors[i - 1]
        flats[i].windows = all_windows[i - 1]
        flats[i].rooms = all_rooms[i - 1]
        flats[i].door = all_doors[i - 1]

    time_4 = time.time()
    print(f"time of modifying {N} objects --- {time_4 - time_3} seconds ---")

    for i in range(N):
        del flats[i].floor
        del flats[i].windows
        del flats[i].rooms
        del flats[i].door

    time_5 = time.time()
    print(f"time of deleting {N} objects --- {time_5 - time_4} seconds ---")


if __name__ == '__main__':
    run()

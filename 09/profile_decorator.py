import cProfile
import pstats
import io


def profile_deco(func):
    class Wrapper:
        def __init__(self):
            self.profile = cProfile.Profile()
            self.stream = io.StringIO()

        def print_stat(self):
            sortby = "cumulative"
            stats = pstats.Stats(self.profile, stream=self.stream).sort_stats(sortby)
            stats.print_stats()
            stat = self.stream.getvalue()
            print(stat)

        def __call__(self, *args, **kwargs):
            self.profile.enable()
            result = func(*args, **kwargs)
            self.profile.disable()
            return result

    return Wrapper()

import cProfile
import pstats
import io


def profile_deco(func):
    class Wrapper:

        def print_stat(self):
            print(self.stat)

        def __call__(self, *args, **kwargs):
            profile = cProfile.Profile()
            profile.enable()
            result = func()
            profile.disable()

            stream = io.StringIO()
            sortby = "cumulative"
            stats = pstats.Stats(profile, stream=stream).sort_stats(sortby)
            stats.print_stats()
            self.stat = stream.getvalue()

            return result

    return Wrapper()

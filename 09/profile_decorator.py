import cProfile, pstats, io


def profile_deco(func):
    class Wrapper:

        def print_stat(self):
            print(self.stat)

        def __call__(self, *args, **kwargs):
            pr = cProfile.Profile()
            pr.enable()
            result = func()
            pr.disable()

            s = io.StringIO()
            sortby = "cumulative"
            ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
            ps.print_stats()
            self.stat = s.getvalue()
            # print()
            return result
    return Wrapper()

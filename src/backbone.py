from support import *


def parallel(func, arr: Collection, max_workers: int = 12):

    """
    Call `func` on every element of `arr` in parallel using `max_workers`.
    """
    _default_cpus = min(max_workers, num_cpus())
    defaults = SimpleNamespace(
        cpus=_default_cpus, cmap="viridis", return_fig=False, silent=False
    )

    max_workers = ifnone(max_workers, defaults.cpus)
    if max_workers < 2:
        results = [func(o) for i, o in tqdm(enumerate(arr), total=len(arr))]
    else:
        with ProcessPoolExecutor(max_workers=max_workers) as ex:
            futures = [ex.submit(func, o) for i, o in enumerate(arr)]
            results = []
            for f in tqdm(concurrent.futures.as_completed(futures), total=len(arr)):
                results.append(f.result())
    if any([o is not None for o in results]):
        return results


def timer_func(func):
    """
    https://www.geeksforgeeks.org/timing-functions-with-decorators-python/
    """

    def wrap_func(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        print(f"Function {func.__name__!r} executed in {(t2-t1):.4f}s")
        return result

    return wrap_func


def split_by_func(items, f):
    """
    Split a list by a function
    """
    mask = [f(o) for o in items]
    f = [o for o, m in zip(items, mask) if m == False]
    t = [o for o, m in zip(items, mask) if m == True]
    return f, t

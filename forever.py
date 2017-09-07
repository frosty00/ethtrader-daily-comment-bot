import prawcore


def forever(f):
    def inner():
            while True:
                try:
                    f()
                except prawcore.exceptions.RequestException:
                    pass
    return inner

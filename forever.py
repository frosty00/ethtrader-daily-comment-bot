import prawcore


def forever(f):
    def inner():
            while True:
                try:
                    f()
                except prawcore.exceptions.RequestException or prawcore.exceptions.ServerError:
                    pass
    return inner

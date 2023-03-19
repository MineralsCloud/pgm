from pgm.version import __version__


def print_banner():
    print(
        f"""
  _ __   __ _ _ __ ___
 | '_ \ / _` | '_ ` _ \
 | |_) | (_| | | | | | |
 | .__/ \__, |_| |_| |_|
 | |     __/ |
 |_|    |___/
 Version {__version__}
    """
    )


if __name__ == "__main__":
    print_banner()

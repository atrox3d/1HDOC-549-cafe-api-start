################################################################################
# https://stackoverflow.com/questions/14132789/relative-imports-for-the-billionth-time
# https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html#case-3-importing-from-parent-directory
################################################################################
import os, sys


def parent_import():
    """
    add project root to sys.path to import from parent folder
    change the number of ".." accordingly
    """
    root = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), ".."))
    print(f"adding project root tp sys.path: {root=}")
    sys.path.append(root)


################################################################################

def show_syspath():
    for n, p in enumerate(sys.path):
        print(f"{n=}, {p=}")

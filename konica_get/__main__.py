import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).parent.parent))


if __name__ == '__main__':
    from konica_get import KonicaGet
    kg = KonicaGet(headless=False)
    kg.get_all_docs(delete=True)
    del kg


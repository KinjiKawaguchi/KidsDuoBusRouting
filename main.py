from src.utils.ConsoleOperation import ConsoleOperation
from src.utils.FileOperation import FileOperation


def main():
    co = ConsoleOperation()
    fo = FileOperation()
    co.handle_main_manu(fo)

if __name__ == "__main__":
    main()

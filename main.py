from src.utils.ConsoleOperation import ConsoleOperation
from src.utils.FileOperation import FileOperation


def main():
    co = ConsoleOperation()
    fo = FileOperation()
    co.login_or_register(fo)
    fo.instantiate_google_api_client()
    co.handle_main_menu(fo)


if __name__ == "__main__":
    main()

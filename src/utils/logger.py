class Logger(object):

    @staticmethod
    def banner(text):
        """ Display log banner (unrelated to loguru or logger configuration) """
        print(Fore.YELLOW, end=" |")
        print("="*15, end="")
        print(Fore.RED, end="")
        print(f" {text.upper()}", end=Fore.YELLOW)
        print("="*15, end="|\n")


import threading
from queue import Queue
import time


class Cutlery:
    """Cutlery manager"""

    def __init__(self, knives=0, forks=0):
        self.knives = knives
        self.forks = forks
        self.lock = threading.Lock()

    def give(self, to: "Cutlery", knives=0, forks=0):
        self.change(-knives, -forks)
        to.change(knives, forks)

    def change(self, knives, forks):
        with self.lock:
            self.knives += knives
            self.forks += forks

    def __str__(self):
        return f"[kitchen] knives:{self.knives}, forks:{self.forks}"


class ThreadBot(threading.Thread):
    """Serving bot managing tasks and cutlery"""

    def __init__(self, bot_capa=4, verbose=False):
        super().__init__(target=self.manage_table)
        self.cutlery = Cutlery(knives=0, forks=0)
        self.tasks = Queue()
        self.bot_capa = bot_capa
        self.verbose = int(verbose)

    def manage_table(self):
        while True:
            task = self.tasks.get()
            if task == "prepare table":
                kitchen.give(to=self.cutlery, knives=self.bot_capa, forks=self.bot_capa)
                if self.verbose:
                    print(f"bot<-kit\t{kitchen}")
                    time.sleep(1)
            elif task == "clear table":
                self.cutlery.give(to=kitchen, knives=self.bot_capa, forks=self.bot_capa)
                if self.verbose:
                    print(f"bot->kit\t{kitchen}")
                    time.sleep(1)
            elif task == "shutdown":
                return


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Servig bot")
    parser.add_argument("--bot_num", type=int, default=10)
    parser.add_argument("--task_num", type=int, default=10)
    parser.add_argument("--inventory", type=int, default=100)
    parser.add_argument("--bot_capa", type=int, default=4)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    kitchen = Cutlery(knives=args.inventory, forks=args.inventory)
    bots = [
        ThreadBot(bot_capa=args.bot_capa, verbose=args.verbose)
        for i in range(args.bot_num)
    ]

    for bot in bots:
        for i in range(args.task_num):
            bot.tasks.put("prepare table")
            bot.tasks.put("clear table")
        bot.tasks.put("shutdown")

    print("Kitchen inventory before service:", kitchen)
    for bot in bots:
        bot.start()

    for bot in bots:
        bot.join()
    print("Kitchen inventory after service:", kitchen)

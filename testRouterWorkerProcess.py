import sys
sys.path.append(sys.path[0] + "/..")
import caffeine.worker


class TestRouterWorker(caffeine.worker.Worker):

    def handle_message(self, message):
        print("worker saying hello", message)
        return b'worker says hello'

if __name__ == "__main__":

    TestRouterWorker().runloop()

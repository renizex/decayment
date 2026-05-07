class UI:
    @staticmethod
    def display(text):
        print(text)

    @staticmethod
    def get_input(prompt="> "):
        return input(prompt)

    def pause(self, message = None):
        if message:
            self.display(message)
        self.display("нажми Enter чтобы продолжить")
        self.get_input()
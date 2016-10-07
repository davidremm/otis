

class Run():

    def __init__(self, sub_parser):
        self._parser = sub_parser.add_parser('run')
        self._parser.set_defaults(func=self.run)

    def run(self, args):
        print("running...")

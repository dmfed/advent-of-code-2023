
class Reader(object):
    def __init__(self, filename):
        self.filename = filename

    def read(self):
        lines = []
        with open(self.filename, 'r') as f:
            for line in f.readlines():
                lines.append(line.strip())
        return lines
                

class File:
    def __init__(self, name, size, parent=None):
        self.name = name
        self.size = size
        self.parent = parent

    def get_size(self):
        return self.size

class Folder:
    def __init__(self, name, parent=None):
        self.name = name
        self.content = []
        self.parent = parent
    
    def get_size(self):
        return sum([item.get_size() for item in self.content])

    def add_file(self, name, size):
        self.content.append(File(name, size, self))

    def add_folder(self, name):
        self.content.append(Folder(name, self))

    def get_folder(self, name):
        return next(filter(lambda item: isinstance(item, Folder) and item.name == name, self.content))

with open('example.txt') as file:
    root = Folder('/')
    current_folder = root

    for line in file.readlines():
        match line.split():
            case '$', 'cd', '/':
                current_folder = root
            case '$', 'cd', '..': 
                current_folder = current_folder.parent
            case '$', 'cd', name:
                current_folder = current_folder.get_folder(name)
            case '$', 'ls':
                pass
            case 'dir', name:
                current_folder.add_folder(name)
            case filesize, _:
                current_folder.add_file(line[1], int(filesize))

    sizes = []
    def rec(folder):
        sizes.append(folder.get_size())
        for f in folder.content:
            if isinstance(f, Folder):
                rec(f)
    rec(root)

    print("part1:", sum([s for s in sizes if s < 100_000]))

    space_on_disk = 70_000_000
    space_needed = 30_000_000
    space_occupied = root.get_size()
    space_required = space_needed - (space_on_disk - space_occupied)
    print("part2", min([s for s in sizes if s >= space_required]))

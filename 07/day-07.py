import sys

sep = '/'

class Directory:

    def __init__(self, path):
        self.path = path
        self.dirs = {}
        self.files = {}

    def add_record(self, spec):
        if (spec.startswith('dir')):
            _, name = spec.split(' ')
            child = Directory(sep.join([self.path, name]))
            self.dirs[name] = child
            return child
        else:
            size, name = spec.split(' ')
            self.files[name] = int(size)
            return None

    @property
    def size(self):
        files = sum(self.files.values())
        dirs = sum(d.size for d in self.dirs.values())
        return files + dirs

pwd = ['/']
root = Directory(pwd[0])
all_dirs = {root.path: root}

for l in map(str.rstrip, sys.stdin):
    parts = l.split(' ')

    if parts[0] == '$':
        # Change directory
        if parts[1] == 'cd':
            if parts[2] == '/':
                pwd = ['/']
            elif parts[2] == '..':
                pwd.pop()
            else:
                pwd.append(parts[2])
        else:
            # Do nothing for ls
            continue
    else:
        current_path = sep.join(pwd)
        current_dir = all_dirs[current_path]
        new_dir = current_dir.add_record(l)
        if new_dir:
            all_dirs[new_dir.path] = new_dir

# Part 1
total = 0
for d in all_dirs.values():
    if d.size <= 100000:
        total += d.size

print(total)

# Part 2
max_space = 70000000
target_free = 30000000
current_free = max_space - root.size

choices = []
for d in all_dirs.values():
    if current_free + d.size >= target_free:
        choices.append(d.size)

print(min(choices))

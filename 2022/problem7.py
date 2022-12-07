import utils


class DirectoryTreeNode:
    def __init__(self, name, parent_directory=None):
        """
        :param str name:
        :param DirectoryTreeNode parent_directory:
        """
        self.name = name
        self.parent_directory = parent_directory
        self.directory_map = {}
        self.files = list()
        self.size = 0

    def add_file(self, file):
        """
        :param File file:
        """
        self.files.append(file)
        self.size += file.size

        parent_node = self.parent_directory
        while parent_node:
            parent_node.size += file.size
            parent_node = parent_node.parent_directory


class File:
    def __init__(self, name, size):
        """
        :param str name:
        :param int size:
        """
        self.name = name
        self.size = size


def get_input():
    with utils.get_input_fd(__file__) as f:
        lines = f.read().split("\n")

    root_directory = DirectoryTreeNode(name="/")
    current_directory = root_directory
    directory_list = [current_directory]
    for line in lines[1:]:
        if line.startswith("$"):
            command_parts = line.split(" ")
            if command_parts[1] == "ls":
                continue
            elif command_parts[1] == "cd":
                if command_parts[2] == "..":
                    current_directory = current_directory.parent_directory
                else:
                    current_directory = current_directory.directory_map[
                        command_parts[2]
                    ]
        else:
            size, name = line.split()
            if size == "dir":
                new_directory = DirectoryTreeNode(
                    name=name, parent_directory=current_directory
                )
                current_directory.directory_map[name] = new_directory
                directory_list.append(new_directory)
            else:
                current_directory.add_file(File(name=name, size=int(size)))

    return root_directory, directory_list


def part1():
    _, directory_list = get_input()
    return sum(
        directory.size for directory in directory_list if directory.size < 100000
    )


def part2():
    root_directory, directory_list = get_input()
    unused_space = 70000000 - root_directory.size
    space_needed = 30000000 - unused_space

    for directory in sorted(directory_list, key=lambda x: x.size):
        if space_needed < directory.size:
            return directory.size


if __name__ == "__main__":
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")

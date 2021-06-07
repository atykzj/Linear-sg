# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Convert new list of url to  website
import os

def list_all_files_dirs(rootdir = '.'):
    l = []
    for file in os.listdir(rootdir):
        d = os.path.join(rootdir, file)
        if os.path.isdir(d):
            for path, subdirs, files in os.walk('.\photos'):
                for name in files:
                    l.append(name)
    #                 print(os.path.join(path, name))
    return l


def iter_given_dir(directory):
    fn = []
    for filename in os.listdir(directory):
        fn.append(filename)
    return fn

def retrieve_attributes(files):
    l = []
    for i in files:
        if i.endswith(".jpg"):
            idx = i[:6]
            temp = i[7:-4].split(', ')
            add = temp.pop(0)
            ids = temp.pop(0)
            t = temp.pop(-1)
            room = temp.pop(-1)
            styles = temp
            td = {}
            td[idx] = {"address": add, "designer": ids, "type": t, "room": room, "styles": styles}
            l.append(td)
    return l

def setup_gcp_link(l):
    pre = "https://storage.googleapis.com/linear-static-assets/"
    temp = []
    for i in l:
        temp.append(pre + i)
    return temp

def setup_gcp():



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

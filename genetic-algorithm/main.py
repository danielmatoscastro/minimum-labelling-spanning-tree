from model.instance import Instance
    
if __name__ == '__main__':
    instance = Instance.load('data/testFile_0_10_5.col')
    print(instance)

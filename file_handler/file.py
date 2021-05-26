'''
binding a file with a class.
this class return some method:
edit(self) -> append content to file

'''

class File:
    def __init__(self, *args, **kwargs) -> None:
        self.main = open(kwargs['filename'],'a')
        self.content = kwargs['content']
        pass
    
    def edit(self) -> None:
        self.main.write(self.content)
        pass

    def save(self):
        self.main.close()
    
name = "test.txt"
f = File(filename = name, content = "something")
f.edit()
f.save()


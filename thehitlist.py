
import appscript

class Task(object):
    thl = appscript.app('The Hit List')
    
    @classmethod
    def find_tagged(cls, tagname):
        for tag in cls.thl.tags_group.groups.get():
            if tag.name.get() == tagname:
                return [Task(t) for t in tag.tasks.get()]
        return []
    
    def __init__(self, osatask):
        self.osatask = osatask
    
    def gettitle(self):
        return self.osatask.title.get()
    def settitle(self, value):
        self.osatask.title.set(value)
    title = property(gettitle, settitle)


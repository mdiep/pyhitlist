
import appscript


class Group(object):
    def __init__(self, osagrp):
        self.osagrp = osagrp

    def getname(self):
        return self.osagrp.name.get()
    def setname(self, value):
        self.osagrp.name.set(value)
    name = property(getname, setname)
    
    @property
    def tasks(self):
        return [Task(t) for t in self.osagrp.tasks.get()]


class Tag(Group):
    pass    


class TheHitList(object):
    app = appscript.app('The Hit List')
    
    @classmethod
    def tags(cls):
        return [Tag(t) for t in cls.app.tags_group.groups.get()]


class Task(object):
    @classmethod
    def find_tagged(cls, tagname):
        for tag in TheHitList.tags():
            if tag.name == tagname:
                return tag.tasks
        return []
    
    def __init__(self, osatask):
        self.osatask = osatask
    
    def gettitle(self):
        return self.osatask.title.get()
    def settitle(self, value):
        self.osatask.title.set(value)
    title = property(gettitle, settitle)



import appscript


class Group(object):
    def __init__(self, osagrp):
        self.osagrp = osagrp

    def __getname(self):
        return self.osagrp.name.get()
    def __setname(self, value):
        self.osagrp.name.set(value)
    name = property(__getname, __setname)


class Folder(Group):
    @property
    def groups(self):
        groups = []
        for g in self.osagrp.groups.get():
            try:
                g.groups.get()
                groups.append(Folder(g))
            except:
                groups.append(List(g))
        return groups


class List(Group):
    @property
    def name(self):
        return super(List,self).name
    
    @property
    def tasks(self):
        return [Task(t) for t in self.osagrp.tasks.get()]


class Tag(Group):
    @property
    def tasks(self):
        return [Task(t) for t in self.osagrp.tasks.get()]


class TheHitList(object):
    app = appscript.app('The Hit List')
    
    inbox    = List(app.inbox)
    today    = List(app.today_list)
    upcoming = List(app.upcoming_list)
    
    groups = Folder(app.folders_group)
    
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


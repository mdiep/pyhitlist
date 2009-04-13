
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
    def __iter__(self):
        return iter(self.groups)
    
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
    def __iter__(self):
        return iter(self.tasks)
    
    @property
    def name(self):
        return super(List,self).name
    
    @property
    def tasks(self):
        return [Task(t) for t in self.osagrp.tasks.get()]


class Tag(Group):
    def __iter__(self):
        return iter(self.tasks)
    
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
    
    def __init__(self, title, **kwargs):
        # internally, we actually pass in an osatask to load
        # an existing object
        if isinstance(title, appscript.reference.Reference):
            self.osatask = title
        else:
            folder = kwargs.pop('folder', TheHitList.inbox)
            keynames = {
                'notes':    appscript.k.notes,
                'priority': appscript.k.priority,
            }
            props = {}
            props[appscript.k.title] = title
            for key, value in kwargs.items():
                if key in keynames:
                    props[keynames[key]] = kwargs[key]
            
            folder.osagrp.make(new=appscript.k.task, with_properties=props)
    
    def gettitle(self):
        return self.osatask.title.get()
    def settitle(self, value):
        self.osatask.title.set(value)
    title = property(gettitle, settitle)
    
    def __notes(self):
        return self.osatask.notes.get()
    def __setnotes(self, value):
        self.osatask.notes.set(value)
    notes = property(__notes, __setnotes)
    
    def __priority(self):
        return self.osatask.priority.get()
    def __setpriority(self, value):
        self.osatask.priority.set(value)
    priority = property(__priority, __setpriority)


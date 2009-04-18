
import appscript
import re
from datetime import date


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
    
    def __getitem__(self, key):
        if type(key) == int:
            return self.groups[key]
        if type(key) == str or type(key) == unicode:
            for g in self.groups:
                if g.name == key:
                    return g
        raise KeyError, key


class TagFolder(Folder):
    @property
    def groups(self):
        return [Tag(t) for t in self.osagrp.groups.get()]


class List(Group):
    def __iter__(self):
        return iter(self.tasks)
    
    @property
    def name(self):
        return super(List,self).name
    
    @property
    def archived(self):
        return [Task(t) for t in self.osagrp.tasks[appscript.its.archived == True].get()]
    
    @property
    def tasks(self):
        return [Task(t) for t in self.osagrp.tasks[appscript.its.archived != True].get()]


class Tag(Group):
    def __iter__(self):
        return iter(self.tasks)
    
    @property
    def archived(self):
        return [Task(t) for t in self.osagrp.tasks[appscript.its.archived == True].get()]
    
    @property
    def tasks(self):
        return [Task(t) for t in self.osagrp.tasks[appscript.its.archived != True].get()]


class TheHitList(object):
    app = appscript.app('The Hit List')
    
    inbox    = List(app.inbox)
    today    = List(app.today_list)
    upcoming = List(app.upcoming_list)
    
    folders = Folder(app.folders_group)
    tags    = TagFolder(app.tags_group)


class TagError(Exception):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return repr(self.value)


class Task(object):
    def __init__(self, title, **kwargs):
        # internally, we actually pass in an osatask to load
        # an existing object
        if isinstance(title, appscript.reference.Reference):
            self.osatask = title
        else:
            for name in kwargs.pop('tags', []):
                title += ' /' + name
                if ' ' in name:
                    title += '/'
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
            
            self.osatask = folder.osagrp.make(new=appscript.k.task, with_properties=props)
    
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
    
    def istagged(self, name):
        for tag in self.tags:
            if tag.name == name:
                return True
        return False
    
    @property
    def tags(self):
        pattern = re.compile(r'\s/(?P<tag>[^/]*[^/ ])/?')
        names   = (match.group('tag') for match in pattern.finditer(self.title))
        return [TheHitList.tags[name] for name in names];
    
    def tag(self, name):
        if self.istagged(name):
            raise TagError, "already tagged " + name
        if ' ' in name:
            name += '/'
        self.title += ' /' + name
    
    def untag(self, name):
        if not self.istagged(name):
            raise TagError, "not tagged " + name
        pattern    = re.compile(r'\s/' + re.escape(name) + r'/?')
        self.title = pattern.sub('', self.title)
    
    def start_today(self):
        self.osatask.start_date.set(date.today())


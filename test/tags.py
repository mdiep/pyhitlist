
import unittest

from test.base  import HitListTest
from thehitlist import *

class TagTestCase(HitListTest):
    def test_01_read_tags(self):
        tags = TheHitList.tags
        self.assertEquals(len(tags.groups), 2)
        self.assertEquals(tags[0].name, 'pyhitlist')
        self.assertEquals(tags[1].name, 'spaced tag')
    
    def test_02_lookup_tags(self):
        tags = TheHitList.tags
        self.assertEquals(tags['pyhitlist'].name,  'pyhitlist')
        self.assertEquals(tags['spaced tag'].name, 'spaced tag')
    
    def test_03_tasks_of_tags(self):
        pyhltag = TheHitList.tags['pyhitlist']
        self.assertEquals(len(pyhltag.tasks), 2)
        self.assertEquals(pyhltag.tasks[0].title, 'Inbox Task 1 /pyhitlist /spaced tag/')
        self.assertEquals(pyhltag.tasks[1].title, 'Inbox Task 2 /pyhitlist')
        
        spacedtag = TheHitList.tags['spaced tag']
        self.assertEquals(len(pyhltag.tasks), 2)
        self.assertEquals(spacedtag.tasks[0].title, 'Inbox Task 1 /pyhitlist /spaced tag/')
        self.assertEquals(spacedtag.tasks[1].title, 'Uno Task 1 /spaced tag/')
    
    def test_04_tagging_tasks(self):
        spacedtag = TheHitList.tags['spaced tag']
        inboxtask1 = spacedtag.tasks[0]
        inboxtask1.tag('blah')
        self.assertEquals(inboxtask1.title, 'Inbox Task 1 /pyhitlist /spaced tag/ /blah')
        self.assertRaises(TagError, inboxtask1.tag, 'pyhitlist')
    
    def test_05_untagging_tasks(self):
        spacedtag = TheHitList.tags['spaced tag']
        inboxtask1 = spacedtag.tasks[0]
        inboxtask1.untag('pyhitlist')
        inboxtask1.untag('spaced tag')
        self.assertEquals(inboxtask1.title, 'Inbox Task 1')
        self.assertRaises(TagError, inboxtask1.untag, 'pyhitlist')

if __name__ == '__main__':
    unittest.main()



import unittest

from test.base import HitListTest
from thehitlist import *

class TaskTestCase(HitListTest):
    def test_01_read_tasks(self):
        task = TheHitList.folders['Uno'].tasks[0]
        self.assertEqual(task.title, 'Uno Task 1 /spaced tag/')
        
        self.assertEqual(len(task.tags), 1)
        self.assertEqual(task.notes, 'Notes for this task')
        self.assertEqual(task.priority, 2)
    
    def test_02_create_tasks(self):
        inbox = TheHitList.inbox
        self.assertEqual(len(inbox.tasks), 2)
        Task('A new task')
        self.assertEqual(len(inbox.tasks), 3)
        
        empty = TheHitList.folders['Empty']
        self.assertEqual(len(empty.tasks), 0)
        task = Task('New task', folder=empty, priority=5, notes='New notes', tags=['foo bar', 'blah'])
        self.assertEqual(len(empty.tasks), 1)
        self.assertEqual(task.title, 'New task /foo bar/ /blah')
        self.assertEqual(task.priority, 5)
        self.assertEqual(task.notes, 'New notes')
        self.assertEqual(len(task.tags), 2)
        self.assertEqual(task.tags[0].name, 'foo bar')
        self.assertEqual(task.tags[1].name, 'blah')

if __name__ == '__main__':
    unittest.main()


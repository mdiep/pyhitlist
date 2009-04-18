
import os
import time
import unittest

from thehitlist import *

LIBRARY_NAME = 'PyHitListTestLibrary.thllibrary'

class HitListTest(unittest.TestCase):
    """
    To avoid changing actual Hit List data, we want to quit The Hit List, point
    it to a test database, run the tests, and then restore the original data.
    """
    def __libraryPath(self):
        pipe = os.popen("defaults read com.potionfactory.TheHitList libraryPath")
        return pipe.readline().strip('\n')
    def __setLibraryPath(self, path):
        os.popen("defaults write com.potionfactory.TheHitList libraryPath '%s'" % path)
    libraryPath = property(__libraryPath, __setLibraryPath)

    def setUp(self):
        self.wasrunning = TheHitList.app.isrunning()
        if self.wasrunning:
            TheHitList.app.quit()
            time.sleep(0.1) # launching too quickly after a quit slows things way down
        
        # copy the test data
        library = os.path.dirname(__file__) + '/' + LIBRARY_NAME
        os.popen("cp -R '%s' /tmp" % library)
        
        # point THL to the test libary
        self.originalPath = self.libraryPath
        self.libraryPath  = '/tmp/' + LIBRARY_NAME
        
        TheHitList.app.launch()
    
    def tearDown(self):
        TheHitList.app.quit()
        time.sleep(0.1) # launching too quickly after a quit slows things way down
        
        # point THL back to the original library
        self.libraryPath = self.originalPath
        
        if self.wasrunning:
            TheHitList.app.launch()


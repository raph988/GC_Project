# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 11:28:28 2017

@author: Raph
"""

from PySide.QtGui import QApplication, QPixmap, QSplashScreen
from PySide.QtCore import Qt
import sys
import logging

from utils import getFromConfig

"""
TO TRY : https://pypi.python.org/pypi/pickleshare
"""

# a try for logs... don't seem to work with PyInstaller on 64bits windows
class StreamToLogger(object):
    
   def __init__(self, logger, log_level=logging.INFO):
       self.logger = logger
       self.log_level = log_level
       self.linebuf = ''
       
   def write(self, buf):
      for line in buf.rstrip().splitlines():
         self.logger.log(self.log_level, buf.rstrip())


    
#class LogWriter(object):
#    def __init__(self, logger, level):
#        self.level = level
##        self.logger = logger
##        if level == logging.ERROR:
##            self.std_com = sys.stderr
##        elif level == logging.DEBUG:
##            self.std_com = sys.stdout
#    def write(self, buf):
##        self.std_com.write(buf)
#        self.logger.log(self.level, buf)
#    def flush(self):
#        self.logger.error(self._stderr)



def main():
    
#    print isfile(getFromConfig("path", "stylesheet_file"))
    with open(getFromConfig("path", "stylesheet_file"), 'r') as f:
        style = f.read()
    app = QApplication(sys.argv)
#    app.translate()
    app.setStyleSheet(style)
    
    pixmap = QPixmap("./data/lancement.png")
    pixmap = pixmap.scaledToHeight(150, Qt.SmoothTransformation)
    splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint)
    splash.show()
    app.processEvents()
    
    
    
    ##########################################
    try: 
        logging.basicConfig(level=logging.DEBUG)#,
    #        format='%(asctime)-15s %(levelname)-8s %(message)s',
    #        datefmt='%Y-%m-%d %H:%M:%S',
    #        filename="Log.log",
    #        filemode='w')
        
        
        stdout_logger = logging.getLogger()
        stderr_logger = logging.getLogger()
        
        fh_debug = logging.FileHandler('Log.log')
        fh_debug.setLevel(logging.DEBUG)
        fh_debug.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
        stdout_logger.addHandler(fh_debug)
        
    #    sh = logging.StreamHandler(sys.stdout)
    #    sh.setLevel(logging.DEBUG)
    #    sh.setFormatter(logging.Formatter('%(asctime)-15s %(levelname)-8s %(message)s'))
    #    stdout_logger.addHandler(sh)
        
#        sys.stdout = StreamToLogger(stdout_logger, logging.DEBUG)
#        sys.stderr = StreamToLogger(stderr_logger, logging.ERROR)
    except:
        try:
            for handler in stdout_logger.handlers:
                handler.close()
                stdout_logger.removeFilter(handler)
                
            for handler in stderr_logger.handlers:
                handler.close()
                stderr_logger.removeFilter(handler)
        except:
            pass
    #########################################

    # IMPORT MODULES
    from classes import Market
    from ui_manager import Ui_manager

    # INITIALIZATION ##  
    Market()

    # EXECUTE
    setup = Ui_manager()
    setup.show()
    splash.finish(setup)
    
    sys.exit(app.exec_())
        


if __name__ == '__main__':
    main()

  

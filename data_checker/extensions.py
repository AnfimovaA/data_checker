import glob
import filecmp

from scrapy import signals
from scrapy.exceptions import NotConfigured

class EmailOnchange(object):
    @classmethod
    def from_crawler(cls, crawler):
        if not crawler.settings.getbool("EMAIL_ON_CHANGE_ENABLED"):
            reaise NotConfigured

        extension = cls()

        crawler.signals.connect(extension.engine_stopped, signal=signals.engine_stopped)

        return extension

    def engine_stopped(self):
        runs = sorted(glob.glob("/tmp/[0-9]*-[0-9]*-[0-9]*T[0-9]*-[0-9]*-[0-9]*.json"), reverse=True)
        if len(runs) < 2:
            return
        
        current_file, previous_file = runs[0:2]
        if not filecmp.cmp(current_file, previous_file):
            print("\n\nTHE FILES ARE DIFFERENT\n\n")
        else:
            print("\n\nNO CHANGE\n\n")
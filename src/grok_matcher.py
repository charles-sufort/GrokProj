from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.select import Select
from grok_manager import GrokManager


class GrokTester:
    def __init__(self,logfile,ctg):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches",["enable-automation"])
        options.add_experimental_option('useAutomationExtension',False)
        self.driver = webdriver.Chrome()
        self.grok_manager = GrokManager()
        self.logfile = logfile
        self.ctg = ctg
        self.load_files()

    def load_files(self):
        self.logs = self.grok_manager.get_logs(self.logfile,self.ctg)
        self.patterns = self.grok_manager.get_patterns(self.logfile,self.ctg)
        self.log_str = "\n".join(self.logs[:50])
        print("log string")
        print(self.log_str)
        self.pattern_str = "({})".format(self.patterns[0])
        print("pattern string")
        for pattern in self.patterns[1:]:
            self.pattern_str += "|({})".format(pattern)
        print(self.pattern_str)

    def test_files(self):
        d = int(len(self.logs) / 100)
        inds = [i*100 for i in range(d+1)] + [len(self.logs)]
        print(inds)
        for i in range(d+1):
            self.driver.get("http://grokconstructor.appspot.com/do/match")
            log_str = "\n".join(self.logs[inds[i]:inds[i+1]])
            loglines = self.driver.find_element(By.ID,"loglines")
            loglines.send_keys(log_str)
            pattern = self.driver.find_element(By.ID,"pattern")
            pattern.send_keys(self.pattern_str)
            submit = self.driver.find_element(By.ID,"submit")
            submit.submit()
            success_elems = self.driver.find_elements(By.CLASS_NAME,"success")
            error_elems = self.driver.find_elements(By.CLASS_NAME,"ym-fbox-text ym-error")
            print(error_elems)
            print("logs: {}".format(len(self.logs)))
            print("patterns: {}".format(len(self.patterns)))
            print("successes: {}".format(len(success_elems)))
            print("fails: {}".format(len(error_elems)))
            input()













GT = GrokTester("secure","sshd_disconnected")
GT.test_files()

input()


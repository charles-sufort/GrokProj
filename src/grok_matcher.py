from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from grok_manager import GrokManager


class GrokTester:
    def __init__(self,logfile,ctg):
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches",["enable-automation"])
        options.add_experimental_option('useAutomationExtension',False)
        self.driver = webdriver.Firefox()

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
        l_int = 200
        d = int(len(self.logs) / l_int)
        inds = [i*l_int for i in range(d+1)] + [len(self.logs)]
        print(inds)
        matched = []
        not_matched = []
        for i in range(d+1):
            self.driver.get("http://grokconstructor.appspot.com/do/match")
            log_str = "\n".join(self.logs[inds[i]:inds[i+1]])
            loglines = self.driver.find_element(By.ID,"loglines")
            loglines.send_keys(log_str)
            pattern = self.driver.find_element(By.ID,"pattern")
            pattern.send_keys(self.pattern_str)
            WebDriverWait(self.driver,5)
            submit = self.driver.find_element(By.ID,"submit")

            submit.submit()
            WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.TAG_NAME,"table")))

            table = self.driver.find_element(By.TAG_NAME,"table")
            rows = table.find_elements(By.TAG_NAME,"tr")
            prev = None
            str1 = "MATCHED"
            str2 = "NOT MATCHED"
            for row in rows:
                row_text = row.text
                if row_text == "MATCHED":
                    matched.append(prev.text)
                elif row_text[:len(str2)] == str2:
                    not_matched.append(prev.text)
                prev = row
            success_elems = self.driver.find_elements(By.CLASS_NAME,"success")
            error_elems = self.driver.find_elements(By.CLASS_NAME,"ym-fbox-text ym-error")
            print("logs: {}".format(len(self.logs)))
            print("patterns: {}".format(len(self.patterns)))
            print("successes: {}".format(len(matched)))
            print("fails: {}".format(len(not_matched)))
            print(not_matched)
            







GT = GrokTester("fail2ban","fail2ban")

print(GT.pattern_str)
GT.test_files()

input()


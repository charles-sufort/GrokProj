import os
import json
import re

class LogFileTool:
    def __init__(self,log,keyword_file):
        self.dir = "../data/{}".format(log)
        self.keyword_file = self.dir + "/" + keyword_file
        self.extract_logs()
        self.extract_keywords()
        self.ctg_log_files()

    def extract_logs(self):
        self.logs = {}
        log_dir = self.dir + "/logs"
        self.log_files = os.listdir(log_dir)
        for log_file in self.log_files:
            self.logs[log_file] = []
            file_path = log_dir + "/{}".format(log_file)
            with open(file_path,"r") as fo:
                for log in fo:
                    self.logs[log_file].append(log[:-1])

    def extract_keywords(self):
        self.re_keywords = []
        with open(self.keyword_file,"r") as fo:
            self.re_keywords = json.load(fo)["keyword_re"]

    def ctg_log_files(self):
        self.log_ctg_obj = {}
        for log_file in self.logs:
            logs = self.logs[log_file]
            log_obj = {}
            log_obj["count"] = len(logs)
            log_obj["re_keywords"] = {self.re_keywords[i]["name"]:{"re_keywords":self.re_keywords[i]["pattern"],"matches":[]} for i in range(len(self.re_keywords))}
            log_obj["no_matches"] = []
            for log in logs:
                log_match = False
                for i in range(len(self.re_keywords)):
                    key = self.re_keywords[i]["name"]
                    p = re.compile(self.re_keywords[i]["pattern"])
                    match = p.search(log)
                    if match is not None:
                        if log_match == True:
                            print("double match")
                        log_obj["re_keywords"][key]["matches"].append(log)
                        log_match = True
                if not log_match:
                    log_obj["no_matches"].append(log)
            self.log_ctg_obj[log_file] = log_obj

    def info_ctg(self):
        total_match_count = 0
        total = 0
        for log_file in self.log_files:
            print("log_file: {}".format(log_file))
            log_count = self.log_ctg_obj[log_file]["count"]
            total += log_count
            match_count = 0
            for i in range(len(self.re_keywords)):
                key = self.re_keywords[i]["name"]
                matches = len(self.log_ctg_obj[log_file]["re_keywords"][key]["matches"])
                match_count += matches
              #  print("----keyword: {}".format(self.re_keywords[i]))
              #  print("++++matches: {} / {}".format(matches,log_count))
            no_match_count = len(self.log_ctg_obj[log_file]["no_matches"])
       #     print("--total {} ({} / {})".format(match_count/log_count,match_count,log_count))
       #     print("--no matches {} ({} / {})".format(no_match_count/log_count,no_match_count,log_count))
       #     print(match_count + no_match_count == log_count)
            total_match_count += match_count
        print("matches {} ({} / {})".format( total_match_count / total, total_match_count, total))



    def write_no_matches(self,pre_path):
        for log_file in self.log_files:
            no_matches = self.log_ctg_obj[log_file]["no_matches"]
            file_path =  "{}_{}.no_matches".format(pre_path,log_file)
            with open(file_path,"w") as fo:
                for log in self.log_ctg_obj[log_file]["no_matches"] :
                    fo.write(log + "\n")
    
    def write_ctg_files(self):
        for i in range(len(self.re_keywords)):
            for log_file in self.log_files:
                key  = self.re_keywords[i]["name"]
                matches = self.log_ctg_obj[log_file]["re_keywords"][key]["matches"]
                file_path = self.dir + "/log_ctgs/{}.log".format(key)
                with open(file_path,"a") as fo:
                    for match in matches:
                        fo.write(match+"\n")

        pattern_obj = {self.re_keywords[i]["name"]: [] for i in range(len(self.re_keywords))}
        path = self.dir + "/ctg_patterns.json"
        with open(path,"w") as fo:
            json.dump(pattern_obj,fo,indent=4)
            


if __name__ == "__main__":
    #files = os.listdir()
    #log_files = []
    #for file in files:
    #    print(file[:4])
    #    if file[-4:] == ".log" and file[:6] == "secure":
    #        log_files.append(file)
    #print(log_files)
    tool = LogFileTool("secure","log_ctgs.json")
    tool.info_ctg()
    tool.write_no_matches("test1")
    tool.write_ctg_files()



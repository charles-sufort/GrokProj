import os
import json
import re

class LogFileTool:
    def __init__(self,keyword_file,log_files):
        self.keyword_file = keyword_file
        self.log_files = log_files
        self.extract_logs()
        self.extract_keywords()
        self.ctg_log_files()

    def extract_logs(self):
        self.logs = {}
        for log_file in self.log_files:
            self.logs[log_file] = []
            with open(log_file,"r") as fo:
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
            log_obj["re_keywords"] = {"keyword_{}".format(i):{"re_keywords":self.re_keywords[i],"matches":[]} for i in range(len(self.re_keywords))}
            log_obj["no_matches"] = []
            for log in logs:
                log_match = False
                for i in range(len(self.re_keywords)):
                    key = "keyword_{}".format(i)
                    p = re.compile(self.re_keywords[i])
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
                key = "keyword_{}".format(i)
                matches = len(self.log_ctg_obj[log_file]["re_keywords"][key]["matches"])
                match_count += matches
              #  print("----keyword: {}".format(self.re_keywords[i]))
              #  print("++++matches: {} / {}".format(matches,log_count))
            no_match_count = len(self.log_ctg_obj[log_file]["no_matches"])
       #     print("--total {} ({} / {})".format(match_count/log_count,match_count,log_count))
       #     print("--no matches {} ({} / {})".format(no_match_count/log_count,no_match_count,log_count))
       #     print(match_count + no_match_count == log_count)
            total_match_count += match_count
        print("matches {} ({} / {})", total_match_count / total, total_match_count, total)



    def write_no_matches(self,pre_path):
        for log_file in self.log_files:
            no_matches = self.log_ctg_obj[log_file]["no_matches"]
            file_path =  "{}_{}.no_matches".format(pre_path,log_file)
            with open(file_path,"w") as fo:
                for log in self.log_ctg_obj[log_file]["no_matches"] :
                    fo.write(log + "\n")


if __name__ == "__main__":
    files = os.listdir()
    log_files = []
    for file in files:
        print(file[:4])
        if file[-4:] == ".log" and file[:6] == "secure":
            log_files.append(file)
    print(log_files)
    tool = LogFileTool("log_ctgs.json",log_files)
    tool.info_ctg()
    tool.write_no_matches("test1")


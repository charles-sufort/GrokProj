import sys
import json

class GrokManager:
    def __init__(self):
        self.data_dir = "../data"

    def get_logs(self,logfile,ctg):
        file = "{}/{}/log_ctgs/{}.log".format(self.data_dir,logfile,ctg)
        logs = []
        with open(file,"r") as fo:
            for line in fo:
                logs.append(line[:-1])
        return logs

    def get_patterns(self,logfile,ctg):
        patterns = []
        file = "{}/{}/ctg_patterns.json".format(self.data_dir,logfile)
        with open(file,"r") as fo:
            ctg_obj = json.load(fo)
        for pattern_obj in ctg_obj[ctg]:
            patterns.append(pattern_obj["pattern"])
        return patterns

    def get_non_empty_ctgs(self,logfile):
        file = "{}/{}/ctg_patterns.json".format(self.data_dir,logfile)
        ctgs = []
        with open(file,"r") as fo:
            ctg_obj = json.load(fo)
        for ctg in ctg_obj:
            if len(ctg_obj[ctg]) != 0:
                ctgs.append(ctg)
        return ctgs



        

if __name__ == "__main__":
    gm = GrokManager()
    print(gm.get_non_empty_ctgs("secure"))
    #print(gm.get_logs("secure","sshd_disconnected_from"))
    #print(gm.get_patterns("secure","sshd_disconnected_from"))

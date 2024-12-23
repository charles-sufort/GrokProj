import sys
import json

class GrokManager:
    def __init__(self):
        self.data_dir = "../data"

    def get_logs(self,logfile,ctg):
        file = "{}/{}/{}.log".format(self.data_dir,logfile,ctg)
        logs = []
        with open(file,"r") as fo:
            for line in fo:
                logs.append(line[:-1])
        return logs

    def get_patterns(self,logfile,ctg):

        patterns = []
        file = "{}/{}/{}_patterns.json".format(self.data_dir,logfile,logfile)
        with open(file,"r") as fo:
            ctg_obj = json.load(fo)
        for pattern_obj in ctg_obj[ctg]:
            patterns.append(pattern_obj["pattern"])
        return patterns

        

if __name__ == "__main__":
    gm = GrokManager()
    print(gm.get_logs("secure","sshd_disconnected"))
    print(gm.get_patterns("secure","sshd_disconnected"))

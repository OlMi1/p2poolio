# the payout variable always holds the most recent one
# i am a cluttered mess written in like 10 minutes, so don't be too harsh :)

# View readme.md for more info & syntax

import time
import datetime
import os

class P2PoolIO:
    def read(path: str = "p2pool.log", returnLines: bool = False, linelimit: int = 100):
        starttime = time.time()

        if (not os.path.exists(path)):
            raise Exception(f'The given path does not exist! Check for {os.path.abspath(os.getcwd())}\{path}')
        
        lines = []
        payout = {}

        possibleTags = ["INFO", "WARN", "ERROR", "FATAL", "DEBUG", "TRACE", "NOTICE"] # thx copilot

        with open(path, "r") as f:
            # Read the file in reverse and add each line to the list
            for line in reversed(f.readlines()):
                if (len(lines) < linelimit):
                    line = line.replace("\n", "").replace("  ", " ")

                    # READ AND CATEGORIZE (and declutter)
                    splits = line.split(" ")

                    type = splits[0]
                    if (type not in possibleTags):
                        continue
                    timestamp = int(time.mktime(datetime.datetime.strptime(
                        f'{splits[1]} {splits[2].split(".")[0]}', "%Y-%m-%d %H:%M:%S").timetuple()))
                    module = splits[3]
                    line = " ".join(splits[4:])

                    # Your wallet ... didn't get a payout in block 2814592 because you had no shares in PPLNS window
                    # Your wallet ... got a payout of 0.12345 XMR in block 2820000
                    hasPayout: bool = (module == "P2Pool" and line.startswith("Your wallet") and "got a payout" in line and not "no shares" in line and payout == {}) 
                    payoutdata = {
                        "payout": hasPayout
                    }

                    if (hasPayout):
                        payoutdata["amount"] = line.split("got a payout of ")[1].split(" ")[0]

                    added = {
                        "type": type,
                        "timestamp": timestamp,
                        "module": module,
                        "payout": payoutdata,
                        "content": line
                    }
                    lines.append(added)

                    if (hasPayout):
                        payoutdata["timestamp"] = timestamp
                        del(payoutdata["payout"])
                        payout = payoutdata
                else:
                    break

        returndata = {
            "payout": payout,
            "time": time.time() - starttime,
        }

        if (returnLines):
            returndata["lines"] = lines

        return returndata


import json
print(json.dumps(P2PoolIO.read()))

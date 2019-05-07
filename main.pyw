import os, time
import ruamel_yaml

yaml = ruamel_yaml.YAML()

def getConfig():
    with open("./config.yaml", "r") as f:
        data = yaml.load(f)
    region = data["region"]
    size = (data["size"]["width"], data["size"]["height"])
    path = data["path"]
    command = f'mode con: cols={size[0]} lines={size[1]}'
    return region, command, path

def latestLoL():
    region, command, leaguePath = getConfig()

    #Get the system.yaml FILE.
    leaguePath += "\\RADS\\projects\\league_client\\releases\\"
    try:
        files = os.listdir(leaguePath)
        paths = [os.path.join(leaguePath, basename) for basename in files]
        yamlFile = max(paths, key=os.path.getctime)+'\\deploy\\system.yaml'
        with open(yamlFile) as f:
            data = yaml.load(f)
  
        #Modify it.
        try:
            if data["region_data"][region]["servers"]["chat"]["chat_port"] == 5224:
            
                data["region_data"][region]["servers"]["chat"]["chat_port"] = 5223
                os.system(f'{command} && ECHO You will appear connected on League of Legends. & color 0A & TITLE Chat ON && ping 127.0.0.1 -n 3 > nul')
            else:
            
                data["region_data"][region]["servers"]["chat"]["chat_port"] = 5224
                os.system(f'{command} && ECHO You will appear disconnected on League of Legends. & color 04 & TITLE Chat OFF && ping 127.0.0.1 -n 3 > nul')
                
        except:
            os.system(f'{command} && ECHO An ERROR has occurred. & color 40 & TITLE ERROR && ping 127.0.0.1 -n 3 > nul')

        with open(yamlFile, "w") as f:
            yaml.dump(data, f)

    except:
        os.system(f'{command} && ECHO Error: Wrong LoL Path. & color 40 & TITLE ERROR && ping 127.0.0.1 -n 3 > nul')
    
if __name__ == "__main__":
    latestLoL()

import datetime
import os
import time
from pathlib import Path


def append_log(configuration, refined_clustering):
    dir_path = str(Path(__file__).parent.parent) + "/log"
    Path(dir_path).mkdir(exist_ok=True)
    os.chdir(dir_path)
    file_path = dir_path + "\\log.log"
    tiny_json = configuration.get_as_json_tiny()
    f = open(file_path, mode="a", encoding='UTF-8')
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    type = "Refined Clustering" if refined_clustering else "Simple Clustering"
    text = "{\n" + "\"timestamp\": \"" + timestamp + "\",\n" + "\"type\": \"" + type + "\",\n" + "\"configuration\":\n" + tiny_json + "\n},\n"
    f.write(text)
    f.close()
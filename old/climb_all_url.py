from urllib.request import urlopen,HTTPError,URLError
import os
import pickle
# open the jar
all_url_file = open(
    "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\all_url.pkl", "rb")

url = pickle.load(all_url_file)  # Take the pickles out of the jar

n = 0
for each_url in url:
    try:
        req = urlopen(each_url)
        all_url_data = req.read()
        pickle_file = open(
            "D:\\Users\\YeahKun\\Desktop\\TDcup\\data process\\all_url_data.pkl", "ab")
        pickle.dump(all_url_data,pickle_file)
        pickle_file.close()
        n += 1
        print(n)
    except (HTTPError,ConnectionResetError,URLError)  as reason:
        print(reason)
        pickle_file.close()
        continue
all_url_file.close()

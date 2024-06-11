'''*** 可以比較Lab1和Lab2，看看直接抓取資料跟透過Kafka 抓取資料的差別'''
import json
from kafka import KafkaConsumer #似乎只有3.10的直譯器版本可以成功使用
import chardet

#先開啟config取得config.json的編碼方式(變數encoding)
with open('config.json', 'rb') as file:
    raw_data = file.read()
    result = chardet.detect(raw_data)
    encoding = result['encoding']

with open("config.json","r",encoding=encoding) as f:
    config:dict = json.load(f) #看不懂的用法
    #config = json.load(f)

consumer = KafkaConsumer(config["topic"],                       #指定接收訊息的topic
                         bootstrap_servers = config["server"],  #導入server為config中設定好的server
                         consumer_timeout_ms = 100000,          #設定待機多久關閉
                         auto_offset_reset = 'earliest')
#從producer取得資料
#偵錯:json.JSONDecodeError
for msg in consumer:
    try:
        #此處印出檢查的文字僅會在batch檔中顯示，不會被consumer接收
        message_str = msg.value.decode(encoding)    #以跟producer編碼相同的編碼方式做解碼，以確保能接收到正確的消息。
        #print(f"Message value: {message_str}")
        if not message_str.strip():                 # 檢查消息是否為空
            print("Received empty message")
            continue
        data = json.loads(message_str)              #寫檔
#        print("data:",data)  # 打印解碼後的消息
        print()
    except UnicodeDecodeError as e:
        print(f"Unicode decode error: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print(f"Message value: {msg.value}")

#處理接收到的資料
sor = data["sor"]
rtns = data["rtns"]

print("start writing data to json file")
#寫入資料為json檔
with open("./data/route.json",'w') as f:
    json.dump(sor, f)
with open("./data/location.json",'w') as f:
    json.dump(rtns, f)
print("finish writing data to json file")
print("finish consumer.py")
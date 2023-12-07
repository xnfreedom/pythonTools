import pandas as pd
import time
import random
import requests
import hashlib

df = pd.read_csv('C:\\Users\\cqcxn\\Downloads\\PTE_WORDS_Level2.csv')
df_new = pd.DataFrame()

def procFun(x):
    # 在这里进行你的处理
    return str(x)+"ha"

appid = '20231128001894612'

secretKey = 'dlx2rd0GtHtNiP_JOUnK'

def get_md5(string):  # 返回字符串md5加密
        hl = hashlib.md5()
        hl.update(string.encode('utf-8'))
        return hl.hexdigest()
def en_to_zh(en_str):  # 英语翻译成中文
    api_url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    #appid = 'xxx'
    #secretKey = 'xxxx'
    salt = random.randint(32768, 65536) # 这个不知道是为啥
    sign =get_md5(appid + en_str + str(salt) +secretKey)
    api_data = {
        'q': en_str,
        'from': 'en',
        'to': 'zh',
        'appid': appid,
        'salt': salt,
        'sign': sign
    }
    req_get = requests.get(api_url, api_data)
    result = req_get.json()
    print(result)
    return result
    
#print(en_to_zh("hello")['trans_result'])
#print(en_to_zh("hello")['trans_result'][0]['dst'])

# 设置一个标志，以便我们知道是否是第一次写入
first_time = True

# 遍历每一列
for col in df.columns:
    # 创建一个临时的Series来存储处理后的数据
    processed_series = pd.Series()

    # 对每一列的数据进行处理，遇到空数据则停止处理
    for i, val in enumerate(df[col]):
        if pd.isnull(val):
            break
        processed_series.at[i] = en_to_zh(val)['trans_result'][0]['dst'] 
        time.sleep(1.5)

    # 将原始数据和处理后的数据存储在新的DataFrame中
    df_new[col+'_original'] = df[col]
    df_new[col+'_processed'] = processed_series

    # 根据是否是第一次写入来决定是否写入列名
    if first_time:
        df_new.to_csv('C:\\Users\\cqcxn\\Downloads\\PTE_WORDS_Level2_translated.csv', mode='a', index=False)
        first_time = False
    else:
        df_new.to_csv('C:\\Users\\cqcxn\\Downloads\\PTE_WORDS_Level2_translated.csv', mode='a', index=False, header=False)

    # 清除df_new以便处理下一列
    df_new = pd.DataFrame()

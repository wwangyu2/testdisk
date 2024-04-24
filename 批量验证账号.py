import requests
from bs4 import BeautifulSoup
from requests.utils import dict_from_cookiejar
import json
import threading
from concurrent.futures import ThreadPoolExecutor
import os
import re



def arkoseToken():
    response = requests.get('https://raw.githubusercontent.com/wwangyu2/test-action/main/arkoseToken.txt')
    
    response_text = response.text.split('\n')  # 将多行文本拆分成行
    json_data = [json.loads(line) for line in response_text if line.strip()]  # 解析每行JSON数据并丢弃空行
    return json_data



def accounts():
    # 获取当前脚本所在的目录路径
    accounts_file = "账号.txt"

    # 读取账号文件并将账号存入列表
    with open(accounts_file, "r", encoding="utf-8") as file:
        accounts = file.readlines()
    
    # 移除账号后的换行符
    accounts = [account.strip() for account in accounts]

    return accounts




def create_directory(directory):
    """Create directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)

# 定义一个全局变量，用于统计获取到 session_token 的次数
session_token_total_count = 0



def process_proxy(account,arkoseToken):
    global session_token_total_count  # 声明要使用的全局变量

    # print(type(account)) 
    # print(account)

    username, password = account.strip().split(':', 1)
    
    # 获取arkoseToken的值
    arkose_token = arkoseToken.get('arkoseToken')

    # print(arkose_token)

    # 构建cookies字典
    cookies = {
        'xy-arkose-session': 'dnedte03rz9p10d0sb8467z6h7dhc936',
        'cf_clearance': 'AVIpuqFmeT18dq.fu3KzVRm_IyhTrrtawV2j2IeGyhE-1713965730-1.0.1.1-bWE5tiv5NttQySvK5eKAj3pOW34z5g6IVuDOOKfdxCPNWoQkQ0em5XmP5eWytVu79Qh3fFVXfbcJCMWeiKEFYw',
        'oai-did': '05f3e593-0e07-43ec-be13-fd3371936c6a',
        '_dd_s': 'rum=0&expire=1713961579787',
        'lb-session': '1sy3y5z1000d0sccr3pq19apm04fvlzx',
        'timestamp': '1713960683870',
        'arkoseToken': arkose_token,
    }

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'cache-control': 'max-age=0',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'xy-arkose-session=dnedte03rz9p10d0sb8467z6h7dhc936; cf_clearance=6vpxM9oiwzbm_A7bzoxgH5BuQ0uVjn1D9pzhwe_VWvc-1713959343-1.0.1.1-n6OmFij5EramA4mGP8sngOgEbzov4C8ueOP6scW4gG5XMahmeYnb12lfwko8hwCvpGnFon_2oBCMM3TmcKlptg; oai-did=05f3e593-0e07-43ec-be13-fd3371936c6a; _dd_s=rum=0&expire=1713961579787; lb-session=1sy3y5z1000d0sccr3pq19apm04fvlzx; timestamp=1713960683870; arkoseToken=85617c9362c41acd3.3742436301|r=us-east-1|meta=3|metabgclr=transparent|metaiconclr=%23757575|guitextcolor=%23000000|pk=0A1D34FC-659D-4E23-B17B-694DCFCF6A6C|at=40|sup=1|rid=14|ag=101|cdn_url=https%3A%2F%2Ftcr9i.openai.com%2Fcdn%2Ffc|lurl=https%3A%2F%2Faudio-us-east-1.arkoselabs.com|surl=https%3A%2F%2Ftcr9i.openai.com|smurl=https%3A%2F%2Ftcr9i.openai.com%2Fcdn%2Ffc%2Fassets%2Fstyle-manager',
        'origin': 'https://chat.rawchat.cc',
        'priority': 'u=0, i',
        'referer': 'https://chat.rawchat.cc/login',
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"124.0.6367.61"',
        'sec-ch-ua-full-version-list': '"Chromium";v="124.0.6367.61", "Google Chrome";v="124.0.6367.61", "Not-A.Brand";v="99.0.0.0"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"19.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }

    data = {
        'username': username,
        'password': password,
    }
    
    try:
        response = requests.post('https://chat.rawchat.cc/login', cookies=cookies, headers=headers, data=data, timeout=15)
        response.encoding = 'utf8'

        # 解析响应
        soup = BeautifulSoup(response.text, 'html.parser')

        # 检查选择器是否存在
        error_elements = soup.select('#error-element-password.ulp-input-error-message[data-error-code="wrong-email-credentials"]')
        # 如果存在，打印出错误元素的文本
        if error_elements:
            for element in error_elements:
                print(element.text.strip())  # .strip() 用来移除字符串开头和结尾的空格
        else:
            print("No Error Element Found!")

            print(response.status_code)

            cookies_dict = dict_from_cookiejar(response.cookies)
            session_token = cookies_dict.get('session-token')
            if session_token:
                
                filename_suffix = re.sub(r'\W+', '', username)
                folder_name = "账号数据"
                create_directory(folder_name)
                filename = os.path.join(folder_name, f"{filename_suffix}.txt")

                # Write account details and session token to file
                with open(filename, "w", encoding="utf-8") as outfile:
                    outfile.write(f"Email: {username}\n")
                    outfile.write(f"Password: {password}\n" + "\n" * 4)
                    outfile.write(f"Session Token: {session_token}\n")
                
                # 打印键值对
                print(f"{username}: {session_token}")

                session_token_total_count += 1  # 增加 session_token 计数器

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    global session_token_total_count  # 声明要使用的全局变量
    
    arkoseToken_list = arkoseToken()
    accounts_list = accounts()

    with ThreadPoolExecutor(max_workers=50) as executor:
        # 提交每个代理的处理任务给线程池
        futures = [executor.submit(process_proxy, account, arkoseToken) for account, arkoseToken in zip(accounts_list, arkoseToken_list)]
        
        # 等待所有任务完成
        for future in futures:
            future.result()

    print(f"Total session_token count: {session_token_total_count}")

if __name__ == "__main__":
    main()

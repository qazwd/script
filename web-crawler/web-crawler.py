import requests

def get_url(target_url):
    url = f'{target_url}'
    return url

def get_headers(User_Agent=None,
                Cookie=None,
                src_url=None,
                Accept=None,
                Accept_Encoding=None,
                Host=None,
                Connection=None,
                Authorization=None,
                Content_Type=None):
    headers = {
        # 主要
        "User-Agent": f"{User_Agent}",            # 标识客户端类型
        "Cookie": f"{Cookie}",                    # 存储用户登陆状态、会话信息
        "Referer": f"{src_url}",                  # 标识请求的来源页面 URL
        "Accept": f"{Accept}",                    # 声明客户端可接收的数据格式
        "Accept-Encoding": f"{Accept_Encoding}",  # 声明支持的压缩方式
        # 次要
        "Host": f"{Host}",                        # 指定目标服务器的 域名/IP
        "Connection": f"{Connection}",            # 控制连接状态
        "Authorization": f"{Authorization}",      # 用于身份验证
        "Content-Type": f"{Content_Type}"         # 指定请求体的数据格式（仅 POST/PUT）等请求需设置
    }
    return headers

def get_params(page=None, 
               size=None, 
               keyword=None, 
               sort=None):
    params = {
        "page": page,
        "size": f"{size}",
        "keyword": f"{keyword}",
        "sort": f"{sort}"
    }
    return params

def get_data(uid=None, name=None):
    data = {
        "id": f"{uid}",
        "name": f"{name}"                           
    }
    return data

def get_json(uid=None, name=None):
    json={
        "id": f"{uid}",
        "name": f"{name}"                           
    }
    return json

def get_timeout(timeout=None):
    return timeout

def get_method(method=None):
    return method

def get_datas(url, data, json, print_data=False):
    data_list = []
    offset = 0

    while True:
        
        # 复制参数模板并更新偏移量
        payload = json.copy()
        #payload["offset"] = data.get("offset", 0)  # 分页参数
        payload["offset"] = offset  # 分页参数

        try:
            response = requests.post(url, data=data, json=payload)
            print("\n状态码\n:", response.status_code)
            response.raise_for_status()
            data = response.json()
            data_list.append(data)

            if print_data:
                print("Response Data:\n", data)

            # 更新偏移量，准备下一页请求
            offset += payload["limit"]
            print(f"当前偏移量: {offset}")  # 打印当前偏移量，方便调试

        except requests.exceptions.RequestException as e:
            print(f"请求失败: {e}")
            break
        except ValueError:
            print("无法解析 JSON 数据")
            print("响应内容:", response.text)
            break

    return data_list

def get_target_data(data_list, target_key):
    target_data = []
    
    # 提取目标数据
    if not data_list:
        print("数据列表为空")
        return None
    if target_key not in data_list[0]:
        print(f"目标键 '{target_key}' 不存在于数据中")
        return None
    if isinstance(data_list[0], dict):
        print("数据列表中的元素不是字典类型")
        return None
    
    target_data = data_list[0][target_key]
    
    for data in data_list:
        target_data.append(data[target_key])
    return target_data


if __name__ == "__main__":
    # 目标 API 的 URL
    target_url = ""

    # 定义请求头，需将 Cookie 替换为你实际获取的值
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
        "Referer": "https://pultegroup.wd1.myworkdayjobs.com/PGI",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Cookie": "PLAY_SESSION=69754d440e1ffdb99d6fa1ee6d28fbf646ad13ec-pultegroup_pSessionId=1j8sbv2jq1b8u4tu5t7v19fv9b&instance=vps-prod-q8l6shqa.prod-vps.pr502.cust.ash.wd; wd-browser-id=c66bb49e-6724-4bbe-a1cf-30ea98b27723; CALYPSO_CSRF_TOKEN=3818714c-b803-4acf-8c42-eb5cebf5f828; wday_vps_cookie=3027859466.53810.0000; __cflb=0H28vCu5mZQ5H5URQ4Xbzh7qZvE1AhPv4cCdydLaiLU; _cfuvid=lnSj2m60duwovxpmobgDD6xZr.a2s_lmvkjMslLBx3A-1753666594749-0.0.1.1-604800000; timezoneOffset=-480; __cf_bm=yNr6MxQxAYd9IJ.8fNL7m7uVR8t2terzF8zJuV63GUs-1753668866-1.0.1.1-wLD9k1E5Xj_z.i1wEfYt8Kijm6P_Zq6sQlrMuuPawu5Vqns4ii4wdxlax3fPZrW.Xa9zkHuM74cuv9hTymcGFVzD9dVlbmuljhPWqAIMqHs"  # 替换为实际的 Cookie
    }

    # 定义请求参数模板
    payload_template = {
        "appliedFacets": {},
        "limit": 20,
        "offset": 0,
        "searchText": ""
    }

    # 定义目标键
    target_key = "data"

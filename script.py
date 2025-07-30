import requests
import csv
from display import TimeTracer

# 目标 API 的 URL
api_url = "https://pultegroup.wd1.myworkdayjobs.com/wday/cxs/pultegroup/PGI/jobs"

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

def get_job_listings():
    all_jobs = []
    offset = 0

    while True:
        # 复制参数模板并更新偏移量
        payload = payload_template.copy()
        payload["offset"] = offset

        try:
            # 发送 POST 请求，将参数以 JSON 格式放在请求体中
            response = requests.post(api_url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

            # 打印响应数据，方便调试
            print("Response Data:", data)

            # 提取职位列表数据
            job_postings = data.get("jobPostings", [])
            if not job_postings:
                break

            for job in job_postings:
                job_name = job.get("title", "N/A")
                location = job.get("locationsText", "N/A")
                job_url = f"https://pultegroup.wd1.myworkdayjobs.com{job.get('externalPath', 'N/A')}"
                new_job = {
                    "Job_name": job_name,
                    "Location": location,
                    "URL": job_url
                }
                # 检查新职位是否已存在
                if new_job not in all_jobs:
                    all_jobs.append(new_job)

            # 更新偏移量，准备下一页请求
            offset += payload["limit"]
            print(f"当前偏移量: {offset}")  # 打印当前偏移量，方便调试

        except requests.RequestException as e:
            print(f"请求出错: {e}")
            print("请求 URL:", api_url)
            print("请求头:", headers)
            print("请求体:", payload)
            break
        except ValueError:
            print("无法解析 JSON 数据")
            print("响应内容:", response.text)
            break

    return all_jobs

def save_to_csv(data, filename):
    if data:
        keys = data[0].keys()
        with open(filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)
        print(f"共 {len(data)} 条数据已保存到 {filename}")
    else:
        print("没有数据可保存。")

def main():
    all_jobs = get_job_listings()
    save_to_csv(all_jobs, "job_data.csv")

if __name__ == "__main__":
    with TimeTracer() as time_tracer:
        print("开始爬取数据...")
        main()
        print("数据爬取完成。")

import requests

def baidu_search(query, region, ak):
    url = 'http://api.map.baidu.com/place/v2/search'
    params = {
        'query': query,  # 搜索关键词
        'region': region,  # 搜索区域
        'output': 'json',  # 返回格式
        'ak': ak,  # API 密钥
        'page_size': 20,  # 每页结果数量
        'page_num': 0  # 页码
    }

    all_results = []

    while True:
        # 发送请求
        response = requests.get(url, params=params)
        response_dict = response.json()

        # 检查请求是否成功
        if response_dict.get('status') != 0:
            print(f"请求失败，状态码: {response_dict.get('status')}")
            print(f"错误信息: {response_dict.get('message')}")
            break

        # 提取结果
        results = response_dict.get('results', [])
        if not results:
            break  # 如果没有更多结果，退出循环

        # 将结果添加到列表中
        all_results.extend(results)

        # 更新页码
        params['page_num'] += 1

    return all_results

def get_waitan_info(ak):
    # 搜索杭州地区的外婆家门店
    query = '外婆家'
    region = '杭州'
    results = baidu_search(query, region, ak)

    # 打印门店信息
    for result in results:
        name = result.get('name')
        location = result.get('location', {})
        lat = location.get('lat')
        lng = location.get('lng')
        address = result.get('address')
        print(f"名称: {name}")
        print(f"坐标: {lat}, {lng}")
        print(f"地址: {address}")
        print("-" * 40)

if __name__ == "__main__":
    ak = 'API密钥'  # 替换为你的有效 API 密钥
    get_waitan_info(ak)
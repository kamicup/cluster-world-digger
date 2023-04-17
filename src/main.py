import requests
import csv
import time
import datetime


def load(page=1):
    url = 'https://api.cluster.mu/v1/worlds/search/func:LatestWorld?page={}'.format(page)

    headers = {
        'authority': 'api.cluster.mu',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ja',
        'origin': 'https://cluster.mu',
        'referer': 'https://cluster.mu/',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
        'x-cluster-app-version': '2.70.2304101300',
        'x-cluster-build-version': '35534',
        'x-cluster-device': 'Web',
        'x-cluster-platform': 'Web',
        'accept-encoding': 'gzip, deflate, br'
    }

    response = requests.get(url, headers=headers)

    # レスポンスの内容を取得する
    content = response.json()

    return content


def flatten(worlds):
    items = []
    for item in worlds:
        items.append([
            item['webUrl'],
            "{:.2f}".format(item['likeCount'] / item['playCount']) if item['playCount'] else 0,
            item['likeCount'],
            item['playCount'],
            item['name'],
            item['privacyType'],
            item['allowEvent'],
            item['category'],
            item['sdkType'],
            item['venueSize'],
            item['venueCreatedAt'],
            item['venuePublishedAt'],
            item['venueUpdatedAt'],
            # item['description'],
            item['creator']['shareUrl'],
            item['creator']['displayName'],
            item['creator']['username'],
            item['creator']['isBeginner'],
            item['creator']['isCertified'],
            item['creator']['isDeleted'],
        ])
    return items


# メイン処理
def main():
    # TSV形式で出力する

    formatted_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = "{}.tsv".format(formatted_time)

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter='\t')

        expected_total = 500000
        items_per_page = 24
        for page in range(1, int(expected_total/items_per_page)):
            content = load(page)

            page_data = content['pageData']
            worlds = content['worlds']

            # print(json.dumps(worlds, indent=4))

            items = flatten(worlds)
            writer.writerows(items)

            print(page_data)
            time.sleep(2)


# メイン処理の実行
if __name__ == '__main__':
    main()

import csv
import datetime
import time

import requests


def get_json(url):
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
    content = response.json()
    return content


def search_latest_world(page=1):
    url = 'https://api.cluster.mu/v1/worlds/search/func:LatestWorld?page={}'.format(page)
    return get_json(url)


def users_profile(username):
    url = 'https://api.cluster.mu/v1/users/profile/{}'.format(username)
    return get_json(url)


def events_created_by(user_id):
    url = 'https://api.cluster.mu/v1/events?createdBy={}'.format(user_id)
    return get_json(url)


def user_friends(user_id):
    url = 'https://api.cluster.mu/v1/user_friends/{}'.format(user_id)
    return get_json(url)


def worlds_created_by(user_id):
    url = 'https://api.cluster.mu/v1/worlds?createdBy={}'.format(user_id)
    return get_json(url)


class ClusterWorldSearch:
    def __init__(self):
        self.profile_cache = {}

    def get_profile(self, user_id):
        if user_id in self.profile_cache:
            return self.profile_cache[user_id]

        time.sleep(1)
        if user_id:
            events = events_created_by(user_id)['events']
            friends = user_friends(user_id)['users']
            worlds = worlds_created_by(user_id)['worlds']
            num_events = len(events)
            num_friends = len(friends)
            num_worlds = len(worlds)
        else:
            num_worlds = num_events = num_friends = None

        value = (num_events, num_friends, num_worlds)
        self.profile_cache[user_id] = value
        return value

    def save_tsv(self, filename):
        with open(filename, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter='\t')

            max_num_worlds = 50000
            items_per_page = 24
            max_page = int(max_num_worlds / items_per_page)
            for page in range(1, max_page):
                content = search_latest_world(page)

                page_data = content['pageData']
                worlds = content['worlds']

                if len(worlds) == 0:
                    break

                for item in worlds:
                    (num_events, num_friends, num_worlds) = self.get_profile(item['creator']['userId'])

                    row = [
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
                        num_worlds,
                        num_events,
                        num_friends,
                    ]
                    csv_writer.writerow(row)
                    print(row)
                    csv_file.flush()

                print(page_data)
                time.sleep(1)


# メイン処理
def main():
    formatted_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = "{}.tsv".format(formatted_time)

    ClusterWorldSearch().save_tsv(filename)


# メイン処理の実行
if __name__ == '__main__':
    main()


import requests


def get_post(sr):
    url = f'https://www.reddit.com/r/{sr}/random.json'
    headers = {'User-Agent': 'Mozilla/5.0'}
    res = requests.get(url, headers=headers)
    response = res.json()  # Directly get the JSON response
    return response


if __name__ == "__main__":
    sr = "AmItheAsshole"
    post = get_post(sr)
    print(post["data"]["children"][1]["data"]["selftext"])

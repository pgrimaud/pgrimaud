import requests
import urllib.request
import image2image as im

url = 'https://api.github.com/repos/pgrimaud/pgrimaud/stargazers'


def get_stargazers_from_api(api_url, start_page):
    # Without an API key in the params, you are limited to 50 API calls per hour
    params = {'format': 'json', 'page': start_page, 'per_page': 100}
    response = requests.get(url=api_url, params=params)
    return response.json()


def get_all_users():
    page = 1
    avatars = []

    has_results = get_stargazers_from_api(url, page)
    while has_results:
        for result in has_results:
            avatars.append(result['avatar_url'] + '&s=30')
        print('Got page ' + str(page) + ' of stargazers')
        page += 1
        has_results = get_stargazers_from_api(url, page)

    return avatars


def download_avatars():
    counter = 1
    for avatar in get_all_users():
        urllib.request.urlretrieve(avatar, './avatars/avt' + str(counter) + '.png')
        counter += 1


if __name__ == '__main__':
    print('Starting script')
    download_avatars()
    print('Avatars have been downloaded')
    im.main(im.get_args())
    print('Output has been created')

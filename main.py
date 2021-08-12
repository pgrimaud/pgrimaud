import cv2
import glob
import image2image as im
import imageio
import os
import requests
import urllib.request

# install dependencies with pip3 (pip3 install -r requirements.txt)

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
            avatars.append({
                'avatar' : result['avatar_url'] + '&s=30',
                'username' : result['login']
            })
        print('Got page ' + str(page) + ' of stargazers')
        page += 1
        has_results = get_stargazers_from_api(url, page)

    return avatars


def download_avatars():
    counter = 1
    for user in get_all_users():
        urllib.request.urlretrieve(user['avatar'], './tmp/avatars/' + str(user['username']) + '.png')

        filename = 'tmp/steps/step' + format_counter_for_sort(counter) + '.jpg'
        filename_rsz = 'tmp/steps_resize/step' + format_counter_for_sort(counter) + '.jpg'

        # create temporary mosaic for GIF
        im.main(im.get_args(filename))

        # resize picture
        image = cv2.imread(filename, cv2.IMREAD_COLOR)
        image = cv2.resize(image, (702, 318), 0, 0, cv2.IMREAD_COLOR)
        cv2.imwrite(filename_rsz, image)

        counter += 1


def format_counter_for_sort(number):
    if number < 10:
        return '00' + str(number)
    elif number < 100:
        return '0' + str(number)


def generate_gif():
    # fetch all steps
    frames = []

    images = glob.glob('{}/*.jpg'.format('tmp/steps_resize'))
    images.sort()

    for image in images:
        frames.append(imageio.imread(image))

    # generate GIF
    imageio.mimsave('./data/output.gif', frames, format='GIF', duration=0.1)


def clean_data():
    for image in glob.glob('{}/*.jpg'.format('tmp/steps')) + glob.glob('{}/*.jpg'.format('tmp/steps_resize')) + glob.glob('{}/*.png'.format('tmp/avatars')):
        os.remove(image)

def write_statistics(statistics):
    output = '#Statistics\n\n'
    # write header
    output = output + '|Username|Times used|\n|--------|:--------:|\n'

    for usage in statistics:
        output = output + '|@' + (usage[0]) + '|' + str(usage[1]) + '|\n'

    # write on README.md
    file = open('STATISTICS.md', 'w+')
    file.write(output)
    file.close()

if __name__ == '__main__':
    print('Clean data')
    clean_data()
    print('Starting script')
    download_avatars()
    print('Avatars have been downloaded')
    statistics = im.main(im.get_args())
    print('Output picture has been created')
    write_statistics(statistics)
    print('Statistics have been created')
    generate_gif()
    print('Output GIF has been created')

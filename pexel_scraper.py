##
import os
import requests
from pexels_api import API
import argparse
import tqdm

##
PEXELS_API_KEY = "#"  # insert your api key in here
NUMBER_OF_PHOTOS_PER_PAGE = 80
PAGE_LIMIT = 5


def main(args):
    page = 1
    api = API(PEXELS_API_KEY)

    photo_dict = {}

    # Getting URLs and meta information

    while page < PAGE_LIMIT:
        api.search(args.query, page=page, results_per_page=NUMBER_OF_PHOTOS_PER_PAGE)
        photos = api.get_entries()

        for photo in tqdm.tqdm(photos):
            photo_dict[photo.id] = vars(photo)["_Photo__photo"]

            if not api.has_next_page:
                break

        page += 1

    # Downloading Images

    if photo_dict:
        os.makedirs(args.path, exist_ok=True)

        for value in tqdm.tqdm(photo_dict.values()):
            urls = value["src"][args.resolution]
            file_name = os.path.basename(value["src"]["original"])
            file_path = os.path.join(args.path, file_name)

            if not os.path.isfile(file_path):
                response = requests.get(urls, stream=True)

                with open(file_path, "wb") as f:
                    f.write(response.content)
            else:
                print(f'file {file_path} exist')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--query',
        type=str,
        required=True
    )
    parser.add_argument(
        '--resolution',
        choices=[
            'original', 'large', 'large2x', 'medium', 'small'
        ],
        default='original',
    )
    parser.add_argument(
        '--path',
        default='./pexels_images'
    )
    args = parser.parse_args()
    main(args)

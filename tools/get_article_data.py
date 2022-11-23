import os.path

import jsonlines
import pandas as pd
import re
from dotenv import load_dotenv
from os import getenv
from tqdm import tqdm


# load env
load_dotenv()
# jsonl article file path
TRAIN_ARTICLE_PATH = getenv('TRAIN_ARTICLE_PATH')
TEST_ARTICLE_PATH = getenv('TEST_ARTICLE_PATH')
VAL_ARTICLE_PATH = getenv('VAL_ARTICLE_PATH')
# article folder path
ARTICLE_FOLDER_PATH = getenv('ARTICLE_FOLDER_PATH')


def remove_emoji(text):
    return re.sub(r'[^A-Za-z0-9.,?!@#$^&*(){};:%`\n\"\' ]', '', text)


def get_article_data(file_path):
    categories = []
    texts = []
    regex = re.compile('{}(.*){}'.format(re.escape('_'), re.escape('.')))
    file_name = regex.findall(file_path)[0]
    file_directory = ARTICLE_FOLDER_PATH + '/{}'.format(file_name)

    with jsonlines.open(file_path) as f:
        for line in tqdm(f):
            categories.append(re.sub(r'[^A-Za-z-]', '', line['id'])[:-1])
            texts.append(remove_emoji(line['text']))

    article_df = pd.DataFrame({'category': categories, 'text': texts})

    try:
        if not os.path.exists(file_directory):
            os.makedirs(file_directory)
            article_df.to_csv(file_directory+'/{}.csv'.format(file_name, file_name), index=False)
    except OSError:
        print("Error: Failed to create the directory")


def main():
    file_list = [TRAIN_ARTICLE_PATH, TEST_ARTICLE_PATH, VAL_ARTICLE_PATH]
    [get_article_data(file_path) for file_path in file_list]


if __name__ == "__main__":
    main()

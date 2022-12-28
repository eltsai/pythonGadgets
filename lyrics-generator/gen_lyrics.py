"""
Generate Chinese Lyrics with Pinyin
"""

from pypinyin import pinyin, lazy_pinyin, Style
import jieba

jieba.enable_paddle()


def read_lyrics_from_txt(filename:str)->list:
    with open(filename, 'r') as f:
        return list(filter(None, [line.strip().replace('\u200b', '') for line in f.readlines()]))


lyrics_list = read_lyrics_from_txt('lyrics.txt')
for line in lyrics_list:
    print(' '.join([x[0] for x in pinyin(line)]))
    seg_list = jieba.cut(line,use_paddle=True)
    print(' '.join(list(seg_list)))
    
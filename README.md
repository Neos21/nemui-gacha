# nemui-gacha : ねむいガチャ

「 `任意の単語 + ガチャ` 」を渡すと、ランダムに否定形を返したり、そのままの文言を返したりする。

- 例
    - 「ねむいガチャ」を渡した場合 → 「ねむい」or「ねむくない」
    - 「飲み会やるガチャ」を渡した場合 → 「飲み会やる」or「飲み会やらない」


## Installation

### Docker を使用しない場合

予め以下をインストールしておく。

- [MeCab](https://taku910.github.io/mecab/)
- [mecab-ipadic-NEologd](https://github.com/neologd/mecab-ipadic-neologd)
- [Python 3](https://www.python.org/)

```sh
# 環境構築
$ pip install pipenv
$ pipenv install --dev

# 実行する
$ pipenv run cli 'ねむいガチャ'
# → 'ねむい' or 'ねむくない'
```

### Docker を使用する場合

```sh
# 環境構築 (Docker イメージは 4.79GB 程度になる)
$ docker-compose up -d
$ docker exec nemui-gacha pipenv install --dev

# 実行する
$ docker exec nemui-gacha pipenv run cli 'ねむいガチャ'
# → 'ねむい' or 'ねむくない'
```


## Author

[Neo](http://neo.s21.xrea.com/)


## Links

- [Neo's World](http://neo.s21.xrea.com/)
- [Corredor](https://neos21.hatenablog.com/)
- [Murga](https://neos21.hatenablog.jp/)
- [El Mylar](https://neos21.hateblo.jp/)
- [Neo's GitHub Pages](https://neos21.github.io/)
- [GitHub - Neos21](https://github.com/Neos21/)

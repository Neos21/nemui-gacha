import random

from . import validator, exceptions

# 末尾の「ガチャ」を除去して返す
def remove_gacha_str(input):
  if not validator.is_gacha(input):
    raise exceptions.NotGachaInputException
  
  if input[-3:] in ['ガチャ', 'がちゃ']:
    return input[:-3]
  elif input[-4:] == 'ｶﾞﾁｬ':
    return input[:-4]
  
  raise exceptions.GachaException  # 未到達

# ガチャすべきかどうか (True なら否定形を返すことにする)
def should_do_gacha():
  return random.choice((True, False))

# 入力値が空文字でないか確認する
def is_empty_str(input):
  return input is None or input == ''

# 入力値が「〜〜ガチャ」の形式かどうか確認する
def is_gacha(input):
  return (len(input) > 3 and input[-3:] in ['ガチャ', 'がちゃ']) or (len(input) > 4 and input[-4:] == 'ｶﾞﾁｬ')

# 正しく否定形に変換できたかどうか (入力値と置換結果が異なるかどうか・同一であれば置換失敗)
def is_successfully_replaced(input, result):
  return input != result

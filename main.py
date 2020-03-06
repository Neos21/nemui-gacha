import random
import sys

import MeCab
mecab = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

# メイン処理
def main(input):
  if not input or input == '':
    print('何か入れて')
    return
  
  # ガチャ判定・末尾ガチャ除去
  input_removed_gacha = ''
  if input[-3:] in ['ガチャ', 'がちゃ']:
    input_removed_gacha = input[:-3]
  elif input[-4:] == 'ｶﾞﾁｬ':
    input_removed_gacha = input[:-4]
  else:
    print('ガチャじゃないよ')
    return
  
  if not input_removed_gacha:
    print('なんのガチャかしら')
    return
  
  # 否定形に変換する
  result = parse(input_removed_gacha)
  
  # 変換がうまくいかなかった場合
  if result == '':
    print('なんのことか分からない')
    return
  
  # ガチャ：否定形を返すか元の文言を返すかランダムに決める
  do_gacha = random.choice((True, False))
  
  # 結果出力
  if do_gacha:
    print(result)
  else:
    print(input_removed_gacha)

# 否定形に変換する
def parse(input):
  raw_parsed = mecab.parse(input)
  
  # 整形
  parsed = raw_parsed.split('\n')
  parsed = list(filter(lambda x: x != 'EOS' and x != '', parsed))
  parsed = list(map(lambda x: x.replace('\t', ','), parsed))
  
  # 置換する情報を格納する
  replaces = []
  
  for index, raw_node in enumerate(reversed(parsed)):
    node       = raw_node.split(',')
    real_index = len(parsed) - 1 - index
    
    surface    = node[0]
    pos        = node[1]
    print('[DEBUG]', index, real_index, surface, pos, raw_node)
    
    if pos == '形容詞':
      words = list(surface)
      if words[-1] == 'い':
        words[-1] = 'くない'
      replaces.append({ 'index': real_index, 'word': ''.join(words) })
      break
    
    if pos == '動詞' and surface == 'いる':
      replaces.append({ 'index': real_index, 'word': 'いない' })
      break
    elif pos == '動詞' and surface == 'する':
      replaces.append({ 'index': real_index, 'word': 'しない' })
      break
    elif pos == '動詞' and (node[5] == '一段' or node[5].startswith('カ変')):
      words = list(surface)
      words[-1] = 'ない'
      replaces.append({ 'index': real_index, 'word': ''.join(words) })
      break
    elif pos == '動詞' and node[5].startswith('五段'):
      words = list(surface)
      words[-1] = words[-1].translate(str.maketrans({ 'う':'わ', 'く':'か', 'す':'さ', 'つ':'た', 'ぬ':'な', 'ふ':'は', 'む':'ま', 'ゆ':'や', 'る':'ら' })) + 'ない'
      replaces.append({ 'index': real_index, 'word': ''.join(words) })
      break
    
    if pos == '助動詞' and surface == 'た':
      prev_node    = list(reversed(parsed))[index + 1].split(',')
      prev_surface = prev_node[0]
      prev_pos     = prev_node[1]
      
      if prev_pos == '動詞' and prev_surface in ['て','い']:
        replaces.append({ 'index': real_index, 'word': 'なかった' })
        break
      elif prev_surface == '来':
        replaces.append({ 'index': real_index, 'word': 'ない' })
        break
      elif prev_surface[-1] == 'い':
        replaces.append({ 'index': real_index, 'word': 'てない' })
        break
      else:
        # FIXME : 「眠かった」→形容詞「眠かっ」などがヒットする
        break
    elif pos == '助動詞' and surface == 'たい':
      replaces.append({ 'index': real_index, 'word': 'たくない' })
      break
    elif pos == '助動詞' and surface == 'ない':
      replaces.append({ 'index': real_index, 'word': 'なくない' })
      break
    elif pos == '助動詞' and surface == 'ます':
      replaces.append({ 'index': real_index, 'word': 'ません' })
      break
    
    if pos == '名詞' and node[2] in ['一般', '固有名詞', '接尾']:
      replaces.append({ 'index': real_index, 'word': surface + 'じゃない' })
      break
    elif pos == '名詞':
      # FIXME : 「課金」→「課金しない」と変換しているが、肯定形で返す時は「課金する」と答えたい
      replaces.append({ 'index': real_index, 'word': surface + 'しない' })
      break
  
  # 置換すべき内容がなければ空文字列を返す
  if not replaces:
    print('[DEBUG] 置換テキストなし')
    return ''
  
  # 置換する
  result = ''
  for index, raw_node in enumerate(parsed):
    surface = raw_node.split(',')[0]
    
    if index in list(map(lambda x: x['index'], replaces)):
      replace_word = [x['word'] for x in replaces if x['index'] == index][0]
      result += replace_word
    else:
      result += surface
  
  # もし置換したつもりで元の文字列と同じ結果になっていたら置換失敗・空文字を返す
  if input == result:
    print('[DEBUG] 置換失敗')
    return ''
  
  return result

# 実行
if __name__ == '__main__':
  args = sys.argv
  
  if len(args) <= 1:
    print('引数がないよ')
    sys.exit(1)
  
  main(args[1])

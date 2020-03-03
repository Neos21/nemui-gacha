import MeCab
mecab = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

# メイン処理
def main(input):
  input_removed_gacha = ''
  
  # ガチャ判定・末尾ガチャ除去
  if input[-3:] in ['ガチャ', 'がちゃ']:
    input_removed_gacha = input[:-3]
  elif input[-4:] == 'ｶﾞﾁｬ':
    input_removed_gacha = input[:-4]
  else:
    print('あっそう')
    return
  
  if not input_removed_gacha:
    print('なんのガチャかしら')
    return
  
  # 否定形に変換する
  result = parse(input_removed_gacha)
  
  # 変換がうまくいかなかった場合は終わり
  if result == input_removed_gacha:
    print('なんのことか分からない')
    return
  
  print(result)

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
    print(index, real_index, surface, pos, raw_node)
    
    if pos == '形容詞':
      words = list(surface)
      if words[-1] == 'い':
        words[-1] = 'くない'
      replaces.append({ 'index': real_index, 'word': ''.join(words) })
      break
    
    if pos == '動詞' and surface == 'いる':
      replaces.append({ 'index': real_index, 'word': 'いない' })
      break
    elif pos == '動詞' and (node[5] == '一段' or node[5].startswith('カ変')):
      words = list(surface)
      words[-1] = 'ない'
      replaces.append({ 'index': real_index, 'word': ''.join(words) })
      break
    elif pos == '動詞' and node[5].startswith('五段'):
      words = list(surface)
      words[-1] = words[-1].translate(str.maketrans({ 'う':'あ', 'く':'か', 'す':'さ', 'つ':'た', 'ぬ':'な', 'ふ':'は', 'む':'ま', 'ゆ':'や', 'る':'ら' })) + 'ない'
      replaces.append({ 'index': real_index, 'word': ''.join(words) })
      break
    
    if pos == '助動詞' and surface == 'た':
      prev_node    = list(reversed(parsed))[index + 1].split(',')
      prev_surface = prev_node[0]
      prev_pos     = prev_node[1]
      
      if prev_pos == '動詞' and prev_surface in ['て','い']:
        replaces.append({ 'index': real_index, 'word': 'なかった' })
        break
      
      break  # TODO : 「眠かった」→形容詞「眠かっ」、「来た」→動詞カ変「来」などがヒットする
    elif pos == '助動詞' and surface == 'ない':
      replaces.append({ 'index': real_index, 'word': 'なくない' })
      break
    elif pos == '助動詞' and surface == 'ます':
      replaces.append({ 'index': real_index, 'word': 'ません' })
      break
    
    if pos == '名詞':
      replaces.append({ 'index': real_index, 'word': surface + 'じゃない' })
      break
  
  # 置換すべき内容がなければ元の文字列をそのまま返す
  if not replaces:
    return input
  
  # 置換する
  result = ''
  for index, raw_node in enumerate(parsed):
    surface = raw_node.split(',')[0]
    
    if index in list(map(lambda x: x['index'], replaces)):
      replace_word = [x['word'] for x in replaces if x['index'] == index][0]
      result += replace_word
    else:
      result += surface
  
  return result

# 実行
if __name__ == '__main__':
  #main('ねむいガチャ')
  
  for input in ['来た','書け',
    # NG : '眠かった','休もう'
    # OK : '眠い','眠くない','眠くなる','眠くならない','眠っていない','眠る','寝る','眠っている','眠ってる','眠っていた','眠ってた',
    #      '田中','寝ます','眠ります','寝ろ','眠れ','休め'
  ]:
    print('')
    print(parse(input))

import subprocess

import MeCab

# mecab-ipadic-neologd 辞書を指定して MeCab を準備する
dic_dir = subprocess.check_output('mecab-config --dicdir', shell = True).decode('utf-8').strip()
option = '-d ' + dic_dir + '/mecab-ipadic-neologd'
mecab = MeCab.Tagger(option)

# MeCab でパースする
def parse_mecab(input):
  raw_parsed = mecab.parse(input)
  
  # 不要な情報を削除し、1要素がカンマ区切りの文字列で構成された配列に整形する
  parsed = raw_parsed.split('\n')
  parsed = list(filter(lambda x: x != 'EOS' and x != '', parsed))
  parsed = list(map(lambda x: x.replace('\t', ','), parsed))
  
  return parsed

# パース結果を基に置換する情報を構築する
def make_replaces(parsed):
  # 置換する情報を格納する
  replaces = []
  
  # パース結果の末尾から走査する
  for index, raw_node in enumerate(reversed(parsed)):
    node       = raw_node.split(',')  # 表層形,品詞,品詞細分類1,品詞細分類2,品詞細分類3,活用型,活用形,原形,読み,発音
    real_index = len(parsed) - 1 - index
    
    surface     = node[0]  # 表層形 (元の文字列)
    pos         = node[1]  # 品詞
    pos_type_1  = node[2]  # 品詞細分類1
    conjugation = node[5]  # 活用型
    #print('[DEBUG]', index, real_index, surface, pos, raw_node)
    
    if pos == '形容詞':
      characters = list(surface)
      
      if characters[-1] == 'い':
        characters[-1] = 'くない'
        replaces.append({ 'index': real_index, 'word': ''.join(characters) })
      
      break
    
    if pos == '動詞':
      if surface[-2:] in ['ずる', 'ずれ']:  # サ変「ずる」 … 「重んずる」
        replaces.append({ 'index': real_index, 'word': surface[:-2] + 'じない' })  # 末尾2文字「ずる」を削り「じない」をつける (「重んじない」)
      if surface[-2:] == ['する', 'すれ']:  # サ変「(会話)/する」「察する」
        replaces.append({ 'index': real_index, 'word': surface[:-2] + 'しない' })  # 末尾2文字「する」を削り「しない」をつける (「会話/しない」「察しない」)
      elif conjugation == '一段' or conjugation.startswith('カ変'):  # 上一段「いる」「見る」「起きる」・下一段「出る」「教える」・カ変「来る」
        replaces.append({ 'index': real_index, 'word': surface[:-1] + 'ない' })  # 末尾1文字「る」を削り「ない」をつける
      elif conjugation.startswith('五段'):
        characters = list(surface)
        characters[-1] = characters[-1].translate(str.maketrans({ 'う':'わ', 'く':'か', 'す':'さ', 'つ':'た', 'ぬ':'な', 'ふ':'は', 'む':'ま', 'ゆ':'や', 'る':'ら' })) + 'ない'
        replaces.append({ 'index': real_index, 'word': ''.join(characters) })
      else:
        pass  #print('[DEBUG] 動詞 未処理')  # 到達しない想定
      
      break
    
    if pos == '助動詞':
      if surface == 'た':
        prev_node    = list(reversed(parsed))[index + 1].split(',')
        prev_surface = prev_node[0]
        prev_pos     = prev_node[1]
        
        if prev_pos == '動詞' and prev_surface in ['て','い']:
          replaces.append({ 'index': real_index, 'word': 'なかった' })
        elif prev_surface == '来':
          replaces.append({ 'index': real_index, 'word': 'ない' })
        elif prev_surface[-1] == 'い':
          replaces.append({ 'index': real_index, 'word': 'てない' })
        else:
          pass  #print('[DEBUG] 助動詞「た」未処理系')  # FIXME : 「眠かった」→形容詞「眠かっ」などがヒットする
      elif surface == 'たい':
        replaces.append({ 'index': real_index, 'word': 'たくない' })
      elif surface == 'ない':
        replaces.append({ 'index': real_index, 'word': 'なくない' })
      elif surface == 'ます':
        replaces.append({ 'index': real_index, 'word': 'ません' })  # 「行き/ます」→「行き/ません」となるが「行かない」と答えられたらいいな…
      
      break
    
    if pos == '助詞':
      if surface == 'て':  # 「教え/て」など
        replaces.append({ 'index': real_index, 'word': 'ない' })
      
      break
    
    if pos == '名詞':
      if pos_type_1 in ['一般', '固有名詞', '接尾']:
        replaces.append({ 'index': real_index, 'word': surface + 'じゃない' })
      elif pos == '名詞':
        #print('[DEBUG] 名詞 不完全処理系')  # FIXME : 「課金」→「課金しない」と変換しているが、肯定形で返す時は「課金する」と答えたい
        replaces.append({ 'index': real_index, 'word': surface + 'しない' })
      
      break
  
  return replaces

# パース結果と置換情報を基に否定形の文章に置換する
def replace_to_negative(parsed, replaces):
  result = ''
  
  for index, raw_node in enumerate(parsed):
    surface = raw_node.split(',')[0]
    
    if index in list(map(lambda x: x['index'], replaces)):
      replace_word = [x['word'] for x in replaces if x['index'] == index][0]
      result += replace_word
    else:
      result += surface
  
  return result

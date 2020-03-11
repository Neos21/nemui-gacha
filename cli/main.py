import sys

from libs import validator, prepare, parser

def main(args):
  if len(args) <= 1:
    return print('引数がないよ')
  
  input = args[1]
  
  if validator.is_empty_str(input):
    return print('何か入れて')
  
  if not validator.is_gacha(input):
    return print('ガチャじゃないよ')
  
  removed_input = prepare.remove_gacha_str(input)
  
  if validator.is_empty_str(removed_input):
    return print('なんのガチャかしら')
  
  # ガチャしない場合はそのまま出力する
  if not prepare.should_do_gacha():
    return print(removed_input)
  
  parsed   = parser.parse_mecab(removed_input)
  replaces = parser.make_replaces(parsed)
  result   = parser.replace_to_negative(parsed, replaces)
  
  if not validator.is_successfully_replaced(removed_input, result):
    return print('なんのことか分からない')
  
  print(result)

if __name__ == '__main__':
  main(sys.argv)

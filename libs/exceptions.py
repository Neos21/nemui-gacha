class GachaException(Exception):
  '例外の基底クラス'

class NotGachaInputException(GachaException):
  '入力値の末尾がガチャで終わっていない'

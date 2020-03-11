class GachaException(Exception):
  '例外の基底クラス'

class InvalidInputException(GachaException):
  '入力値不正'

class EmptyInputException(InvalidInputException):
  '入力値が空'

class NotGachaInputException(InvalidInputException):
  '入力値の末尾がガチャで終わっていない'

# https://www.youtube.com/watch?v=vBH6GRJ1REM  Python dataclasses will save you HOURS, also featuring attrs
import inspect
from dataclasses import dataclass, astuple, asdict, field
from pprint import pprint
@dataclass(frozen=True, order=True)
class Comment:
  id:int = field()
  text:str = field(default="")
  replies: list[int] = field(default_factory=list)

def main():
  comment = Comment(1,"I just test!")
  print(comment)
  print(astuple(comment))
  print(asdict(comment))

  pprint(inspect.getmembers(Comment, inspect.isfunction))

if __name__ == '__main__':
  main()
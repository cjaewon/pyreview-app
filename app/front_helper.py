import pathlib

cache = {}

def read_html_with_cache(path: str, encoding="utf-8") -> str:
  path_obj = pathlib.Path(path)
  path_abs = path_obj.absolute()

  if path_abs not in cache:
    cache[path_abs] = path_obj.read_text(encoding=encoding)

  return cache[path_abs]
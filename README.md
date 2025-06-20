# pyreview-app
> [Introduction to Computers and Programming 컴프입] Term Project  
2025 Spring  
[Prof. Woo](https://pl.pusan.ac.kr/~woogyun/)

## How to Install

```sh
git clone https://github.com/cjaewon/pyreview-app
cd pyreview-app
mv .example.env.toml .env.toml # you must write your api key!
uv sync
```

## How To Run
```sh
uv run uvicorn main:app --app-dir app
```

## not implemented
- frontend api error status message
  - day limit
  - ...
- openapi error status code 
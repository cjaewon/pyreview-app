# pyreview-app
> [Introduction to Computers and Programming 컴프입] Term Project  
2025 Spring  
[Prof. Woo](https://pl.pusan.ac.kr/~woogyun/)

## Reports
See `/doc` directory.

- [proposal.pdf](https://github.com/cjaewon/pyreview-app/blob/main/doc/proposal.pdf)
- [final_report.pdf](https://github.com/cjaewon/pyreview-app/blob/main/doc/final_report.pdf)
- [slide.pdf](https://github.com/cjaewon/pyreview-app/blob/main/doc/slide.pdf)

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

## Note
The frontend's handling of error codes from the backend is weak. Also, not all status codes are displayed in the OpenAPI documentation.
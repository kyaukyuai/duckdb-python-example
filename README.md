# duckdb-python-example

example codes for using DuckDB with the Python client

## How to run the example codes

### Local

1. Create a virtual environment and activate it

```bash
$ python3 -m venv venv
$ . venv/bin/activate
```
2. Install the requirements

```bash
$ pip install -r requirements.txt
```

3. Run the example codes

```bash
$ python3 example/simple.py
```

### Docker

1. Build and Run the docker image

```bash
$ make build
$ make run
```

2. Run the example codes

```bash
$ python3 example/simple.py
```
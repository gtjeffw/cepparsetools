# CEP Parse Tools
CEP Parse Tools provides tools for parsing CEP data.

Right now, it provides a parser that converts AWS IoT Analytics data contained within CSV query results into Python data structures. This data is very similar to JSON, but not quite.

## Installation/Update

> pip install git+https://github.com/????/cepparsetools

## Usage

* cep_iot_parser

```
str0 = r'{cepid=CEP010, filename=a/b/c/d/e/f.json, filecount=58, loaddate=2022-03-12T04:32:30.124Z}'
demo = cep_parse_iot(str0)
print(demo)
print(demo['cepid'])
```

## Dependencies

* Lark - https://github.com/lark-parser/lark
* re - Python Regular Expressions

## License

[MIT](LICENSE)
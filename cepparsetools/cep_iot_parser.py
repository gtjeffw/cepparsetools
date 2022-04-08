from lark import Lark
from lark import Transformer
import re

# CEP AWS IoT Analytics CSV result parser
# Description: This converts AWS IoT Analytics data that is in a JSON-like format (but not actually JSON)
# into Python data structs.
#
# Example usage:
# str0 = r'{cepid=CEP010, filename=a/b/c/d/e/f.json, filecount=58, loaddate=2022-03-12T04:32:30.124Z}'
# demo = cep_parse_iot(str0)
# print(demo)
#
# Author: Jeff Wilson (jeff@imtc.gatech.edu)

# These regexes are used to promote generic values to either ints or floats, if possible
regex_num = re.compile('^-?(?=[1-9]|0(?!\d))\d+(\.\d+)?([eE][+-]?\d+)?$')
regex_int = re.compile('^[-+]?[0-9]+$')


# Lark Transformer to convert AWS-IoT data to Python data structs
class IoTTransformer(Transformer):

    def list(self, items):
        return list(items)

    def pair(self, key_value):
        k, v = key_value
        return k, v

    def dict(self, items):
        return dict(items)

    def label(self, s):
        (s,) = s
        s = str(s)
        return s

    def generic(self, s):
        (s,) = s
        s = str(s)
        if regex_num.match(s):
            success = False
            if regex_int.match(s):
                try:
                    v = int(s)
                    s = v
                    success = True
                except ValueError:
                    success = False
            if not success:
                try:
                    v = float(s)
                    s = v
                except ValueError:
                    pass
        return s

    def string(self, s):
        (s,) = s
        return s[1:-1]

    def null(self, _):
        return None

    def true(self, _):
        return True

    def false(self, _):
        return False


# A note about the parser config below. Whitespace is ignored, however it is recovered
# automatically _after_ a token is matched. The end result is that spaces in the interior
# of token string sequences are preserved. This ends up being the behavior that we want!
# Also, this is heavily based on the json example in the lark documentation
cep_iot_parser_rules = r'''
    ?value: dict
          | list
          | string
   //       | number // better to ignore numbers and later see if labels can be promoted to nums
          | generic
          | "true"             -> true
          | "false"            -> false
          | "null"             -> null           

    list : "[" [value ("," value)*] "]"

    dict : "{" [pair ("," pair)*] "}"

    // We use an = instead of : for our not-JSON format
    pair : (string | label) "=" value

    IOT_TOK : /[^=,{}[\]]+/  
    
    // A key that is not a string
    label: IOT_TOK  
    
    // A value other than nested types, strings, or true|false|null
    generic: IOT_TOK
    
    string : ESCAPED_STRING

    // number : SIGNED_NUMBER

    %import common.ESCAPED_STRING
    // %import common.SIGNED_NUMBER
    %import common.WS
    %ignore WS

    '''

cep_iot_parser = Lark(cep_iot_parser_rules, start='value', parser='lalr', transformer=IoTTransformer())
cep_iot_tree_parser = Lark(cep_iot_parser_rules, start='value', parser='lalr')


# Switch back to separate transformer and parse tree if more dev needs to be done
# cep_iot_transformer = IoTTransformer()


# Takes a cell from AWS IoT Analytics CSV results and converts to Python data structure
def cep_parse_iot(s):
    # tree = cep_iot_parser.parse(s)
    # return cep_iot_transformer.transform(tree)
    return cep_iot_parser.parse(s)


if __name__ == "__main__":
    # Some test data
    str0 = r'{cepid=CEP010, filename=orcatech_data/json/home_2001/2022-03-11_2022-03-12/nyce-w-6975_26288.json, filecount=58, loaddate=2022-03-12T04:32:30.124Z}'
    str1 = r'{cepid=CEP010, dict={this=thing, hello=world, one=2.0}, listicle=[my, list, of, craps, 1.2, 3], bob="And Bob is \" my uncle", filename=orcatech_data/json/home_2001/2022-03-11_2022-03-12/nyce-w-6975_26288.json, filecount=58, label with spaces=3.14, another label=this is some string with spaces but without quotes, bool_thing=false, happy_little null=null, loaddate=2022-03-12T04:32:30.124Z, not actually true=true dat}'
    str2 = r'{itemid=26288, itemname=nyce-w-6975, serialnumber=ZBW6975, macaddress=000D6F00132B33CB, modelid=120, modelname=NCZ-3041, subjectspecific=0, vendorid=52, vendorname=NYCE Controls, typeid=10, typename=Activity Sensors, subtypeid=39, subtypename=Zigbee / Wall, currenthomeid=null, currenthomestart=null, active=null, activename=null, statusid=null, statusname=null, batterymonths=12, lastbatterychange=null, hasbatteries=1}'
    str3 = r'{stamp=1.647039603041E9, event=48, sunday=null, monday=null, tuesday=null, wednesday=null, thursday=null, friday=null, saturday=null, sequencenum=12, macaddress=000D6F00132B33CB, areaid=23, areaname=Kitchen 1, alarm1=false, alarm2=false, tamper=false, battery=false, superreports=true, restorereports=true, trouble=false, ac=false, weight=null, fatmass=null, watermass=null, bonemass=null, musclemass=null, batterylevel=null, from=null, to=null, duration=null, fromgmtoffset=null, durationinbed=null, durationawake=null, durationinsleep=null, durationinrem=null, durationinlight=null, durationindeep=null, durationsleeponset=null, durationbedexit=null, awakenings=null, bedexitcount=null, tossnturncount=null, avghr=null, minhr=null, maxhr=null, hrvscore=null, hrvlf=null, hrvhf=null, avgrr=null, minrr=null, maxrr=null, avgactivity=null, fmcount=null, sleepscore=null}'
    str4 = '{"key": ["item0", "item1", 3.14], "key2": true, tricky label: "bob", label2: tricky value}'

    text = str1

    my_transformer = IoTTransformer()
    tree = cep_iot_tree_parser.parse(text)

    out = tree.pretty()

    print("parsed:")
    print(out)


    transform = my_transformer.transform(tree)

    print("Transformer Example:")
    print(transform)

    demo = cep_parse_iot(str0)
    print(demo)

    demo = cep_parse_iot(str1)
    print(demo)

    demo = cep_parse_iot(str2)
    print(demo)

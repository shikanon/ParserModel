import re

def user_normalize_function(url):
    url = url.replace("http://epub.cnki.net/kns","http://www.cnki.net/KCMS")
    magical_parm = "&urlid=&yx=&uid=WEEvREcwSlJHSldTTGJhYkdDekROODNNRlorSml6NTJTalpkRHJwTEVlWWl0SWdXMFpkWDlnMjRSVi96Nzk3bmdRUT0=$9A4hF_YAuvQ5obgVAqNKPCYcEjKensW4IQMovwHtwkF4VYPoHbKxJw!!&v=MzEzMjJyU2Q3RzRIOVhOcjQ5RVpvUjhlWDFMdXhZUzdEaDFUM3FUcldNMUZyQ1VSTHlmWnVSdkZDbmhVYjNQSWk="
    return url + magical_parm


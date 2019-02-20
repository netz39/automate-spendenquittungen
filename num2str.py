#! /usr/bin/env python3

testcases = {
    1:"eins",
    2:"zwei",
    3:"drei",
    4:"vier",
    10:"zehn",
    11:"elf",
    12:"zwölf",
    13:"dreizehn",
    16:"sechzehn",
    17:"siebzehn",
    20:"zwanzig",
    21:"einundzwanzig",
    30:"dreißig",
    40:"vierzig",
    50:"fünfzig",
    60:"sechzig",
    70:"siebzig",
    100:"einhundert",
    111:"einhundertundelf",
    500:"fünfhundert",
    1000:"eintausend",
    13456:"dreizehntausendundvierhundertundsechsundfünfzig"
}

def lu_1(n):
    assert n >= 0
    assert n < 10
    lu1 = { 
        0:"",
        1:"eins",
        2:"zwei",
        3:"drei",
        4:"vier",
        5:"fünf",
        6:"sechs",
        7:"sieben",
        8:"acht",
        9:"neun"
        }  
    return lu1[n]

def lu_1x(n):
    assert n >= 0
    assert n < 20
    exceptions = {
        11:"elf",
        12:"zwölf",
        16:"sechzehn",
        17:"siebzehn"
    }
    if n < 10:
        return lu_1(n)
    elif n in exceptions.keys():
        return exceptions[n]
    else:
        return lu_1(int(n%10)) + 'zehn'

def lu_xx(n):
    assert n >= 0
    assert n < 100
    exceptions = {
        2:"zwanzig",
        3:"dreißig",
        6:"sechzig",
        7:"siebzig"
    }

    if n < 20:
        return lu_1x(n)

    if n%10 == 0:
        prefix = ''
    elif n%10 == 1:
        prefix = 'einund'
    else: 
        prefix = lu_1(n%10) + 'und'


    if int(n/10) in exceptions.keys():
        return prefix + exceptions[int(n/10)]
    else:
        return prefix + lu_1(int(n/10)) + 'zig'
    
def lu_xxx(n):
    assert n >= 0
    assert n < 1000

    if n < 100:
        return lu_xx(n)

    if int(n/100) == 1:
        prefix = 'einhundert'
    else:
        prefix = lu_1(int(n/100)) + 'hundert'
    
    if n%100 == 0:
        suffix = ''
    else:
        suffix = 'und' + lu_xx(n%100)

    return prefix + suffix

def lu_xxxx(n):
    assert n >= 0
    assert n < 1000000
    if n < 1000:
        return lu_xxx(n)

    if int(n/1000) == 1:
        prefix = 'eintausend'
    else:
        prefix = lu_xxx(int(n/1000)) + 'tausend'

    if n%1000 == 0:
        suffix = ''
    else:
        suffix =  'und' + lu_xxx(n%1000)
    
    return prefix + suffix

def num2str(number):
    assert number >= 0
    assert number < 1000000
    return lu_xxxx(number)

def test():
    for key in testcases.keys():
        assert num2str(key) == testcases[key], '{} - got {} - expected {}'.format(
            key,
            num2str(key),
            testcases[key]
        )
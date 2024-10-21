ones = ["zero ", "one ", "two ", "three ", "four ", "five ", "six ", "seven ", "eight ", "nine "]

tens = ["ten ", "eleven ", "twelve ", "thirteen ", "fourteen ", "fifteen ", "sixteen ", "seventeen ", "eighteen ", "nineteen "]

tens_2 = ["","", "twenty ", "thirty ", "fourty ", "fifty ", "sixty ", "seventy ", "eighty ", "ninety "]

suffixes = ["", "thousand ", "million ", "billion ", "quadrillion ", "quintillion "]

def num_words(number):
    number = int(number)
    result=''
    num_length = len(str(number))
    divider = num_length - 1
    while divider >= 0:
        value = number // (10**(divider))
        value = value % 10
        ending = suffixes [divider // 3]
        div = divider % 3
        if value > 0:
            if divider == 0:
                if num_length > 1 and (number // (10**(1)))== 0:
                   result = result + "and " + ones[value] 
                else:    
                    result = result + ones[value] 
            elif divider == 1:
                if value == 1:
                    divider = divider -1
                    value = number // (10**(divider))
                    value = value % 10
                    if num_length > 2 :
                        result = result + "and " + tens[value] 
                    else: 
                        result = result + tens[value] 
                else:
                    if (num_length) > 2 :
                        result = result + "and " +tens_2[value] 
                    else: 
                        result = result + tens_2[value]
            elif divider == 2:
                result = result + ones[value] + "hundred " 
            elif divider > 2:
                n = value
                for i in range (div):
                    divider = divider-1
                    value = number // (10**(divider))
                    value = value % 10
                    value = str(value)
                    n= str(n)
                    n = n+value
                n = int(n)
                result = result + num_words(n) + ending
            
        else:
            if num_length ==1:
                result = result + ones[value]
        divider = divider -1
    return result
    
def convert_num(number):
    number = float(number)
    if number < 0:
        negative = True
    else:
        negative = False
    number = abs(number)
    raw_num = number // 1
    raw_num = int(raw_num)
    if raw_num > 0:
        dec_num = round(number % raw_num,2)
    else:
        dec_num = round(number,2)
    dec = dec_num * 10**2
    result = num_words(raw_num)+ "cedis " + "and " + num_words(dec)+"pesewas "
    start = result[0]
    start = start.upper()
    final = start+result[1:-1]
    if negative == True:
        final = "Negative "+final
    else:
        final = final
    return final






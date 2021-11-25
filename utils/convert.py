def string_from_list(lis):
    addition='<@>'
    string=''
    for item in lis:
        if item == lis[len(lis)-1]:
            string+= item.strip()
        else:
            string+= item.strip()+ ' '+ addition+' '
    return string



def delete_some(str1,str2):
    temp=''
    str1_list=str1.split(',')
    for now in str1_list:
        if now != str2 and now != '':
            temp += now + ','
    return temp
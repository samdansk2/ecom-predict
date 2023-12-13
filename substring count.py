def string(str,sub_str):
    count=0
    index = str.find(sub_str)
    while index!=-1:
        count+=1
        index= str.find(sub_str, index+1)
    return count
str="abcdcdc"
sub_str="cdc"
ab= string(str,sub_str)
print(ab)

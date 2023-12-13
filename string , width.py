def split_string(input_string, width):

    chunks = []  

    i = 0
    while i < len(input_string):
        chunk = ""
        for j in range(width):
            if i < len(input_string):
                chunk += input_string[i]
                i += 1
        chunks.append(chunk)

    result = ' '.join(chunks)
    return result

input_string = "abcdefghi"
width = 3

output = split_string(input_string, width)
print(output)

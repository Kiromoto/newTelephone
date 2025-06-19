from adressBook import content, clear_book

# result = []

# position_end = content.find("@mail.gkse", 0)
# while position_end != -1:
#     position_start = content[0:position_end].find("aria-label=")
#     if position_start != -1:
#         s = content[position_start+12:position_end + 10].strip()
#         if 'Remove' not in s:
#             s = s.replace("  ", " ")
#             s = s.replace("<", "")
#             print(s)
#             result.append(s)
#     content = content[position_end + 10:]
#     position_end = content.find("@mail.gkse", 0)

# print(result)
# print(len(result))



for element in clear_book:
    last_w = element.rfind(' ')
    if last_w != -1:
        name = element[:last_w]
        print(name)

for element in clear_book:
    last_w = element.rfind(' ')
    if last_w != -1:
        email = element[last_w + 1:]
        print(email)




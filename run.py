

sample_id = '91101800034'
i = 0
spacer = ""
while i < (22 - len(sample_id)):
    spacer += " "
    i += 1
full_sample_id = spacer + sample_id
print("Full Sample Id: {}".format(full_sample_id))
print("Full Sample Id Len: {}".format(len(full_sample_id)))
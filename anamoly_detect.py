#-----------READING A LOG FILE-----------
from collections import Counter

with open("application.log","r") as file:
    logs = file.readlines()

# print(logs)

# for log in logs:
#     print(log.split())

# ----------------PARSING----------------

# log1 = "2026-08-18 10:01:09 INFO UserService Request successful"

# date , time , level , source , message = log1.split(" ",4)
# print(log1)
# print("Date :",date)
# print("Time :",time)
# print("Level :",level)
# print("Source :",source)
# print("Message :",message)

#----------------ANAMOLY DETECT-----------------
error_count = 0
for log in logs:
    if "ERROR" in log:
        error_count += 1

print("No of Errors:",error_count)


info_count = 0
for log in logs:
    if "INFO" in log:
        info_count += 1

print("No of Informations:",info_count)


#--------------COUNT ERRORS BY TIME---------------

errors_by_time = Counter()

for log in logs:
    parse = log.split()

    if "ERROR" in parse:
        minute = parse[1][:5]
        errors_by_time[minute] +=1

print(errors_by_time)
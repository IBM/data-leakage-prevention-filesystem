from faker import Faker
import os
import random
import sys

if len(sys.argv) < 4:
    print("usage: data-generation.py <file_name> <desired_size> <number_of_files>")
    quit()

file_name = sys.argv[1]
print(f"File name: {file_name}")

desired_size = int(sys.argv[2])
print(f"Desired number of rows: {desired_size}")

number_of_files = int(sys.argv[3])
print(f"Number of files: {number_of_files}")

fake = Faker()
total_icd = 0
total_records = 0
total_emails = 0
total_batwomen = 0
total_catwomen = 0

for file_number in range(number_of_files):
    if number_of_files > 1:
        file = f"{file_name}.{file_number}"
    else:
        file = f"{file_name}"
    
    with open(file, 'a') as f:
        #f.write('"id","icd","amount","message"\n')
      
        while True:
            total_records = total_records + 1

            amount = f'"${round(random.uniform(1,1000),2)}"'

            if random.uniform(0,1) <= 0.05:
                icd = '"' + fake.icd_code() + '"'
                total_icd += 1
            else:
                icd = '""'

            message = '"' + fake.sentence()

            if random.uniform(0,1) <= 0.01:
                message += " SporadicKeyword."            
                total_batwomen += 1

            if random.uniform(0,1) <= 0.10:
                message += " FrequentKeyword."
                total_catwomen += 1

            if random.uniform(0,1) <= 0.05:
                message += " " + fake.email()
                total_emails = total_emails + 1

            message += " " + fake.sentence() + '"'

            f.write(f'{total_records},{icd},{amount},{message}\n')

            if total_records >= desired_size:
                break

    print(f"Bytes written: {os.path.getsize(file)}")
    print(f"Number of records: {total_records}")
    print(f"Total icd: {total_icd}")
    print(f"Total batwomen: {total_batwomen}")
    print(f"Total catwomen: {total_catwomen}")
    print(f"Total emails: {total_emails}")

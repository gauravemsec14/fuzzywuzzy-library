import json
from fuzzywuzzy import fuzz

def find_key(obj, target_keys):
    max_similarity = 0
    found_key = None

    if isinstance(obj, dict):
        for key in obj.keys():
            similarity = fuzz.ratio(target_keys[0], key.lower())
            if similarity > max_similarity:
                max_similarity = similarity
                found_key = key

    return found_key

def find_email_key(obj):
    email_keys = ['email', 'e-mail', 'mail', 'user_email', 'user_email_address', 'user_mail']
    return find_key(obj, email_keys)

def find_password_key(obj):
    password_keys = ['password', 'pass', 'passwd', 'user_password', 'user_pass', 'user_passwd', 'secure_password']
    return find_key(obj, password_keys)

def find_phone_key(obj):
    phone_keys = ['phone', 'mobilenumber', 'mobile_number', 'telephone', 'tel', 'Mobile no']
    return find_key(obj, phone_keys)

def find_password(obj):
    password_key = find_password_key(obj)

    if password_key:
        password_value = obj.get(password_key, '')
        if isinstance(password_value, str) and password_value.strip():  
            return password_value

    return ''

def find_phone(obj):
    phone_key = find_phone_key(obj)

    if phone_key:
        phone_value = obj.get(phone_key, '')
        if isinstance(phone_value, str) and phone_value.strip() and phone_value.isdigit():  
            return phone_value

    return ''

def find_emails_and_passwords(obj):
    result_list = []

    email_key = find_email_key(obj)
    phone = find_phone(obj)

    if isinstance(obj, dict) and email_key:
        email = obj.get(email_key, '')
        password = find_password(obj)
        password_hash = obj.get('password_hash', '')
        id_value = obj.get('id', '')
        username = obj.get('username', '')
        name = obj.get('name', '')
        dob = obj.get('dob', '')
        address = obj.get('address', '')
        source = obj.get('source', '')
        breach_date = obj.get('breach_date', '')
        domain_name = obj.get('domainName', '')
        others = obj.get('others', '')

        result_list.append({
            "id": id_value,
            "username": username,
            "email": email,
            "password": password,
            "password_hash": password_hash,
            "name": name,
            "dob": dob,
            "phone": phone,
            "address": address,
            "source": source,
            "breach_date": breach_date,
            "domainName": domain_name,
            "others": others
        })

    return result_list

def process_json_data(json_data):
    result_list = []
    for item in json_data:
        result_list.extend(find_emails_and_passwords(item))

    return result_list

def read_and_find_emails_and_passwords(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    result_list = process_json_data([json_data]) if isinstance(json_data, dict) else process_json_data(json_data)
    return result_list

def save_to_json(output_file_path, data):
    try:
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            json.dump(data, output_file, indent=2, ensure_ascii=False)
        print(f'Found Email Addresses and Passwords saved to {output_file_path}')
    except Exception as e:
        print(f'Error saving to JSON file: {e}')

def main():
    input_file_path = 'C:\\Users\\Gaurav Kumar\\Desktop\\testing\\testing.json'
    result_list = read_and_find_emails_and_passwords(input_file_path)

    output_file_path = 'C:\\Users\\Gaurav Kumar\\Desktop\\testing\\output_emails_and_passwords.json'
    save_to_json(output_file_path, result_list)

if __name__ == "__main__":
    main()

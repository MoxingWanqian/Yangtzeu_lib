users_Id = input('请输入账号: ').strip()
users_passwd = input('请输入密码: ').strip()
users = {
	'Id': users_Id,
	'passwd': users_passwd
}
with open('./Lib/users_dict.dll', 'w', encoding='utf-8') as f:
	f.write(str(users))
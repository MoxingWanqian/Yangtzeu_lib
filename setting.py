home_list = [
    '一楼电子文献阅览室',
    '一楼社科借阅室(1)',
    '一楼社科借阅室(3)',
    '二楼大厅',
    '二楼报刊阅览室(1)',
    '二楼报刊阅览室(2)',
    '二楼社科借阅室(2)',
    '三楼外文借阅室',
    '三楼大厅',
    '三楼自科借阅室(1)',
    '四楼大厅',
    '四楼自科借阅室(2)'
]

# 房间Id列表
roomsId = {
    '一楼社科借阅室(1)': 1,
    '一楼社科借阅室(3)': 2,
    '二楼社科借阅室(2)': 3,
    '二楼大厅': 4,
    '二楼报刊阅览室(1)': 5,
    '二楼报刊阅览室(2)': 6,
    '三楼自科借阅室(1)': 7,
    '三楼大厅': 8,
    '三楼外文借阅室': 9,
    '四楼自科借阅室(2)': 10,
    '四楼大厅': 11,
    '一楼电子文献阅览室': 13
}

print('-' * 50)
for home in home_list:
	num = home_list.index(home)
	num = '%02d' % num
	print(f'{num} | {home}')
print('-' * 50)
home_num = int(input('请输入你想要选择的房间的序号：').strip())
while home_num not in [i for i in range(12)]:
	home_num = int(input('请输入你想要选择的房间的序号：').strip())
print(f'你选择的房间是： {home_list[home_num]}')

with open('./Lib/seatId_dict.dll', 'r', encoding='utf-8') as f:
	seatId_dict = eval(f.read())
	room = seatId_dict[home_list[home_num]]
	seat_num = int(input('请输入你想要预约的座位号: '))
	seat_num = "'%03d'" % seat_num
	seatId = int(room[seat_num])

start_num = int(input('请输入你想要预约的开始时间: ').strip())
end_num = int(input('请输入你想要预约的结束时间: ').strip())

data_dict = {'roomId': roomsId[home_list[home_num]], 'seatId': seatId, 'start_time': start_num, 'end_time': end_num}
with open('./Lib/data_dict.dll', 'w', encoding='utf-8') as d:
    d.write(str(data_dict))
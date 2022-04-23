# -*- coding: utf-8 -*-
import os
import xlwt
import re
import major_function
"""
该脚本文件是对KVDK——P2CA日志文件内容的信息进行提取后汇总excel文件
脚本说明：
1、KVDK数据分类(string\sorted)提取
2、进行容量排序
3、写入数据生成不同的模式表
4、读取多个文件夹进行以上步骤操作
5、生成excel文件
"""
file_path = '/home/zdc/KVDK_P2CA_log'     # 日志文件存放的路径
# excel_name = 'kvdk_p2ca_data'     # 保存的excel文件名称
path = os.path.realpath(__file__).split('kvdk_p2ca_data')[0]
print(path)
if os.path.isdir(path + 'save_csv'):
    file_list = os.listdir(path + 'save_csv')
    for file_name in file_list:
        os.remove(path + 'save_csv' + '/' + file_name)
else:
    os.mkdir(path + 'save_csv')

save_path = path + 'save_csv'  # csv文件保存路径当前文件夹下

def kvdk_p2ca_data():
    file_folders = os.listdir(file_path)
    print(file_folders)
    title_ru91 = ['type', 'options', 'value_size', 'bench_threads', 'instance_threads',	'read_OPS',
                  'AVG', 'P50', 'P99', 'P99.5', 'P99.9', 'P99.99', 'write_OPS', 'AVG', 'P50', 'P99', 'P99.5', 'P99.9',
                  'P99.99']
    title_list = ['type', 'options', 'value_size', 'bench_threads', 'instance_threads', 'write_OPS', 'AVG', 'P50', 'P99', 'P99.5', 'P99.9',
                  'P99.99']
    title_scan = ['type', 'options', 'value_size', 'bench_threads', 'instance_threads', 'read_OPS', 'AVG', 'P50', 'P99', 'P99.5', 'P99.9',
                  'P99.99']
    for folder in file_folders:
        if os.path.exists(file_path + '/' + folder):
            # print(folder)
            file_names = os.listdir(file_path + '/' + folder)
            # print(file_names)
            result_sorted = []
            result_string = []
            result_list = []
            for file_name in file_names:
                if 'sorted' in file_name:
                    result_sorted.append(file_name)
                elif 'string' in file_name:
                    result_string.append(file_name)
            result_list.append(result_sorted)
            result_list.append(result_string)
            excel_name = folder
            
            for save_data in result_list:
                workbook = major_function.Instantiate_excel_object()
                if 'sorted' in save_data[0]:
                    fill_data = []
                    insert_data = []
                    read_data = []
                    ru91_data = []
                    scan_data = []
                    update_data = []
                    for log_name in save_data:
                        # print(log_name.split('_'))
                        if 'fill' in log_name.split('_')[2]:
                            fill_data.append(log_name)
                        elif 'insert' in log_name.split('_')[2]:
                            insert_data.append(log_name)
                        elif 'read' in log_name.split('_')[2]:
                            read_data.append(log_name)
                        elif 'ru91' in log_name.split('_')[2]:
                            ru91_data.append(log_name)
                        elif 'scan' in log_name.split('_')[2]:
                            scan_data.append(log_name)
                        elif 'update' in log_name.split('_')[2]:
                            update_data.append(log_name)

                    update_all_name = []
                    for update_name in update_data:
                        print(update_name)
                        update_list = []
                        update_list.append('sorted')
                        update_list.append('update')
                        values = re.findall(r'\d+', update_name)
                        update_list.append(int(values[0]))    # 添加value_size
                        update_list.append(int(values[1]))    # 添加bench_threads
                        # 添加instance_threads
                        update_list.append(int(values[1]))

                        with open(file_path + '/' + folder + '/' + update_name, 'r') as f:
                            for line in f.readlines():
                                # 判断条件是否满足，获取IOPS

                                if 'read ops' in line and 'write ops' in line:
                                    print(line)
                                    iops = (re.findall(r'\d+', line))
                                    if iops:
                                        update_list.append(int(iops[1]))
                                # 判断条件是否满足，获取AVG等数据
                                elif 'write lantencies (us)' in line:
                                    print(line)
                                    for line_data in line.split(','):
                                        # print(line_data.split(':')[-1])
                                        update_list.append(
                                            float(line_data.split(':')[-1]))
                        update_all_name.append(update_list)
                    print(update_all_name)

                    sheet_update = workbook.add_sheet('update')
                    for col, colum in enumerate(title_list):
                        sheet_update.write(0, col, colum)
                    for col, update_sheet in enumerate(update_all_name):
                        for col1, update in enumerate(update_sheet):
                            sheet_update.write(col+1, col1, update)


                    scan_all_name = []
                    for scan_name in scan_data:
                        print(scan_name)
                        scan_list = []
                        scan_list.append('sorted')
                        scan_list.append('scan')
                        values = re.findall(r'\d+', scan_name)
                        scan_list.append(int(values[0]))    # 添加value_size
                        scan_list.append(int(values[1]))    # 添加bench_threads
                        # 添加instance_threads
                        scan_list.append(int(values[1]))

                        with open(file_path + '/' + folder + '/' + scan_name, 'r') as f:
                            for line in f.readlines():
                                # 判断条件是否满足，获取IOPS
                                
                                if 'read ops' in line and 'write ops' in line:
                                
                                    iops = (re.findall(r'\d+', line))
                                    if iops:
                                        scan_list.append(int(iops[0]))
                                # 判断条件是否满足，获取AVG等数据
                                elif 'read lantencies (us)' in line:
                                
                                    for line_data in line.split(','):
                                        # print(line_data.split(':')[-1])
                                        scan_list.append(
                                            float(line_data.split(':')[-1]))
                        scan_all_name.append(scan_list)
                    # print(scan_all_name)

                    sheet_scan = workbook.add_sheet('scan')
                    for col, colum in enumerate(title_scan):
                        sheet_scan.write(0, col, colum)
                    for col, scan_sheet in enumerate(scan_all_name):
                        for col1, scan in enumerate(scan_sheet):
                            sheet_scan.write(col+1, col1, scan)

                    ru91_all_name = []
                    for ru91_name in ru91_data:
                        ru91_list = []
                        ru91_list.append('sorted')
                        ru91_list.append('ru91')
                        values = re.findall(r'\d+', ru91_name)
                        ru91_list.append(int(values[0]))    # 添加value_size
                        ru91_list.append(int(values[1]))    # 添加bench_threads
                        # 添加instance_threads
                        ru91_list.append(int(values[1]))

                        with open(file_path + '/' + folder + '/' + ru91_name, 'r') as f:
                            for line in f.readlines():
                                # 判断条件是否满足，获取IOPS
                                if 'read ops' in line and 'write ops' in line:
                                    iops = (re.findall(r'\d+', line))
                                    if iops:
                                        ru91_list.append(int(iops[0]))
                                # 判断条件是否满足，获取AVG等数据
                                elif 'read lantencies (us)' in line:
                                    for line_data in line.split(','):
                                        # print(line_data.split(':')[-1])
                                        ru91_list.append(
                                            float(line_data.split(':')[-1]))
                                elif 'write lantencies (us)' in line:
                                    ru91_list.append(int(iops[1]))
                                    for line_data in line.split(','):
                                        # print(line_data.split(':')[-1])
                                        ru91_list.append(
                                            float(line_data.split(':')[-1]))
                        ru91_all_name.append(ru91_list)
                    # print(ru91_all_name)

                    sheet_ru91 = workbook.add_sheet('ru91')
                    for col, colum in enumerate(title_ru91):
                        sheet_ru91.write(0, col, colum)
                    for col, ru91_sheet in enumerate(ru91_all_name):
                        for col1, ru91 in enumerate(ru91_sheet):
                            sheet_ru91.write(col+1, col1, ru91)

                    fill_all_name = []
                    for fill_name in fill_data:
                        fill_list = []
                        fill_list.append('sorted')
                        fill_list.append('fill')
                        values = re.findall(r'\d+', fill_name)
                        fill_list.append(int(values[0]))    # 添加value_size
                        fill_list.append(int(values[1]))    # 添加bench_threads
                        # 添加instance_threads
                        fill_list.append(int(values[1]))

                        with open(file_path + '/' + folder + '/' + fill_name, 'r') as f:
                            for line in f.readlines():
                                # 判断条件是否满足，获取IOPS
                                if 'read ops' in line and 'write ops' in line:
                                    iops = (re.findall(r'\d+', line))
                                    if iops:
                                        fill_list.append(int(iops[1]))
                                # 判断条件是否满足，获取AVG等数据
                                elif 'write lantencies (us)' in line:
                                    for line_data in line.split(','):
                                        # print(line_data.split(':')[-1])
                                        fill_list.append(
                                            float(line_data.split(':')[-1]))
                        fill_all_name.append(fill_list)
                    # print(fill_all_name)

                    sheet_fill = workbook.add_sheet('fill')
                    for col, colum in enumerate(title_list):
                        sheet_fill.write(0, col, colum)
                    for col, fill_sheet in enumerate(fill_all_name):
                        for col1, fill in enumerate(fill_sheet):
                            sheet_fill.write(col+1, col1, fill)
                    
                    read_all_name = []
                    # print(read_data)
                    for read_name in read_data:
                        read_list = []
                        read_list.append('sorted')
                        read_list.append('read')
                        values = re.findall(r'\d+', read_name)
                        read_list.append(int(values[0]))    # 添加value_size
                        read_list.append(int(values[1]))    # 添加bench_threads
                        # 添加instance_threads
                        read_list.append(int(values[1]))

                        with open(file_path + '/' + folder + '/' + read_name, 'r') as f:
                            for line in f.readlines():
                                # 判断条件是否满足，获取IOPS
                                if 'read ops' in line and 'write ops' in line:
                                    iops = (re.findall(r'\d+', line))
                                    if iops:
                                        read_list.append(int(iops[0]))
                                # 判断条件是否满足，获取AVG等数据
                                elif 'read lantencies (us)' in line:
                                    for line_data in line.split(','):
                                        # print(line_data.split(':')[-1])
                                        read_list.append(
                                            float(line_data.split(':')[-1]))
                        read_all_name.append(read_list)
                    # print(read_all_name)
                    sheet_read = workbook.add_sheet('read')
                    for col, colum in enumerate(title_scan):
                        sheet_read.write(0, col, colum)
                    for col1, read_sheet in enumerate(read_all_name):
                        for col2, read in enumerate(read_sheet):
                            sheet_read.write(col1+1, col2, read)
                
                    insert_all_name = []
                    for insert_name in insert_data:

                        insert_list = []
                        insert_list.append('sorted')
                        insert_list.append('insert')
                        values = re.findall(r'\d+', insert_name)
                        insert_list.append(int(values[0]))    # 添加value_size
                        insert_list.append(int(values[1]))    # 添加bench_threads
                        # 添加instance_threads
                        insert_list.append(int(values[1]))

                        with open(file_path + '/' + folder + '/' + insert_name, 'r') as f:
                            for line in f.readlines():
                                # 判断条件是否满足，获取IOPS
                                if 'read ops' in line and 'write ops' in line:
                                    iops = (re.findall(r'\d+', line))
                                    if iops:
                                        insert_list.append(int(iops[1]))
                                # 判断条件是否满足，获取AVG等数据
                                elif 'write lantencies (us)' in line:
                                    for line_data in line.split(','):
                                        # print(line_data.split(':')[-1])
                                        insert_list.append(
                                            float(line_data.split(':')[-1]))
                        insert_all_name.append(insert_list)
                    # print(insert_all_name)
                    sheet_insert = workbook.add_sheet('insert')
                    for col, colum in enumerate(title_list):
                        sheet_insert.write(0, col, colum)
                    for col1, insert_sheet in enumerate(insert_all_name):
                        for col2, insert in enumerate(insert_sheet):
                            sheet_insert.write(col1+1, col2, insert)
            
                    workbook.save(save_path + '/' +
                                  excel_name + '_sorted' + '.csv')
                elif 'string' in save_data[0]:
                    # print('string')
                    fill_data = []
                    insert_data = []
                    read_data = []
                    ru91_data = []
                    scan_data = []
                    update_data = []
                    for log_name in save_data:
                        # print(log_name.split('_'))
                        if 'fill' in log_name.split('_')[2]:
                            fill_data.append(log_name)
                        elif 'insert' in log_name.split('_')[2]:
                            insert_data.append(log_name)
                        elif 'read' in log_name.split('_')[2]:
                            read_data.append(log_name)
                        elif 'ru91' in log_name.split('_')[2]:
                            ru91_data.append(log_name)
                        elif 'scan' in log_name.split('_')[2]:
                            scan_data.append(log_name)
                        elif 'update' in log_name.split('_')[2]:
                            update_data.append(log_name)

                    update_all_name = []
                    for update_name in update_data:
                        print(update_name)
                        update_list = []
                        update_list.append('string')
                        update_list.append('update')
                        values = re.findall(r'\d+', update_name)
                        update_list.append(int(values[0]))    # 添加value_size
                        update_list.append(int(values[1]))    # 添加bench_threads
                        # 添加instance_threads
                        update_list.append(int(values[1]))

                        with open(file_path + '/' + folder + '/' + update_name, 'r') as f:
                            for line in f.readlines():
                                # 判断条件是否满足，获取IOPS

                                if 'read ops' in line and 'write ops' in line:
                                    print(line)
                                    iops = (re.findall(r'\d+', line))
                                    if iops:
                                        update_list.append(int(iops[1]))
                                # 判断条件是否满足，获取AVG等数据
                                elif 'write lantencies (us)' in line:
                                    print(line)
                                    for line_data in line.split(','):
                                        # print(line_data.split(':')[-1])
                                        update_list.append(
                                            float(line_data.split(':')[-1]))
                        update_all_name.append(update_list)
                    print(update_all_name)

                    sheet_update = workbook.add_sheet('update')
                    for col, colum in enumerate(title_list):
                        sheet_update.write(0, col, colum)
                    for col, update_sheet in enumerate(update_all_name):
                        for col1, update in enumerate(update_sheet):
                            sheet_update.write(col+1, col1, update)

                    scan_all_name = []
                    for scan_name in scan_data:
                        print(scan_name)
                        scan_list = []
                        scan_list.append('string')
                        scan_list.append('scan')
                        values = re.findall(r'\d+', scan_name)
                        scan_list.append(int(values[0]))    # 添加value_size
                        scan_list.append(int(values[1]))    # 添加bench_threads
                        # 添加instance_threads
                        scan_list.append(int(values[1]))

                        with open(file_path + '/' + folder + '/' + scan_name, 'r') as f:
                            for line in f.readlines():
                                # 判断条件是否满足，获取IOPS

                                if 'read ops' in line and 'write ops' in line:

                                    iops = (re.findall(r'\d+', line))
                                    if iops:
                                        scan_list.append(int(iops[0]))
                                # 判断条件是否满足，获取AVG等数据
                                elif 'read lantencies (us)' in line:

                                    for line_data in line.split(','):
                                        # print(line_data.split(':')[-1])
                                        scan_list.append(
                                            float(line_data.split(':')[-1]))
                        scan_all_name.append(scan_list)
                    # print(scan_all_name)

                    sheet_scan = workbook.add_sheet('scan')
                    for col, colum in enumerate(title_scan):
                        sheet_scan.write(0, col, colum)
                    for col, scan_sheet in enumerate(scan_all_name):
                        for col1, scan in enumerate(scan_sheet):
                            sheet_scan.write(col+1, col1, scan)

                    ru91_all_name = []
                    for ru91_name in ru91_data:
                        ru91_list = []
                        ru91_list.append('string')
                        ru91_list.append('ru91')
                        values = re.findall(r'\d+', ru91_name)
                        ru91_list.append(int(values[0]))    # 添加value_size
                        ru91_list.append(int(values[1]))    # 添加bench_threads
                        # 添加instance_threads
                        ru91_list.append(int(values[1]))

                        with open(file_path + '/' + folder + '/' + ru91_name, 'r') as f:
                            for line in f.readlines():
                                # 判断条件是否满足，获取IOPS
                                if 'read ops' in line and 'write ops' in line:
                                    iops = (re.findall(r'\d+', line))
                                    if iops:
                                        ru91_list.append(int(iops[0]))
                                # 判断条件是否满足，获取AVG等数据
                                elif 'read lantencies (us)' in line:
                                    for line_data in line.split(','):
                                        # print(line_data.split(':')[-1])
                                        ru91_list.append(
                                            float(line_data.split(':')[-1]))
                                elif 'write lantencies (us)' in line:
                                    ru91_list.append(int(iops[1]))
                                    for line_data in line.split(','):
                                        # print(line_data.split(':')[-1])
                                        ru91_list.append(
                                            float(line_data.split(':')[-1]))
                        ru91_all_name.append(ru91_list)
                    # print(ru91_all_name)

                    sheet_ru91 = workbook.add_sheet('ru91')
                    for col, colum in enumerate(title_ru91):
                        sheet_ru91.write(0, col, colum)
                    for col, ru91_sheet in enumerate(ru91_all_name):
                        for col1, ru91 in enumerate(ru91_sheet):
                            sheet_ru91.write(col+1, col1, ru91)

                    fill_all_name = []
                    for fill_name in fill_data:
                        fill_list = []
                        fill_list.append('string')
                        fill_list.append('fill')
                        values = re.findall(r'\d+', fill_name)
                        fill_list.append(int(values[0]))    # 添加value_size
                        fill_list.append(int(values[1]))    # 添加bench_threads
                        # 添加instance_threads
                        fill_list.append(int(values[1]))

                        with open(file_path + '/' + folder + '/' + fill_name, 'r') as f:
                            for line in f.readlines():
                                # 判断条件是否满足，获取IOPS
                                if 'read ops' in line and 'write ops' in line:
                                    iops = (re.findall(r'\d+', line))
                                    if iops:
                                        fill_list.append(int(iops[1]))
                                # 判断条件是否满足，获取AVG等数据
                                elif 'write lantencies (us)' in line:
                                    for line_data in line.split(','):
                                        # print(line_data.split(':')[-1])
                                        fill_list.append(
                                            float(line_data.split(':')[-1]))
                        fill_all_name.append(fill_list)
                    # print(fill_all_name)

                    sheet_fill = workbook.add_sheet('fill')
                    for col, colum in enumerate(title_list):
                        sheet_fill.write(0, col, colum)
                    for col, fill_sheet in enumerate(fill_all_name):
                        for col1, fill in enumerate(fill_sheet):
                            sheet_fill.write(col+1, col1, fill)

                    read_all_name = []
                    # print(read_data)
                    for read_name in read_data:
                        read_list = []
                        read_list.append('string')
                        read_list.append('read')
                        values = re.findall(r'\d+', read_name)
                        read_list.append(int(values[0]))    # 添加value_size
                        read_list.append(int(values[1]))    # 添加bench_threads
                        # 添加instance_threads
                        read_list.append(int(values[1]))

                        with open(file_path + '/' + folder + '/' + read_name, 'r') as f:
                            for line in f.readlines():
                                # 判断条件是否满足，获取IOPS
                                if 'read ops' in line and 'write ops' in line:
                                    iops = (re.findall(r'\d+', line))
                                    if iops:
                                        read_list.append(int(iops[0]))
                                # 判断条件是否满足，获取AVG等数据
                                elif 'read lantencies (us)' in line:
                                    for line_data in line.split(','):
                                        # print(line_data.split(':')[-1])
                                        read_list.append(
                                            float(line_data.split(':')[-1]))
                        read_all_name.append(read_list)
                    # print(read_all_name)
                    sheet_read = workbook.add_sheet('read')
                    for col, colum in enumerate(title_scan):
                        sheet_read.write(0, col, colum)
                    for col1, read_sheet in enumerate(read_all_name):
                        for col2, read in enumerate(read_sheet):
                            sheet_read.write(col1+1, col2, read)
                  
                    insert_all_name = []
                    for insert_name in insert_data:

                        insert_list = []
                        insert_list.append('string')
                        insert_list.append('insert')
                        values = re.findall(r'\d+', insert_name)
                        insert_list.append(int(values[0]))    # 添加value_size
                        insert_list.append(int(values[1]))    # 添加bench_threads
                        # 添加instance_threads
                        insert_list.append(int(values[1]))

                        with open(file_path + '/' + folder + '/' + insert_name, 'r') as f:
                            for line in f.readlines():
                                # 判断条件是否满足，获取IOPS
                                if 'read ops' in line and 'write ops' in line:
                                    iops = (re.findall(r'\d+', line))
                                    if iops:
                                        insert_list.append(int(iops[1]))
                                # 判断条件是否满足，获取AVG等数据
                                elif 'write lantencies (us)' in line:
                                    for line_data in line.split(','):
                                        # print(line_data.split(':')[-1])
                                        insert_list.append(
                                            float(line_data.split(':')[-1]))
                        insert_all_name.append(insert_list)
                    # print(insert_all_name)
                    sheet_insert = workbook.add_sheet('insert')
                    for col, colum in enumerate(title_list):
                        sheet_insert.write(0, col, colum)
                    for col1, insert_sheet in enumerate(insert_all_name):
                        for col2, insert in enumerate(insert_sheet):
                            sheet_insert.write(col1+1, col2, insert)
                    workbook.save(save_path + '/' +
                                  excel_name + '_string'  + '.csv')
        else:
            continue
    

if __name__ == '__main__':
    kvdk_p2ca_data()

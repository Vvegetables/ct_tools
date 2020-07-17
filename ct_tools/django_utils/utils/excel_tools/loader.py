from openpyxl.reader.excel import load_workbook

def excel_loader(path: str, has_title: bool=False, sheet_name=None):
    """excel读取器，根据path将excel读入，has_title判断第一行是否为标题，返回数组信息和标题信息。
    """
    wb = load_workbook(path)
    if sheet_name is None:
        sheet = wb.active
    else:
        sheet = wb[sheet_name]
    
    title_list = []
    ret_list = []
    for i, line in enumerate(sheet.values, 1):
        if has_title:
            if i == 1:
                title_list = list(line)
                continue
            if title_list:
                temp_dict = dict(
                    (k, v)
                    for k, v in zip(title_list, line)
                )
                ret_list.append(temp_dict)
        else:
            ret_list.append(list(line))
    
    return ret_list, title_list

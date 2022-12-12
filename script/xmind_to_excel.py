from xmindparser import xmind_to_dictfrom openpyxl import WorkbookXMIND_FILE_PATH = '/Users/linzhongjie/Documents/爆米/测试用例/FMS2.4.xmind'OUTPUT_FILE_PATH = '/Users/linzhongjie/Documents/爆米/测试用例/'CASE_LEVEL = {    "priority-1": "P0",    "priority-2": "P1",    "priority-3": "P2",    "priority-4": "P3"}HEADER = ["一级模块", "二级模块", "三级模块", "四级模块", "用例名称", "优先级", "用例类型",          "前置条件", "步骤描述", "预期结果", "备注", "维护人"]def parse_case(parent_node, child, case_data):    """    解析用例    :param parent_node: 父节点的title    :param child: 子节点    :param case_data: 用于存放用例的list    """    case_detail = {        "module": parent_node,  # 用例模块        "title": child.get("title", ""),  # 用例标题        "priority": "",  # 优先级        "case_type": "功能测试",  # 用例类型，暂时写死功能测试，后面通过图标识别        "pre_condition": "无",  # 前置条件        "step": "",  # 步骤描述，暂时写死用例标题的下一级        "expect": ""  # 预期结果，暂时写死用例步骤的下一级    }    marker = [i for i in child.get("makers") if i in CASE_LEVEL]    if not marker:        raise Exception("优先级图例错误")    case_detail["priority"] = CASE_LEVEL[marker[0]]    for case in child["topics"]:        if case.get("makers"):            if case["makers"][0] == 'c_symbol_pen':                # 解析前置条件                case_detail["pre_condition"] = case["title"]                continue        case_detail["step"] = case.get("title", "")        case_detail["expect"] = case["topics"][0].get("title", "")    case_data.append(case_detail)def parse_module(parent_node, child, case_data):    """    解析模块    :param parent_node: 父节点 title    :param child: 子节点    :param case_data: 用于存放用例的list    """    parent_node = f"{parent_node}#{child.get('title')}"    # 递归遍历，解析子节点    for c in child["topics"]:        deal_parse(parent_node, c, case_data)def deal_parse(parent_node, child, case_data):    """    处理json对象的解析，按标记符区别用例和模块    :param parent_node: 根节点    :param child: 子节点    :param case_data: 解析出的用例存储list    """    if child.get("makers"):        # 当前层级存在标识符时，识别为用例，进入用例解析        parse_case(parent_node, child, case_data)    else:        # 不存在时，识别为模块，进入模块解析        parse_module(parent_node, child, case_data)def parse_xmind(xmind_data: dict):    """    解析xmind数据，    :param xmind_data: xmind文件解压后的json对象    """    case_data = []    root_node = xmind_data["title"]    for child in xmind_data["topics"]:        deal_parse(root_node, child, case_data)    return case_datadef write_excel(sheet_name: str, cases: list):    """    将解析好的dict 写入到 excel    :param sheet_name: 工作表名称, str 类型    :param cases: 解析的用例数据, list 类型    """    work_book = Workbook()    work_sheet = work_book.active    work_sheet.append(HEADER)    for case in cases:        row_data = []        module_list = case.get("module").split("#")        row_data.extend(module_list[1:5])  # 从画布的二级主题开始获取模块        # 模块不足4时，填充空字符        if len(row_data) < 4:            for i in range(4 - len(row_data)):                row_data.append("")        row_data.extend(            [                v for k, v in case.items()                if k != 'module'            ]        )        work_sheet.append(row_data)    return work_book.save(f"{OUTPUT_FILE_PATH}{sheet_name}.xlsx")def main():    raw_data = xmind_to_dict(XMIND_FILE_PATH)    rs = parse_xmind(raw_data[0]['topic'])    write_excel(raw_data[0]['topic']['title'], rs)if __name__ == '__main__':    main()
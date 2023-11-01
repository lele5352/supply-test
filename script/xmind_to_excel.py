import osimport tkinter as tkfrom tkinter import filedialogfrom xmindparser import xmind_to_dictfrom openpyxl import Workbookfrom utils.log_handler import logger# 解析标识字典CASE_MARKER = {    '前置条件': 'symbol-idea',    '优先级': {        "priority-1": "P0",        "priority-2": "P1",        "priority-3": "P2",        "priority-4": "P3"    }}# 用例类型字典，已根据 ones 支持的用例类型配置CASE_TYPE = {    '性能': '性能测试',    '功能': '功能测试',    '接口': '接口测试',    '安装': '安装部署',    '安全': '安全相关',    '配置': '配置相关',    '其他': '其他',    'default': '功能测试'}SPLIT_FLAG = chr(20)HEADER = ["一级模块", "二级模块", "三级模块", "四级模块", "用例名称", "优先级", "用例类型",          "前置条件", "步骤描述", "预期结果", "备注", "维护人"]def parse_case(parent_node, child, case_data):    """    解析用例    :param parent_node: 父节点的title    :param child: 子节点    :param case_data: 用于存放用例的list    """    case_detail = {        "module": parent_node,  # 用例模块        "title": child.get("title", ""),  # 用例标题        "priority": None,  # 优先级        "case_type": CASE_TYPE['default'],  # 用例类型，通过用例标题的标签识别，没有标签则默认功能测试        "pre_condition": None,  # 前置条件        "step": None,  # 步骤描述，取用例标题的下一级        "expect": None,  # 预期结果，取用例步骤的下一级        "tips": None, # 备注，取预期结果的下一级    }    marker = [i for i in child.get("makers") if i in CASE_MARKER['优先级']]    # 校验用例优先级    if not marker:        raise ValueError("优先级图例错误")    # 校验用例步骤    if not child.get("topics"):        raise ValueError(f"解析异常: {case_detail['title']} ，缺少用例步骤，请检查")    case_detail["priority"] = CASE_MARKER['优先级'][marker[0]]    if child.get('labels'):        label = child['labels'][0]        case_type = [CASE_TYPE[i] for i in CASE_TYPE if i in label]        try:            case_detail['case_type'] = case_type[0]        except IndexError:            logger.info(f'关键字: {label}，解析不到对应的用例类型，默认为功能测试')    for case in child["topics"]:        if case.get("makers"):            if case["makers"][0] == 'symbol-idea':                # 解析前置条件                case_detail["pre_condition"] = case["title"]                continue        # 解析用例步骤和预期结果        case_detail["step"] = case.get("title", "")        try:            case_detail["expect"] = case["topics"][0]["title"]        except (IndexError, KeyError):            raise ValueError(f"解析异常: {case_detail['title']} ，缺少预期结果，请检查")        else:            try:                # 解析备注                case_detail["tips"] = case["topics"][0]["topics"][0]["title"]            except (IndexError, KeyError):                pass    case_data.append(case_detail)def parse_module(parent_node, child, case_data):    """    解析模块    :param parent_node: 父节点 title    :param child: 子节点    :param case_data: 用于存放用例的list    """    parent_node = f"{parent_node}{SPLIT_FLAG}{child.get('title')}"    try:        # 递归遍历，解析子节点        for c in child["topics"]:            deal_parse(parent_node, c, case_data)    except KeyError:        logger.debug(f"当前节点 {child.get('title')} ，已遍历完子节点，未发现用例")        passdef deal_parse(parent_node, child, case_data):    """    处理json对象的解析，按标记符区别用例和模块    :param parent_node: 根节点    :param child: 子节点    :param case_data: 解析出的用例存储list    """    if child.get("makers"):        # 当前层级存在标识符时，识别为用例，进入用例解析        parse_case(parent_node, child, case_data)    else:        # 不存在时，识别为模块，进入模块解析        parse_module(parent_node, child, case_data)def parse_xmind(xmind_data: dict):    """    解析xmind数据，    :param xmind_data: xmind文件解压后的json对象    """    case_data = []    root_node = xmind_data["title"]    for child in xmind_data["topics"]:        deal_parse(root_node, child, case_data)    return case_datadef write_excel(sheet_name: str, cases: list, output_path: str):    """    将解析好的dict 写入到 excel    :param sheet_name: 工作表名称, str 类型    :param cases: 解析的用例数据, list 类型    :param output_path: 输入的excel文件保存路径    """    work_book = Workbook()    work_sheet = work_book.active    work_sheet.append(HEADER)    for case in cases:        row_data = []        module_list = case.get("module").split(SPLIT_FLAG)        row_data.extend(module_list[1:5])  # 从画布的二级主题开始获取模块，最多获取四级模块        # 模块不足四个时，填充空字符        if len(row_data) < 4:            for i in range(4 - len(row_data)):                row_data.append("")        row_data.extend(            [                v for k, v in case.items()                if k != 'module'            ]        )        work_sheet.append(row_data)    file_name = f"{sheet_name}.xlsx"    file_path = os.path.join(output_path, file_name)    logger.info('用例转换完成，文件输出路径：%s' % file_path)    return work_book.save(file_path)def browse_file():    """    执行文件选择    """    root = tk.Tk()    root.withdraw()    xmind_file_path = filedialog.askopenfilename(        title="选择XMind文件", filetypes=[("XMind Files", "*.xmind")]    )    return xmind_file_pathdef main():    xmind_path = browse_file()    if not xmind_path:        print("未选择XMind文件，退出程序")        return    # 获取所选文件的目录，用于输出excel文件    file_directory = os.path.dirname(xmind_path)    raw_data = xmind_to_dict(xmind_path)    rs = parse_xmind(raw_data[0]['topic'])    write_excel(raw_data[0]['topic']['title'], rs, file_directory)if __name__ == '__main__':    main()
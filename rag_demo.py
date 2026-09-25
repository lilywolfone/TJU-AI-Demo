import re

# 规则表：key 为字段名，value 为 (正则, 替换串)
FIELD_RULES = {
    "身份证": (r'\d{17}[\dXx]', '*' * 18),
    "手机号": (r'1[3-9]\d{9}', '*' * 11),
    "长数字": (r'(?<!\d)\d{8,12}(?!\d)', '****'),
    "姓名":   (r'(姓名[:：]?\s*)(\S)([^\s性别民族学院专业电话]*)', r'\1\2**'),
    "民族":   (r'(民族[:：]?\s*)\S+', r'\1**'),
    "学院":   (r'(学院[:：]?\s*).+?(?=\s*专业|\s*$)', r'\1**'),
    "专业":   (r'(专业[:：]?\s*).+?(?=\s*学院|\s*$)', r'\1**'),
}

# 执行顺序：先处理定长强特征（身份证/手机号），再处理字段类
ORDER = ["身份证", "手机号", "长数字", "姓名", "民族", "学院", "专业"]


def desensitize(text: str) -> str:
    for key in ORDER:
        pattern, repl = FIELD_RULES[key]
        text = re.sub(pattern, repl, text)
    return text
def test_desensitize():
    # 学院 / 专业
    assert "学院 **" in desensitize("学院 精密仪器与光电子工程学院")
    assert "专业 **" in desensitize("专业 测控技术与仪器")

    # 手机号
    assert "手机号 " + "*" * 11 in desensitize("手机号 13800138000")
    # 姓名
    assert desensitize("姓名 张三") != "姓名 张三"
              

    # 组合场景
    combo = "姓名 张三 民族 汉族 学院 精密仪器与光电子工程学院 专业 测控技术与仪器 手机号 13800138000"
    result = desensitize(combo)
    assert "张三" not in result
    assert "精密仪器与光电子工程学院" not in result    
    print(repr(result))
    assert "测控技术与仪器" not in result

    print("全部用例通过")


if __name__ == "__main__":
    test_desensitize()

    sample = "姓名 张三 民族 汉族 学院 精密仪器与光电子工程学院 专业 测控技术与仪器 手机号 13800138000"
    print("--- 原文 ---")
    print(sample)
    print("--- 脱敏后 ---")
    print(desensitize(sample))
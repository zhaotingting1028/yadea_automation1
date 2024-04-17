import random, string
import datetime
from Config import config


def getRandomPhone():
    """随机生成手机号码"""
    prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "150", "151", "152", "153",
               "155", "156", "157", "158", "159", "186", "187", "188"]
    return random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))

def getRandomvim():
    """固定车架号随机抽选"""
    prelist = config.vim_data
    return random.choice(prelist)

def gettime():
    """生成当前日期"""
    time = datetime.datetime.now().strftime('%Y-%m-%d')
    return time

def gettime_hh():
    """生成当前日期"""
    time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return time



def genPassword(length):
    """生成随机6位数字+字母的密码"""
    # 随机出数字的个数
    numOfNum = random.randint(1, length - 1)
    numOfLetter = length - numOfNum
    # 选中numOfNum个数字
    slcNum = [random.choice(string.digits) for i in range(numOfNum)]
    # 选中numOfLetter个字母
    slcLetter = [random.choice(string.ascii_letters) for i in range(numOfLetter)]
    # 打乱这个组合
    slcChar = slcNum + slcLetter
    random.shuffle(slcChar)
    # 生成密码
    genPwd = ''.join([i for i in slcChar])
    return genPwd


def genNumByLength(length):
    """生成指定位数的随机数"""
    num = ""
    while length > 0:
        num += str(random.randint(0, 9))
        length = length - 1
    return num




if __name__ == "__main__":
    print(genNumByLength(9))
    print(genPassword(9))



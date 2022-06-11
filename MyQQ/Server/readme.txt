状态码：
    1：成功
    2：用户名或密码错误
    3：未知错误


数据包：
    C-->S:
        request
        request需要的参数
    S-->C:
        request
        状态码
        若成功，则有结果
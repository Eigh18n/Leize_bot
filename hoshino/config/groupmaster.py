import random

increase_welcome = {
    "default": random.choice(["欢迎，你是，「卢皮卡」吗？", "欢迎入群，我是雷泽", "欢迎，一起狩猎吗？"])
}

join_approve = {
    1000000: {
        "keywords": ["入群暗号"],
        "reject_when_not_match": True
    },
}

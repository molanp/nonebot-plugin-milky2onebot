# nonebot-plugin-milky2onebot

一个将 Milky 协议转换到 Onebot 协议的 Nonebot 插件

> [!IMPORTANT]
>
> 当前只支持 WebSocket 的 Milky 协议转换
>

## 使用

此插件会自动链接 Onebot 的 WebSocket 服务器，并自动将 Milky 协议的请求转发给 Onebot，请同时注册 Onebot 适配器并正确填写配置

### MILKY2OB_CLIENTS

MILKY 连接配置

```
MILKY2OB_CLIENTS='
[
  {
    "host": "localhost",
    "port": "8080",
    "access_token": "xxx"
  }
]
'
```

`host` 与 `port` 为 Milky 协议端设置的监听地址与端口，

`access_token` 为可选项，具体情况以 Milky 协议端为准。

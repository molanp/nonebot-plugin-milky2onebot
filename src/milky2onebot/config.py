import nonebot
from yarl import URL
from pydantic import Field, BaseModel


class ClientInfo(BaseModel):
    host: str = "localhost"
    """Milky 协议端地址"""
    port: int = 8080
    """Milky 协议端端口"""
    access_token: str | None = None
    """Milky 协议端 验证密钥"""

    def get_url(self, route: str) -> str:
        return str(URL(f"http://{self.host}:{self.port}") / "api" / route)

    def ws_url(self):
        return f"ws://{self.host}:{self.port}/event"


class Config(BaseModel):
    MILKY2OB_CLIENTS: list[ClientInfo] = Field(default_factory=list)
    """MILKY连接配置"""
    ONEBOT_ACCESS_TOKEN: str | None = None
    """访问令牌"""
    ONEBOT_V11_ACCESS_TOKEN: str | None = None
    """v11访问令牌"""


plugin_config: Config = nonebot.get_plugin_config(Config)
system_config = nonebot.get_driver().config

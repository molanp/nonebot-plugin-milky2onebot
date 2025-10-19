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

    def get_headers(self) -> dict[str, str]:
        if self.access_token is None:
            return {}
        return {"Authorization": f"Bearer {self.access_token}"}


class Config(BaseModel):
    MILKY2OB_CLIENTS: list[ClientInfo] = Field(default_factory=list)
    """MILKY连接配置"""


plugin_config: Config = nonebot.get_plugin_config(Config)
system_config = nonebot.get_driver().config
onebot_base = f"ws://{system_config.host}:{system_config.port}/onebot/"

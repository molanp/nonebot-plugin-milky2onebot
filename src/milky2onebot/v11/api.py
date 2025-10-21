import inspect

from nonebot import logger


async def getApiData(api: str, params: dict = {}, uin: int = 0):

    class publicApi:
        @staticmethod
        def get_login_info():
            pass

    if not hasattr(publicApi, api):
        logger.warning(f"[ws-plugin] 未适配的api: {api}")
        return
    method = getattr(publicApi, api)

    if inspect.iscoroutinefunction(method):
        return await method(**params)
    else:
        return method(**params)

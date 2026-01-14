import logging
from typing import Optional, Any

logger = logging.getLogger(__name__)


class Constant:

    HTTP_TAG: str = "http://"
    HTTPS_TAG: str = "https://"

    EMPTY: str =''


class StrUtil:

    @classmethod
    def is_none(cls, value: Optional[Any]):
        return True if value is None else False

    @classmethod
    def is_not_none(cls, value: Optional[Any]):
        return cls.is_none(value)

    @classmethod
    def is_not_blank(cls, value: Optional[str]) -> bool:
        return not cls.is_blank(value)

    @classmethod
    def is_blank(cls, value: Optional[str]) -> bool:
        if value is None:
            return True
        value = cls.strip(value)
        if len(value) == 0:
            return True
        return False

    @classmethod
    def strip(cls, value: Optional[str] = None) -> Optional[str]:
        if value is None:
            return None
        return value.strip()

    @classmethod
    def remove_http(cls, value: Optional[str] = None) -> Optional[str]:
        value = cls.strip(value)
        if value is None:
            return None
        if value.startswith(Constant.HTTPS_TAG):
            value = value.replace(Constant.HTTPS_TAG, Constant.EMPTY)
        if value.startswith(Constant.HTTP_TAG):
            value = value.replace(Constant.HTTP_TAG, Constant.EMPTY)
        return value

    @classmethod
    def write_file(cls, value: str, file_path: str):
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(value)
                f.flush()
        except Exception as e:
            logger.error(f'写入文件错误, file_path:{file_path}', exc_info=True)

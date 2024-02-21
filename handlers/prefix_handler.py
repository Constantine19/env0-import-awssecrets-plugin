import re

from . import _handler


class PrefixHandler(
    _handler.BaseHandler,
):
    def __init__(
        self, 
        prefix,
    ):
        self.prefix = prefix
        self.key_extraction_pattern = rf'\$\{{{self.prefix}:(.*?)\}}'
        self.is_prefixed_pattern = r'\$\{([^:]+):[^}]*\}'
            
    def is_prefixed(
        self, 
        value,
    ):
        return bool(
            re.match(
                self.is_prefixed_pattern, 
                value,
            )
        )
    
    def extract_secret_key(
        self, 
        prefix_embedded_value,
    ):
        match = re.search(
            self.key_extraction_pattern, 
            prefix_embedded_value,
        )
        if match:
            return match.group(1)
        return None

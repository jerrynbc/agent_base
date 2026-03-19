class Config:
    # 默认配置
    DEFAULT_API_BASE = "https://api.openai.com/v1"
    DEFAULT_MODEL = "gpt-3.5-turbo"
    DEFAULT_TEMPERATURE = 0.7
    DEFAULT_MAX_TOKENS = 1000
    DEFAULT_SYSTEM_PROMPT = "You are a helpful assistant."
    
    # 运行时配置
    def __init__(self):
        self.api_base = self.DEFAULT_API_BASE
        self.api_key = None
        self.model = self.DEFAULT_MODEL
        self.temperature = self.DEFAULT_TEMPERATURE
        self.max_tokens = self.DEFAULT_MAX_TOKENS
        self.system_prompt = self.DEFAULT_SYSTEM_PROMPT
    
    def update_config(self, config_dict):
        """更新配置"""
        for key, value in config_dict.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)
    
    def get_config(self):
        """获取当前配置"""
        return {
            "api_base": self.api_base,
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "system_prompt": self.system_prompt
        }

# 创建全局配置实例
config = Config()
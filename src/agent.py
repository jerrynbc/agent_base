from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from config import config

class LangChainAgent:
    def __init__(self):
        self.llm = None
        self.chat_history = []
        self.update_llm()
    
    def update_llm(self):
        """更新语言模型"""
        if config.api_key:
            self.llm = ChatOpenAI(
                base_url=config.api_base,
                api_key=config.api_key,
                model=config.model,
                temperature=config.temperature,
                max_tokens=config.max_tokens
            )
    
    def update_config(self, config_dict):
        """更新配置"""
        config.update_config(config_dict)
        if 'api_key' in config_dict or 'api_base' in config_dict or 'model' in config_dict:
            self.update_llm()
    
    def clear_chat_history(self):
        """清空对话历史"""
        self.chat_history = []
    
    def add_message(self, message):
        """添加消息到对话历史"""
        self.chat_history.append(message)
    
    def get_chat_history(self):
        """获取对话历史"""
        return self.chat_history
    
    def generate_response(self, user_input):
        """生成响应"""
        if not self.llm:
            return "请先配置API密钥和模型设置"
        
        # 构建消息列表
        messages = [SystemMessage(content=config.system_prompt)]
        
        # 添加历史消息
        for msg in self.chat_history:
            if msg['role'] == 'user':
                messages.append(HumanMessage(content=msg['content']))
            elif msg['role'] == 'assistant':
                messages.append(AIMessage(content=msg['content']))
        
        # 添加当前用户输入
        messages.append(HumanMessage(content=user_input))
        
        # 生成响应
        try:
            response = self.llm.invoke(messages)
            response_content = response.content
            
            # 添加到对话历史
            self.add_message({"role": "user", "content": user_input})
            self.add_message({"role": "assistant", "content": response_content})
            
            return response_content
        except Exception as e:
            return f"错误: {str(e)}"

# 创建全局智能体实例
agent = LangChainAgent()
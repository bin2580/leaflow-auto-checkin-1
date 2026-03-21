#!/usr/bin/env python3
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_environment_variables():
    """
    提取脚本所需的所有环境变量，并进行合法性检查
    返回：包含所有环境变量的字典
    """
    env_vars = {
        # 核心账号配置
        "LEAFLOW_ACCOUNTS": os.getenv('LEAFLOW_ACCOUNTS', ''),
        "LEAFLOW_EMAIL": os.getenv('LEAFLOW_EMAIL', ''),
        "LEAFLOW_PASSWORD": os.getenv('LEAFLOW_PASSWORD', ''),
        
        # 通知配置
        "TELEGRAM_BOT_TOKEN": os.getenv('TELEGRAM_BOT_TOKEN', ''),
        "TELEGRAM_CHAT_ID": os.getenv('TELEGRAM_CHAT_ID', ''),
        
        # 运行环境标识
        "GITHUB_ACTIONS": os.getenv('GITHUB_ACTIONS', 'false')
    }
    
    # 验证账号配置是否有效
    if not env_vars["LEAFLOW_ACCOUNTS"] and (not env_vars["LEAFLOW_EMAIL"] or not env_vars["LEAFLOW_PASSWORD"]):
        raise ValueError(
            "环境变量配置错误！请至少配置以下其中一种：\n"
            "1. LEAFLOW_ACCOUNTS (多账号): email1:pass1,email2:pass2\n"
            "2. LEAFLOW_EMAIL + LEAFLOW_PASSWORD (单账号)"
        )
    
    # 验证Telegram配置（如果填写了其中一个，另一个也必须填写）
    if (env_vars["TELEGRAM_BOT_TOKEN"] and not env_vars["TELEGRAM_CHAT_ID"]) or \
       (not env_vars["TELEGRAM_BOT_TOKEN"] and env_vars["TELEGRAM_CHAT_ID"]):
        logger.warning("警告：Telegram配置不完整！请同时填写TELEGRAM_BOT_TOKEN和TELEGRAM_CHAT_ID")
    
    logger.info("环境变量提取完成：")
    logger.info(f"- 多账号配置: {'已设置' if env_vars['LEAFLOW_ACCOUNTS'] else '未设置'}")
    logger.info(f"- 单账号配置: {'已设置' if env_vars['LEAFLOW_EMAIL'] and env_vars['LEAFLOW_PASSWORD'] else '未设置'}")
    logger.info(f"- Telegram通知: {'已配置' if env_vars['TELEGRAM_BOT_TOKEN'] and env_vars['TELEGRAM_CHAT_ID'] else '未配置'}")
    logger.info(f"- 运行环境: {'GitHub Actions' if env_vars['GITHUB_ACTIONS'] == 'true' else '本地环境'}")
    
    return env_vars

# ------------------------------
# 使用示例
# ------------------------------
if __name__ == "__main__":
    try:
        # 提取并验证环境变量
        env_config = extract_environment_variables()
        
        # 访问提取的环境变量
        print(f"\n=== 提取的环境变量信息 ===")
        print(f"多账号配置: {env_config['LEAFLOW_ACCOUNTS'][:50]}..." if env_config['LEAFLOW_ACCOUNTS'] else "无")
        print(f"单账号邮箱: {env_config['LEAFLOW_EMAIL']}")
        print(f"Telegram Bot Token: {env_config['TELEGRAM_BOT_TOKEN'][:10]}..." if env_config['TELEGRAM_BOT_TOKEN'] else "无")
        print(f"运行环境: {'GitHub Actions' if env_config['GITHUB_ACTIONS'] == 'true' else '本地'}")
        
    except ValueError as e:
        logger.error(f"环境变量验证失败: {e}")
    except Exception as e:
        logger.error(f"提取环境变量时出错: {e}")

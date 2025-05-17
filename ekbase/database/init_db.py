import os
from ekbase.database.utils import Database

def init_database():
    """初始化数据库，创建必要的表"""
    # 配置数据库文件路径
    # 使用config/settings.py中的配置
    
    db = Database()
    
    # 读取SQL文件
    sql_file = os.path.join(os.path.dirname(__file__), 'sql', 'init.sql')
    with open(sql_file, 'r', encoding='utf-8') as f:
        sql_content = f.read()
    
    # 分割SQL语句（以分号结尾的语句）
    sql_commands = [cmd.strip() for cmd in sql_content.split(';') if cmd.strip()]
    
    # 执行每条SQL命令
    try:
        for command in sql_commands:
            if command:  # 确保不是空命令
                db.execute(command)
        db.commit()
        print(f"数据库初始化成功，数据库文件位置: {db.db_path}")
    except Exception as e:
        db.rollback()
        print(f"数据库初始化失败: {str(e)}")
    finally:
        db.close()
#!/usr/bin/env python3
"""
Database Initialization Script
数据库初始化脚本

This script provides commands to initialize, reset, and manage the database.
本脚本提供初始化、重置和管理数据库的命令。
"""

import sys
import os
from app import create_app
from models import db

def init_database():
    """
    Initialize the database by creating all tables.
    通过创建所有表来初始化数据库。
    """
    app = create_app()
    with app.app_context():
        print("Creating database tables...")
        print("正在创建数据库表...")
        db.create_all()
        print("✓ Database tables created successfully!")
        print("✓ 数据库表创建成功！")
        print(f"\nDatabase location: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print(f"数据库位置: {app.config['SQLALCHEMY_DATABASE_URI']}")

def drop_database():
    """
    Drop all database tables.
    删除所有数据库表。
    
    WARNING: This will delete all data!
    警告：这将删除所有数据！
    """
    app = create_app()
    with app.app_context():
        print("WARNING: This will delete all data!")
        print("警告：这将删除所有数据！")
        confirm = input("Are you sure? Type 'yes' to confirm: ")
        if confirm.lower() == 'yes':
            print("Dropping all tables...")
            print("正在删除所有表...")
            db.drop_all()
            print("✓ All tables dropped successfully!")
            print("✓ 所有表删除成功！")
        else:
            print("Operation cancelled.")
            print("操作已取消。")

def reset_database():
    """
    Reset the database by dropping and recreating all tables.
    通过删除并重新创建所有表来重置数据库。
    
    WARNING: This will delete all data!
    警告：这将删除所有数据！
    """
    app = create_app()
    with app.app_context():
        print("WARNING: This will delete all data and reset the database!")
        print("警告：这将删除所有数据并重置数据库！")
        confirm = input("Are you sure? Type 'yes' to confirm: ")
        if confirm.lower() == 'yes':
            print("Dropping all tables...")
            print("正在删除所有表...")
            db.drop_all()
            print("Creating new tables...")
            print("正在创建新表...")
            db.create_all()
            print("✓ Database reset successfully!")
            print("✓ 数据库重置成功！")
        else:
            print("Operation cancelled.")
            print("操作已取消。")

def show_info():
    """
    Display database information.
    显示数据库信息。
    """
    app = create_app()
    with app.app_context():
        print("\n" + "="*60)
        print("Database Information / 数据库信息")
        print("="*60)
        print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print(f"数据库URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print("\nConfigured Tables / 配置的表:")
        print("-" * 60)
        
        # Try to get table information
        try:
            from models import User, Device, TrafficLog, Alert, PacketCapture
            tables = [
                ("users", "用户表", User),
                ("devices", "设备表", Device),
                ("traffic_logs", "流量日志表", TrafficLog),
                ("alerts", "警报表", Alert),
                ("packet_captures", "数据包捕获表", PacketCapture)
            ]
            
            for table_name, chinese_name, model in tables:
                print(f"  • {table_name:20} ({chinese_name})")
            
            print("\n" + "="*60)
        except ImportError as e:
            print(f"Error: Could not import database models: {e}")
            print(f"错误：无法导入数据库模型: {e}")
            print("Please ensure models.py is properly configured.")
            print("请确保 models.py 已正确配置。")
        except Exception as e:
            print(f"Error getting table information: {e}")
            print(f"获取表信息时出错: {e}")

def print_usage():
    """
    Print usage information.
    打印使用说明。
    """
    print("\n" + "="*60)
    print("Database Management Tool / 数据库管理工具")
    print("="*60)
    print("\nUsage / 用法:")
    print("  python init_db.py [command]")
    print("\nCommands / 命令:")
    print("  init     - Initialize database (create tables)")
    print("           - 初始化数据库（创建表）")
    print("  drop     - Drop all tables (WARNING: deletes all data)")
    print("           - 删除所有表（警告：删除所有数据）")
    print("  reset    - Reset database (drop and recreate tables)")
    print("           - 重置数据库（删除并重新创建表）")
    print("  info     - Show database information")
    print("           - 显示数据库信息")
    print("  help     - Show this help message")
    print("           - 显示此帮助信息")
    print("\nExamples / 示例:")
    print("  python init_db.py init")
    print("  python init_db.py info")
    print("  python init_db.py reset")
    print("\n" + "="*60 + "\n")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(0)
    
    command = sys.argv[1].lower()
    
    if command == 'init':
        init_database()
    elif command == 'drop':
        drop_database()
    elif command == 'reset':
        reset_database()
    elif command == 'info':
        show_info()
    elif command == 'help':
        print_usage()
    else:
        print(f"Unknown command: {command}")
        print(f"未知命令: {command}")
        print_usage()
        sys.exit(1)

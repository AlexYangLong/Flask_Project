from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from QA_Platform import app
from exts import db
from models import User, Question, Answer

manager = Manager(app=app)

# 使用Migrate绑定app和db
migrate = Migrate(app=app, db=db)

# 添加迁移脚本命令到manager中
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

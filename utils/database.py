from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy import LONGBLOB
from typing import Optional
import os

load_dotenv()

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 定义 User 表模型
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    userid = Column(String(255), unique=True, index=True)  # 用户邮箱
    password = Column(String(255))  # 用户密码（加密存储）
    level = Column(Integer, default=1)  # 用户等级（1：编外人员，2：干事，3：部长及以上）
    realname = Column(String(100))  # 用户名
    phone_num = Column(String(50), default="")  # 手机号
    note = Column(Text, default="暂无")  # 备注信息
    state = Column(Integer, default=1)  # 账户状态（0：封禁，1：正常）
    profile_photo = Column(LONGBLOB)  # 头像（存储为二进制数据）
    score = Column(Integer, default=0)  # 用户积分
    created_at = Column(String(50))  # 创建时间
    updated_at = Column(String(50))  # 更新时间

Base.metadata.create_all(bind=engine)

#用户信息表的CRUD部分
def create_user(
    db: Session, 
    userid: str, 
    password: str, 
    level: int, 
    realname: str, 
    phone_num: str, 
    note: str, 
    state: int, 
    profile_photo: bytes, 
    score: int, 
    created_at: str, 
    updated_at: str
) -> User:
    """
    创建新用户
    """
    db_user = User(
        userid=userid,
        password=password,
        level=level,
        realname=realname,
        phone_num=phone_num,
        note=note,
        state=state,
        profile_photo=profile_photo,
        score=score,
        created_at=created_at,
        updated_at=updated_at
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
def get_users(
    db: Session, 
    skip: int = 0, 
    limit: int = 10
) -> List[User]:
    """
    获取用户列表，支持分页
    """
    return db.query(User).offset(skip).limit(limit).all()
def get_users(
    db: Session, 
    skip: int = 0, 
    limit: int = 10
) -> List[User]:
    """
    获取用户列表，支持分页
    """
    return db.query(User).offset(skip).limit(limit).all()
def get_user_by_email(
    db: Session, 
    email: str
) -> Optional[User]:
    """
    根据用户邮箱获取用户
    """
    return db.query(User).filter(User.userid == email).first()
def update_user(
    db: Session, 
    user_id: int, 
    update_data: Dict[str, Optional[str | int | bytes]]
) -> Optional[User]:
    """
    更新用户信息
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    
    # 更新字段
    for key, value in update_data.items():
        if hasattr(db_user, key) and value is not None:
            setattr(db_user, key, value)
    
    # 提交事务
    db.commit()
    db.refresh(db_user)
    return db_user
def delete_user(
    db: Session, 
    user_id: int
) -> bool:
    """
    删除用户
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return False
    
    # 删除记录
    db.delete(db_user)
    db.commit()
    return True


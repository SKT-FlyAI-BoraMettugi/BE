from sqlalchemy import Column, String, Integer, DateTime, Enum
from database.nolly import Base

class Theme(Base):
    __tablename__ = 'theme'

    theme_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False) # 테마 번호
    theme_name = Column(String(20), nullable=False) # 테마 이름
    theme_ex = Column(String(100), nullable=True) # 테마 설명
    profile_img = Column(String(100), nullable=False) # 프로필 이미지
    background_img = Column(String(100), nullable=False) # 배경 이미지
    high_succ_color = Column(String(10), nullable=False) # 상 난이도 성공 색상
    high_fail_color = Column(String(10), nullable=False) # 상 난이도 미성공 색상
    mid_succ_color = Column(String(10), nullable=False) # 중 난이도 성공 색상
    mid_fail_color = Column(String(10), nullable=False) # 중 난이도 미성공 색상
    low_succ_color = Column(String(10), nullable=False) # 하 난이도 성공 색상
    low_fail_color = Column(String(10), nullable=False) # 하 난이도 미성공 색상
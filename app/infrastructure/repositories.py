from sqlalchemy.orm import Session
from typing import List, Optional
from app.infrastructure.models import LinkDB, UserDB
from sqlalchemy.sql import func

class LinkRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, user_id: int) -> List[LinkDB]:
        return self.db.query(LinkDB).filter(LinkDB.owner_id == user_id).all()
    
    def get_by_id(self, link_id: int, user_id: int) -> Optional[LinkDB]:
        return self.db.query(LinkDB).filter(
            LinkDB.id == link_id, 
            LinkDB.owner_id == user_id
        ).first()
    
    def create(self, link_data: dict, owner_id: int) -> LinkDB:
        try:
            link = LinkDB(**link_data, owner_id=owner_id)
            self.db.add(link)
            self.db.commit()
            self.db.refresh(link)
            return link
        except Exception:
            self.db.rollback()
            raise
    
    def update(self, link_id: int, user_id: int, update_data: dict) -> Optional[LinkDB]:
        link = self.get_by_id(link_id, user_id)
        if not link:
            return None
        
        try:
            for key, value in update_data.items():
                if value is not None:
                    setattr(link, key, value)
            link.updated_at = func.now()
            self.db.commit()
            self.db.refresh(link)
            return link
        except Exception:
            self.db.rollback()
            raise
    
    def delete(self, link_id: int, user_id: int) -> bool:
        link = self.get_by_id(link_id, user_id)
        if not link:
            return False
        
        try:
            self.db.delete(link)
            self.db.commit()
            return True
        except Exception:
            self.db.rollback()
            raise
    
    def count(self, user_id: int) -> int:
        return self.db.query(LinkDB).filter(LinkDB.owner_id == user_id).count()

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_username(self, username: str) -> Optional[UserDB]:
        return self.db.query(UserDB).filter(UserDB.username == username).first()
    
    def get_by_email(self, email: str) -> Optional[UserDB]:
        return self.db.query(UserDB).filter(UserDB.email == email).first()
    
    def get_by_id(self, user_id: int) -> Optional[UserDB]:
        return self.db.query(UserDB).filter(UserDB.id == user_id).first()
    
    def create(self, user_data: dict) -> UserDB:
        try:
            user = UserDB(**user_data)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception:
            self.db.rollback()
            raise
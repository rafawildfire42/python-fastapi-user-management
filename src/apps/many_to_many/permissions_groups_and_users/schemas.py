from pydantic import BaseModel


class UserAndGroupRelation(BaseModel):
    user_id: int = 0
    permission_group_id: int = 0

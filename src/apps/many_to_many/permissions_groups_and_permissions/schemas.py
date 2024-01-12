from pydantic import BaseModel


class PermissionAndGroupRelation(BaseModel):
    permission_id: int = 0
    permission_group_id: int = 0

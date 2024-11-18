from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from typing import List
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_user
from app.services import material_service
from app.schemas import material as material_schemas
from app.schemas.user import User

router = APIRouter(
    prefix="/materials",
    tags=["materials"]
)

@router.get("/list", response_model=List[material_schemas.Material])
async def list_materials(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    教材一覧を取得するエンドポイント
    - ページネーション対応
    - 認証済みユーザーのみアクセス可能
    """
    try:
        materials = material_service.get_materials(
            db=db,
            user_id=current_user.id,
            skip=skip,
            limit=limit
        )
        return materials
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"教材一覧の取得に失敗しました: {str(e)}"
        )

@router.get("/download/{material_id}")
async def download_material(
    material_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    指定された教材をダウンロードするエンドポイント
    - 認証済みユーザーのみアクセス可能
    - アクセス権限の確認を実施
    """
    try:
        material_file = material_service.download_material(
            db=db,
            material_id=material_id,
            user_id=current_user.id
        )
        return material_file
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"教材のダウンロードに失敗しました: {str(e)}"
        )

@router.post("/upload", response_model=material_schemas.Material)
async def upload_material(
    title: str,
    description: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    新しい教材をアップロードするエンドポイント
    - 管理者権限を持つユーザーのみアクセス可能
    - ファイルサイズと形式の検証を実施
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="この操作を実行する権限がありません"
        )

    try:
        # ファイルサイズの検証（例: 最大100MB）
        file_size = await file.read()
        if len(file_size) > 100 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="ファイルサイズが大きすぎます（最大100MB）"
            )
        
        # ファイルポインタを先頭に戻す
        await file.seek(0)
        
        new_material = material_service.create_material(
            db=db,
            title=title,
            description=description,
            file=file,
            uploaded_by=current_user.id
        )
        return new_material
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"教材のアップロードに失敗しました: {str(e)}"
        )

@router.delete("/{material_id}")
async def delete_material(
    material_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    指定された教材を削除するエンドポイント
    - 管理者権限を持つユーザーのみアクセス可能
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="この操作を実行する権限がありません"
        )

    try:
        material_service.delete_material(
            db=db,
            material_id=material_id
        )
        return {"message": "教材が正常に削除されました"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"教材の削除に失敗しました: {str(e)}"
        )
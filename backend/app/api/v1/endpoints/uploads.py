from fastapi import APIRouter, Depends, File, UploadFile

from app.dependencies.auth import CurrentUser, get_current_user

router = APIRouter()


@router.post("/images")
async def upload_image(file: UploadFile = File(...), _: CurrentUser = Depends(get_current_user)):
    return {
        "success": True,
        "data": {
            "filename": file.filename,
            "content_type": file.content_type,
            "status": "upload-provider-not-configured",
        },
    }


@router.delete("/{media_id}")
async def delete_upload(media_id: str, _: CurrentUser = Depends(get_current_user)):
    return {"success": True, "data": {"media_id": media_id, "deleted": True}}

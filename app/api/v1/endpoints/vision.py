from fastapi import APIRouter, UploadFile, File, Form, HTTPException, status
from app.services.gemini import gemini_service
from app.core.config import settings

router = APIRouter()
ALLOWED_MIME_TYPES = ["image/jpeg", "image/png", "image/webp", "image/gif"]

@router.post(
        "/vision",
        summary="Analyze an uploaded image with Gemini",
        status_code=status.HTTP_200_OK
    )
async def upload_and_analyze_image(
        file: UploadFile = File(..., description="The image file to analyze (JPEG, PNG, WEBP)"),
        prompt: str = Form("Describe what you see in this image in detail.", description="Question or prompt about the image")
    ):
        """
        Multimodal Vision Endpoint:
        - Accepts an image file + custom prompt
        - Validates MIME type
        - Passes raw bytes to GeminiService
        - Returns AI analysis in JSON
        """
        # 1. Validate File Type
        if file.content_type not in ALLOWED_MIME_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file type '{file.content_type}'. Allowed types: {', '.join(ALLOWED_MIME_TYPES)}"
            )
    
        try:
            # 2. Read file bytes asynchronously
            image_bytes = await file.read()
    
            # 3. Call Gemini Service
            analysis = gemini_service.analyze_image(
                image_bytes=image_bytes,
                mime_type=file.content_type,
                prompt=prompt
            )

            return {
                "status": "success",
                "filename": file.filename,
                "content_type": file.content_type,
                "prompt": prompt,
                "analysis": analysis,
                "model_used": settings.DEFAULT_MODEL
            }

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Vision processing failed: {str(e)}"
            )
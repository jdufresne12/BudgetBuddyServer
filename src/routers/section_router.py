from typing import List
from fastapi import APIRouter, HTTPException, Depends # type: ignore
from ..services.section.section_service import SectionService
from ..schemas.section import CreateSectionData, CreateSectionResponse, GetMonthsSectionsData, DeleteSectionData
from ..utils.auth_token import verify_token

router = APIRouter(prefix='/section', tags=['section'])
section_service = SectionService()

# NOT USED ANYMORE - Now use static sections
@router.post('/create_section', response_model=CreateSectionResponse)
async def create_section(data: CreateSectionData, token: dict = Depends(verify_token)):
    try:
        section = await section_service.create_section(data)
        if section:
            return CreateSectionResponse(
                section_id = section.section_id,
                name = section.name,
                start_date = section.start_date,
                end_date = section.end_date
            )
        raise HTTPException(status_code=400, detail="Failed to create section")
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})
    
# NOT USED ANYMORE - Now use static sections
@router.delete('/delete_section', response_model=bool)
async def delete_section(data: DeleteSectionData, token: dict = Depends(verify_token)):
    try:
        response = await section_service.delete_section(data)
        if response:
            return True
        raise HTTPException(status_code=400, detail="Section not found or doesn't belong to user")
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})
    
@router.post('/get_months_sections', response_model=List[CreateSectionResponse])
async def get_months_sections(data: GetMonthsSectionsData, token: dict = Depends(verify_token)):
    try:
        sections = await section_service.get_months_sections(data)
        if sections:
            return sections
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=500, detail={str(e)})
    

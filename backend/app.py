from io import BytesIO
from fastapi import FastAPI, File, UploadFile, Form
from face_shape import classify_face_shape, recommend_styles
from hair_segmentation import apply_hair_color, segment_hair


app = FastAPI()

@app.post("/analyze-face-shape/")
async def analyze_face_shape(file: UploadFile = File(...)):
    image_bytes = await file.read()
    face_shape = classify_face_shape(image_bytes)
    styles = recommend_styles(face_shape)
    return {"face_shape": face_shape, "recommended_styles": styles}


from fastapi.responses import StreamingResponse
from hair_segmentation import segment_hair

@app.post("/segment-hair/")
async def segment(file: UploadFile = File(...)):
    image_bytes = await file.read()
    processed_image_bytes = segment_hair(image_bytes)
    return StreamingResponse(BytesIO(processed_image_bytes), media_type="image/jpeg")

@app.post("/virtual-try-on/")
async def virtual_try_on(file: UploadFile = File(...), color: str = Form("red")):
    # Map color names to BGR values
    color_map = {
        "red": (0, 0, 255),
        "blue": (255, 0, 0),
        "green": (0, 255, 0),
        "blonde": (194, 178, 128),
        "black": (0, 0, 0)
    }
    bgr_color = color_map.get(color.lower(), (0, 0, 255))  # Default to red

    image_bytes = await file.read()
    processed_image_bytes = apply_hair_color(image_bytes, color=bgr_color)
    return StreamingResponse(BytesIO(processed_image_bytes), media_type="image/jpeg")
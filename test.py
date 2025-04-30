from storage import storage_service
import os

# with open("video1.mp4", "rb") as file:
#     file_content = file.read()

# secure_url, public_id = storage_service.uploadVideo(file_content)
# print(f"Secure URL: {secure_url}")
# print(f"Public ID: {public_id}")


delete_result =  storage_service.delete("jez8ctrwrskhcowqzhse", isVideo=True)
print(delete_result)
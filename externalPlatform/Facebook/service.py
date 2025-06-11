from config import get_env_variable
from video.service import video_service
import requests
import tempfile
import os
import mimetypes
class FacebookService():
    def __init__(self):
        self.appId = get_env_variable("FACEBOOK_APP_ID")
        self.app_secret = get_env_variable("FACEBOOK_APP_SECRET")
        self.graph_api_version = "v21.0"
     
    # Đăng nhập người dùng để lấy access token, sau đó dùng api để đăng video
    # Khi người dùng click vào ô share on facebook
    # trả ra url đăng nhập của facebook
    # frontend gọi và chỉ định sau khi đăng nhập xong sẽ redirect về trang nào
    # Frontend nhận dược url và hiển thị giao diện đăng nhập -> đăng nhập xong, nhận code
    # Gửi code về backend để lấy access_token -> lưu access_token vào local_storage 
    # để sử dụng trong phiên đăng nhập đó 
    # Hiển thị dialog đang tải video lên và tải video thành công
    # có thể fail => FB chỉ hỗ trợ đăng video cho page từ 2018 => test fail thì cấu hình lại
    def get_login_url(self, redirect_uri: str) -> str:
        """Generate Facebook OAuth login URL"""
        return (
            f"https://www.facebook.com/{self.graph_api_version}/dialog/oauth?"
            f"client_id={self.appId}&redirect_uri={redirect_uri}"
            "&scope=public_profile,email,user_videos,publish_video"
            "&response_type=code"
        )
    
    def exchangeCodeForAccessToken(self, code: str, redirect_uri: str):
        getToken_url=f"https://graph.facebook.com/{self.graph_api_version}/oauth/access_token"
        response = requests.get(
            getToken_url,
            params={
                "client_id": self.appId,
                "client_secret": self.app_secret,
                "code": code,
                "redirect_uri": redirect_uri, 
            }
        )
        response.raise_for_status()
        return response.json().get("access_token")

    def uploadVideo(self, videoId: str, access_token: str):
        # Gọi db để lấy URL của videoId
        video = video_service.get_video_by_id(videoId)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        temp_file_path = temp_file.name
        temp_file.close()  # Đóng file để các hàm khác có thể sử dụng

        # Tải nội dung từ URL và ghi vào file
        response = requests.get(video.url, stream=True)
        with open(temp_file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        file_length = os.path.getsize(temp_file_path)
        file_type, _ = mimetypes.guess_type(temp_file_path)

        # Gửi yêu cầu khởi tạo upload session đến Facebook
        init_url = (
            f"https://graph.facebook.com/{self.graph_api_version}/{self.appId}/uploads"
        )
        init_params = {
            "file_name": os.path.basename(temp_file_path),
            "file_length": file_length,
            "file_type": file_type,
            "access_token": access_token
        }
        
        init_resp = requests.post(init_url, params=init_params)
        init_data = init_resp.json()
        print("Init upload:", init_data)

        if 'id' not in init_data or 'upload_url' not in init_data:
            raise Exception(f"Upload init failed: {init_data}")

        upload_id = init_data["id"]
        upload_url = init_data["upload_url"]

        # Upload video file lên upload_url mà Facebook cung cấp
        with open(temp_file_path, 'rb') as f:
            file_upload_resp = requests.put(upload_url, data=f)
            print("Upload file result:", file_upload_resp.status_code)

            if not file_upload_resp.ok:
                raise Exception("File upload failed")

        # Đăng bài viết dùng video đã upload
        create_video_post_url = f"https://graph.facebook.com/{self.graph_api_version}/me/videos"
        post_params = {
            "upload_phase": "finish",
            "video_id": upload_id,
            "access_token": access_token
        }

        finish_resp = requests.post(create_video_post_url, data=post_params)
        print("Finish upload result:", finish_resp.json())

        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            
        return finish_resp.json()

    
        
        
       

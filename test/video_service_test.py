from video.service import video_service
from video.dto.requests import CreateVideoRequest
import asyncio
from db import init_db

request = CreateVideoRequest(
    script=(
        "Bạn có bao giờ tự hỏi, liệu con đường học vấn ở Việt Nam có thực sự trải đầy hoa hồng? " + 
        "Chúng ta luôn nghe về những tấm gương học sinh nghèo vượt khó, những thủ khoa điểm cao ngất ngưởng. " + 
        "Nhưng phía sau ánh hào quang đó là gì?\n" + 
        "Áp lực thi cử đè nặng lên vai những cô cậu học trò mới lớn. " +
        "Học thêm trở thành \"cơm bữa\" không thể thiếu, bào mòn thời gian và sức lực của cả học sinh lẫn phụ huynh. " + 
        "Chương trình học nặng tính lý thuyết, thiếu thực tế, khiến học sinh khó áp dụng kiến thức vào cuộc sống.\n" + 
        "Chúng ta vẫn loay hoay với việc nhồi nhét kiến thức, thay vì khuyến khích tư duy sáng tạo và khả năng tự học. " +
        "Giáo viên chịu áp lực thành tích, đôi khi quên đi việc quan tâm đến từng cá nhân học sinh.\n" + 
        "Nhưng không phải là không có tia hy vọng. " +
        "Nhiều thầy cô tâm huyết đang nỗ lực đổi mới phương pháp giảng dạy, tạo ra những lớp học thú vị và kích thích tư duy. " +
        "Các bạn trẻ năng động tham gia các hoạt động ngoại khóa, trau dồi kỹ năng mềm và khám phá bản thân.\n" +
        "Giáo dục Việt Nam đang đứng trước ngã ba đường. " +
        "Chúng ta có thể tiếp tục con đường cũ, hoặc mạnh dạn thay đổi để tạo ra một môi trường học tập thực sự khai phóng, " +
        "nơi mỗi học sinh đều có cơ hội phát triển toàn diện.\n" +
        "Liệu chúng ta có đủ dũng cảm để lựa chọn con đường thứ hai?\n"
    ),
    title="Giáo dục Việt Nam: Áp lực hay cơ hội?",
    userId="pqkiet854"
)

async def main():
    await init_db()
    await test_create_video()

async def test_create_video():
    secure_url, public_id = await video_service.create_video(request)
    print("Video created successfully")
    print(f"Video path: {secure_url}")
    print(f"Video ID: {public_id}")

if __name__ == "__main__":
    asyncio.run(main())
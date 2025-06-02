from video.service import video_service
from video.dto.requests import CreateVideoRequest
import asyncio
from db import init_db

request = CreateVideoRequest(
    script="""
        (MỞ ĐẦU - 0-10 giây)

    HÌNH ẢNH: Một dòng thời gian đồ họa ngắn gọn, bắt đầu từ hình ảnh máy tính cổ điển, chuyển dần sang các biểu tượng sơ khai của AI (ví dụ: máy tính chơi cờ). Nền nhạc nhẹ nhàng, đầy suy tư.
    GIỌNG NÓI (VO): "Từ những ước mơ khoa học viễn tưởng xa xôi, Trí tuệ nhân tạo, hay AI, đã và đang có một hành trình phát triển đầy ngoạn mục. Từng bước một, chúng ta đã chứng kiến những khái niệm trừu tượng dần trở thành hiện thực."
    (GIAI ĐOẠN ĐẦU & NHỮNG BƯỚC ĐỘT PHÁ - 10-30 giây)

    HÌNH ẢNH: Chuyển cảnh nhanh sang các đoạn phim hoặc đồ họa minh họa các cột mốc quan trọng:
    Mạng nơ-ron nhân tạo sơ khai.
    Hệ thống chuyên gia.
    Máy tính Deep Blue đánh bại kiện tướng cờ vua Garry Kasparov (năm 1997).
    Sự trỗi dậy của Machine Learning với các thuật toán học hỏi từ dữ liệu.
    GIỌNG NÓI (VO): "Ban đầu, AI tập trung vào việc mô phỏng tư duy logic và giải quyết các bài toán cụ thể. Rồi đến những năm 2000, sự bùng nổ của dữ liệu lớn và sức mạnh tính toán đã mở ra một kỷ nguyên mới: kỷ nguyên của Học máy (Machine Learning). AI bắt đầu học hỏi từ hàng núi dữ liệu, nhận diện mẫu và đưa ra dự đoán với độ chính xác đáng kinh ngạc."
    (KỶ NGUYÊN HIỆN ĐẠI & TƯƠNG LAI - 30-55 giây)

    HÌNH ẢNH: Hình ảnh minh họa AI trong cuộc sống hiện đại:
    Xe tự lái trên đường.
    Trợ lý ảo trên điện thoại.
    Hệ thống nhận diện khuôn mặt, dịch thuật thời gian thực.
    AI sáng tạo nghệ thuật, âm nhạc.
    Cuối cùng là hình ảnh AI giúp đỡ con người trong y tế, khoa học. Nền nhạc trở nên lạc quan, truyền cảm hứng.
    GIỌNG NÓI (VO): "Ngày nay, chúng ta đang sống trong kỷ nguyên của Học sâu (Deep Learning). AI không chỉ phân tích mà còn hiểu và tạo ra nội dung như ngôn ngữ, hình ảnh. Từ những chiếc xe tự lái, trợ lý ảo thông minh cho đến các công cụ chẩn đoán y tế, AI đang thay đổi cách chúng ta làm việc, học tập và tương tác với thế giới. Nó không còn là công cụ hỗ trợ, mà là một đối tác thông minh."
    (KẾT THÚC - 55-60 giây)

    HÌNH ẢNH: Logo hoặc biểu tượng AI hiện đại, kết hợp với hình ảnh con người và công nghệ hòa hợp.
    GIỌNG NÓI (VO): "Tương lai của AI hứa hẹn những đột phá chưa từng có, mở ra những chân trời mới cho sự phát triển của nhân loại. AI không chỉ là công nghệ, đó là tương lai của chúng ta."
    """,
    title="Hành Trình Phát Triển Của Trí Tuệ Nhân Tạo",
    userId="pqkiet854"
)

async def main():
    await test_get_video_metadata()

async def test_create_video():
    secure_url, public_id = await video_service.create_video(request)
    print("Video created successfully")
    print(f"Video path: {secure_url}")
    print(f"Video ID: {public_id}")
async def test_get_video_metadata():
    video_metadata = await video_service.get_video_metadata(request)
    print("Video metadata retrieved successfully")
    print(f"Video metadata: {video_metadata}")
if __name__ == "__main__":
    asyncio.run(main())
from ai import ai_service
import asyncio

def test_generate_image():
    prompt = "A beautiful sunset over the mountains"
    ai_service.generate_image(prompt=prompt)
def test_get_response():
    # prompt = f"""
    # Hãy viết một kịch bản video ngắn (dưới 1 phút) về chủ đề tiết kiệm tiền.
    # Kịch bản bao gồm:
    # - Phần mở đầu để thu hút người xem
    # - Nội dung chính: 2-3 mẹo tiết kiệm tiền đơn giản
    # - Phần kết thúc ấn tượng và lời kêu gọi hành động
    # """
    prompt = """
    generate a short video script: 
    Write a short video script (under 1 minute) on the topic of saving money.
    The script should include:
    - An engaging introduction to capture viewers' attention
    - Main content: 2-3 simple money-saving tips
    - A memorable conclusion and a call to action
    """
    
    responses = ai_service.get_response(prompt=prompt)
    print(responses)
if __name__ == "__main__":
    test_get_response()
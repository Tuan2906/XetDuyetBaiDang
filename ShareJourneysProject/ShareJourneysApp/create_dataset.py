import pandas as pd

# Dữ liệu mẫu với văn bản tiếng Anh và tiếng Việt và nhãn
data = {
    'text': [
        "This is a normal content.",
        "This content contains sensitive information.",
        "Here is some regular text.",
        "Sensitive data detected in this text.",
        "Just another normal content.",
        "This article includes some sensitive details.",
        "F**k this! This is sh*t!",
        "Đ*o tin được, thật là v*cl!",
        "Call me at 123-456-7890!",
        "Liên hệ với tôi qua số 098-765-4321!",
        "<p>This is a paragraph.</p>",
        "<script>alert('This is a test');</script>",
        "Content without meaning $$$ %%% @@@",
        "Nội dung không rõ nghĩa ### $$$",
        "The password is '12345'.",
        "Mật khẩu là 'abcdef'.",
        "Do not share your social security number.",
        "Không chia sẻ số chứng minh nhân dân của bạn.",
        "Buy now for $9.99 only!",
        "Mua ngay với giá chỉ 199.000đ!",
        "Vũng Tàu có bãi biển đẹp",
        "Hà Nội đẹp",
        "Đà Lạt mộng mơ",
        "Đà Lạt là thành phố du lịch nổi tiếng của Việt Nam",
        "Đà Lạt mùa này rất đẹp",
        "Đà Lạt có rất nhiều hoa",
        "Hà Nội",
        "sex",
        "mua bán trinh",
        "đẹp lắm nha",
        "Chợ",
        "Đà Lạt",
        "TP.HCM",
    ],
    'label': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,0,0,0,0,0,0,0,1,1,0,0,0,0]  # 0: Không nhạy cảm, 1: Nhạy cảm
}

# Tạo DataFrame
df = pd.DataFrame(data)

# Lưu DataFrame vào tệp CSV
df.to_csv('duLieuNhayCam.csv', index=False)

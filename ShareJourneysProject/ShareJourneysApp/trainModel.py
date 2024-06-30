import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import make_pipeline

# Đọc dữ liệu từ tệp CSV
df = pd.read_csv('duLieuNhayCam.csv')

# Chia dữ liệu thành văn bản và nhãn
texts = df['text'].tolist()
labels = df['label'].tolist()

# Tách dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(texts, labels, test_size=0.1, random_state=42)

# Tạo pipeline với TfidfVectorizer và LogisticRegression
# TfidfVectorizer: Chuyển đổi các văn bản thành ma trận TF-IDF.
# LogisticRegression: Mô hình hồi quy logistic để phân loại văn bản.
pipeline = make_pipeline(TfidfVectorizer(), LogisticRegression())

# Định nghĩa các siêu tham số cần tìm kiếm
param_grid = {
    'tfidfvectorizer__max_df': [0.7, 0.8, 0.9, 1.0], #Loại bỏ các từ xuất hiện trong văn bản hơn (70% hoặc 80%,90%,) 1,0 không loai6 bỏ tử nào
        'tfidfvectorizer__min_df': [1, 2, 5], # 1: Bao gồm tất cả các từ xuất hiện ít nhất một lần. 2 Loại bỏ các từ xuất
        # hiện ít hơn 2 lần. 5Loại bỏ các từ xuất hiện ít hơn 5 lần.
    'tfidfvectorizer__ngram_range': [(1, 1), (1, 2), (1, 3)], # các (1, 1): Chỉ sử dụng unigram (từ đơn lẻ).(1,
    # 2): Sử dụng cả unigram và bigram (cặp từ liên tiếp).(1, 3): Sử dụng unigram, bigram và trigram (ba từ liên tiếp).
    'logisticregression__C': [0.1, 1, 10, 100]
}

# Sử dụng GridSearchCV để tìm siêu tham số tốt nhất
grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy')
grid_search.fit(X_train, y_train)

# In ra các siêu tham số tốt nhất
print("Best parameters found: ", grid_search.best_params_)

# Huấn luyện lại mô hình với siêu tham số tốt nhất
best_model = grid_search.best_estimator_
best_model.fit(X_train, y_train)

# Đánh giá mô hình trên tập kiểm tra
accuracy = best_model.score(X_test, y_test)
print(f"Test accuracy: {accuracy:.2f}")

# Lưu mô hình
joblib.dump(best_model, 'content_model.pkl')

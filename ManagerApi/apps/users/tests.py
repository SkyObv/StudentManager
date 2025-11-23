from django.test import TestCase

# Create your tests here.
# 测试sql语句
"""
-- 插入40条学生数据 (已包含所有 AbstractUser 必填字段)
INSERT INTO students (password, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, name, gender) VALUES
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202301', '张伟', '', '', false, true, '2025-01-01 00:00:00', '张伟', 'male'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202302', '王芳', '', '', false, true, '2025-01-01 00:00:00', '王芳', 'female'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202303', '李娜', '', '', false, true, '2025-01-01 00:00:00', '李娜', 'female'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202304', '刘敏', '', '', false, true, '2025-01-01 00:00:00', '刘敏', 'female'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202305', '陈静', '', '', false, true, '2025-01-01 00:00:00', '陈静', 'female'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202306', '赵强', '', '', false, true, '2025-01-01 00:00:00', '赵强', 'male'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202307', '周磊', '', '', false, true, '2025-01-01 00:00:00', '周磊', 'male'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202308', '孙洋', '', '', false, true, '2025-01-01 00:00:00', '孙洋', 'male'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202309', '钱勇', '', '', false, true, '2025-01-01 00:00:00', '钱勇', 'male'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202310', '吴艳', '', '', false, true, '2025-01-01 00:00:00', '吴艳', 'female'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202311', '郑杰', '', '', false, true, '2025-01-01 00:00:00', '郑杰', 'male'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202312', '冯涛', '', '', false, true, '2025-01-01 00:00:00', '冯涛', 'male'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202313', '蒋秀英', '', '', false, true, '2025-01-01 00:00:00', '蒋秀英', 'female'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202314', '沈明', '', '', false, true, '2025-01-01 00:00:00', '沈明', 'male'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202315', '韩丽', '', '', false, true, '2025-01-01 00:00:00', '韩丽', 'female'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202316', '杨华', '', '', false, true, '2025-01-01 00:00:00', '杨华', 'male'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202317', '朱平', '', '', false, true, '2025-01-01 00:00:00', '朱平', 'male'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202318', '秦霞', '', '', false, true, '2025-01-01 00:00:00', '秦霞', 'female'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202319', '尤军', '', '', false, true, '2025-01-01 00:00:00', '尤军', 'male'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202320', '许琳', '', '', false, true, '2025-01-01 00:00:00', '许琳', 'female'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202321', '何斌', '', '', false, true, '2025-01-01 00:00:00', '何斌', 'male'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202322', '吕雪', '', '', false, true, '2025-01-01 00:00:00', '吕雪', 'female'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202323', '施辉', '', '', false, true, '2025-01-01 00:00:00', '施辉', 'male'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202324', '张伟', '', '', false, true, '2025-01-01 00:00:00', '张伟', 'male'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202325', '孔芳', '', '', false, true, '2025-01-01 00:00:00', '孔芳', 'female'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202326', '曹娜', '', '', false, true, '2025-01-01 00:00:00', '曹娜', 'female'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202327', '严敏', '', '', false, true, '2025-01-01 00:00:00', '严敏', 'female'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202328', '华强', '', '', false, true, '2025-01-01 00:00:00', '华强', 'male'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202329', '金磊', '', '', false, true, '2025-01-01 00:00:00', '金磊', 'male'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202330', '魏洋', '', '', false, true, '2025-01-01 00:00:00', '魏洋', 'male'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202331', '陶勇', '', '', false, true, '2025-01-01 00:00:00', '陶勇', 'male'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202332', '姜艳', '', '', false, true, '2025-01-01 00:00:00', '姜艳', 'female'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202333', '戚杰', '', '', false, true, '2025-01-01 00:00:00', '戚杰', 'male'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202334', '谢涛', '', '', false, true, '2025-01-01 00:00:00', '谢涛', 'male'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202335', '邹秀英', '', '', false, true, '2025-01-01 00:00:00', '邹秀英', 'female'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202336', '喻明', '', '', false, true, '2025-01-01 00:00:00', '喻明', 'male'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202337', '柏丽', '', '', false, true, '2025-01-01 00:00:00', '柏丽', 'female'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202338', '水华', '', '', false, true, '2025-01-01 00:00:00', '水华', 'male'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202339', '窦平', '', '', false, true, '2025-01-01 00:00:00', '窦平', 'male'),
('pbkdf2_sha256$600000$vN8M5bL9kL7oJhG5sP2wFz$Kp8XeN1tYjL7sP9wQ3rF6vZ9nH2kL5mO8pQ1rT4uY7iA0cV3bN6eW9zX2fS5g', false, '202340', '章霞', '', '', false, true, '2025-01-01 00:00:00', '章霞', 'female');

"""
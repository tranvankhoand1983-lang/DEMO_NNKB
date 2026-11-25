const rateLimit = require('express-rate-limit');
const crypto = require('crypto');

// 1. Chống NoSQL Injection chuyên sâu
// Hàm đệ quy kiểm tra các toán tử nguy hiểm như $gt, $ne, $where, $regex, $or...
const hasPoisonKey = (obj) => {
  if (!obj || typeof obj !== 'object') return false;
  for (const key of Object.keys(obj)) {
    if (key.startsWith('$') || key.includes('.')) {
      return true;
    }
    if (typeof obj[key] === 'object' && hasPoisonKey(obj[key])) {
      return true;
    }
  }
  return false;
};

const preventNoSqlInjection = (req, res, next) => {
  if (hasPoisonKey(req.body) || hasPoisonKey(req.query) || hasPoisonKey(req.params)) {
    console.warn(`[SECURITY ALERT] Phát hiện hành vi NoSQL Injection từ IP: ${req.ip}`);
    return res.status(400).json({
      status: 'error',
      message: 'Cảnh báo an toàn: Phát hiện cấu trúc truy vấn hoặc toán tử NoSQL độc hại!'
    });
  }
  next();
};

// 2. Chống Brute-force dò mật khẩu vào API đăng nhập / đăng ký
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 phút
  max: 10, // Tối đa 10 lần thử từ 1 IP
  standardHeaders: true,
  legacyHeaders: false,
  message: {
    status: 'error',
    message: 'Quá nhiều lần thử xác thực không thành công từ IP này. Vui lòng thử lại sau 15 phút!'
  }
});

// Giới hạn tần suất chung cho toàn bộ API (chống spam/DDoS)
const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 500, // Tối đa 500 request trong 15 phút
  standardHeaders: true,
  legacyHeaders: false,
  message: {
    status: 'error',
    message: 'Hệ thống đang quá tải yêu cầu từ địa chỉ mạng của bạn. Vui lòng thử lại sau ít phút!'
  }
});

// 3. Bộ lọc chống XSS cơ bản (loại bỏ các thẻ script độc hại)
const sanitizeXSS = (req, res, next) => {
  const sanitizeString = (str) => {
    if (typeof str !== 'string') return str;
    return str.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');
  };

  if (req.body && typeof req.body === 'object') {
    for (const key of Object.keys(req.body)) {
      if (typeof req.body[key] === 'string') {
        req.body[key] = sanitizeString(req.body[key]);
      }
    }
  }
  next();
};

// 4. Xác thực chữ ký số HMAC-SHA256 cho thanh toán PayOS VietQR
const verifyPayOSSignature = (data, checksumKey, signature) => {
  try {
    // Sắp xếp các khoá theo thứ tự bảng chữ cái để tạo chuỗi dữ liệu ký
    const sortedKeys = Object.keys(data).sort();
    const signData = sortedKeys.map(k => `${k}=${data[k]}`).join('&');
    const computedSignature = crypto.createHmac('sha256', checksumKey).update(signData).digest('hex');
    return computedSignature === signature;
  } catch (err) {
    return false;
  }
};

module.exports = {
  preventNoSqlInjection,
  authLimiter,
  apiLimiter,
  sanitizeXSS,
  verifyPayOSSignature
};

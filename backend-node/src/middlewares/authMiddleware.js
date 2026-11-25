const jwt = require('jsonwebtoken');
const User = require('../models/User');

const protect = async (req, res, next) => {
  let token;
  if (req.headers.authorization && req.headers.authorization.startsWith('Bearer')) {
    token = req.headers.authorization.split(' ')[1];
  } else if (req.cookies && req.cookies.token) {
    token = req.cookies.token;
  }

  if (!token) {
    return res.status(401).json({ message: 'Chưa đăng nhập, vui lòng đăng nhập để tiếp tục' });
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET || 'velmora_super_secure_jwt_secret_key_2026_epu');
    const user = await User.findOne({ id: decoded.id }).select('-password');
    if (!user) {
      return res.status(401).json({ message: 'Tài khoản không tồn tại trên hệ thống' });
    }
    req.user = user;
    next();
  } catch (err) {
    return res.status(401).json({ message: 'Token không hợp lệ hoặc đã hết hạn' });
  }
};

const authorize = (...roles) => {
  return (req, res, next) => {
    if (!req.user || !roles.includes(req.user.role)) {
      return res.status(403).json({ message: 'Bạn không có quyền truy cập chức năng này' });
    }
    next();
  };
};

module.exports = { protect, authorize };

const mongoose = require('mongoose');

const userVoucherSchema = new mongoose.Schema({
  id: { type: Number, required: true, unique: true },
  userId: { type: String, required: true },
  promotionId: { type: Number, required: true },
  savedAt: { type: Date, default: Date.now },
  isUsed: { type: Boolean, default: false },
  usedAt: { type: Date, default: null }
});

module.exports = mongoose.model('UserVoucher', userVoucherSchema, 'user_vouchers');

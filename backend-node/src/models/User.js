const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  id: { type: String, required: true, unique: true },
  fullName: { type: String, required: true },
  name: { type: String },
  email: { type: String, required: true, unique: true },
  password: { type: String, default: null },
  avatar: { type: String, default: null },
  role: { type: String, enum: ['admin', 'staff', 'customer'], default: 'customer' },
  provider: { type: String, default: 'email' },
  phone: { type: String, default: null },
  defaultAddress: { type: String, default: null },
  address: { type: String, default: null },
  newsletterOptin: { type: Boolean, default: false },
  isActive: { type: Boolean, default: true },
  createdAt: { type: Date, default: Date.now }
}, { timestamps: true });

module.exports = mongoose.model('User', userSchema, 'users');

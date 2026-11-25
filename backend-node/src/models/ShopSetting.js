const mongoose = require('mongoose');

const shopSettingSchema = new mongoose.Schema({
  id: { type: Number, required: true, unique: true },
  phone: { type: String },
  email: { type: String },
  workingHours: { type: String },
  address: { type: String },
  facebookUrl: { type: String },
  instagramUrl: { type: String },
  updatedAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('ShopSetting', shopSettingSchema, 'shop_settings');

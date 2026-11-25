const mongoose = require('mongoose');

const bannerSchema = new mongoose.Schema({
  id: { type: Number, required: true, unique: true },
  imageUrl: { type: String, required: true },
  subtitle: { type: String },
  title: { type: String, required: true },
  description: { type: String },
  isActive: { type: Boolean, default: true }
});

module.exports = mongoose.model('Banner', bannerSchema, 'banners');

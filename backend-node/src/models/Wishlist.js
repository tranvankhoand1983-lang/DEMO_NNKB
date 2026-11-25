const mongoose = require('mongoose');

const wishlistSchema = new mongoose.Schema({
  userId: { type: String, required: true },
  productId: { type: Number, required: true },
  createdAt: { type: Date, default: Date.now }
});

wishlistSchema.index({ userId: 1, productId: 1 }, { unique: true });
module.exports = mongoose.model('Wishlist', wishlistSchema, 'wishlist');

const mongoose = require('mongoose');

const cartItemSchema = new mongoose.Schema({
  id: { type: Number },
  cartId: { type: Number },
  productId: { type: Number },
  variantId: { type: Number },
  quantity: { type: Number, default: 1 },
  size: { type: String },
  product: {
    id: { type: Number },
    name: { type: String },
    price: { type: Number },
    images: [{ type: String }]
  }
}, { _id: false });

const cartSchema = new mongoose.Schema({
  id: { type: Number, required: true, unique: true },
  userId: { type: String, required: true },
  createdAt: { type: Date, default: Date.now },
  items: [cartItemSchema]
}, { timestamps: true });

module.exports = mongoose.model('Cart', cartSchema, 'carts');

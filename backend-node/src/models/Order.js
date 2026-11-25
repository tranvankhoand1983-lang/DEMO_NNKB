const mongoose = require('mongoose');

const orderItemSchema = new mongoose.Schema({
  id: { type: Number },
  orderId: { type: String },
  productId: { type: Number },
  variantId: { type: Number },
  quantity: { type: Number, default: 1 },
  size: { type: String },
  priceAtPurchase: { type: Number },
  product: {
    id: { type: Number },
    name: { type: String },
    price: { type: Number },
    images: [{ type: String }]
  }
}, { _id: false });

const orderSchema = new mongoose.Schema({
  id: { type: String, required: true, unique: true },
  userId: { type: String, required: true },
  date: { type: String },
  createdAt: { type: Date, default: Date.now },
  paidAt: { type: Date, default: null },
  paymentDate: { type: Date, default: null },
  recipientName: { type: String, required: true },
  firstName: { type: String },
  lastName: { type: String },
  email: { type: String, required: true },
  phone: { type: String, required: true },
  company: { type: String, default: '' },
  address: { type: String, required: true },
  apartment: { type: String, default: '' },
  city: { type: String, required: true },
  country: { type: String, default: 'Vietnam' },
  postalCode: { type: String, default: '' },
  shippingMethod: { type: String, default: 'free' },
  shippingFee: { type: Number, default: 0 },
  paymentMethod: { type: String, default: 'vietqr' },
  paymentStatus: { type: String, default: 'unpaid' },
  status: { type: String, default: 'pending' },
  orderStatus: { type: String, default: 'pending' },
  discountCode: { type: String, default: null },
  discountAmount: { type: Number, default: 0 },
  total: { type: Number, required: true },
  totalAmount: { type: Number, required: true },
  estimatedDelivery: { type: String, default: null },
  items: [orderItemSchema]
}, { timestamps: true });

module.exports = mongoose.model('Order', orderSchema, 'orders');

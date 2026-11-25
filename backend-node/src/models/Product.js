const mongoose = require('mongoose');

const variantSchema = new mongoose.Schema({
  id: { type: Number },
  productId: { type: Number },
  sku: { type: String },
  size: { type: String },
  price: { type: Number },
  originalPrice: { type: Number },
  stockQuantity: { type: Number, default: 0 },
  isSale: { type: Boolean, default: false },
  inStock: { type: Boolean, default: true },
  createdAt: { type: Date }
}, { _id: false });

const detailedImageSchema = new mongoose.Schema({
  id: { type: Number },
  productId: { type: Number },
  url: { type: String },
  isMain: { type: Number, default: 0 },
  displayOrder: { type: Number, default: 0 }
}, { _id: false });

const productSchema = new mongoose.Schema({
  id: { type: Number, required: true, unique: true },
  sku: { type: String, required: true },
  name: { type: String, required: true },
  price: { type: Number, required: true },
  originalPrice: { type: Number },
  category: { type: String },
  categoryId: { type: Number },
  categoryName: { type: String },
  material: { type: String },
  materialId: { type: Number },
  materialName: { type: String },
  description: { type: String },
  originStory: { type: String, default: null },
  stockQuantity: { type: Number, default: 0 },
  rating: { type: Number, default: 5.0 },
  reviews: { type: Number, default: 0 },
  reviewCount: { type: Number, default: 0 },
  isNew: { type: Boolean, default: false },
  isSale: { type: Boolean, default: false },
  inStock: { type: Boolean, default: true },
  availableSizes: [{ type: String }],
  images: [{ type: String }],
  detailedImages: [detailedImageSchema],
  variants: [variantSchema],
  createdAt: { type: Date, default: Date.now }
}, { timestamps: true, suppressReservedKeysWarning: true });

module.exports = mongoose.model('Product', productSchema, 'products');

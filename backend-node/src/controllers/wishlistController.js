const Wishlist = require('../models/Wishlist');
const Product = require('../models/Product');

exports.getWishlist = async (req, res) => {
  try {
    const list = await Wishlist.find({ userId: req.user.id });
    const productIds = list.map(w => w.productId);
    const products = await Product.find({ id: { $in: productIds } });
    res.json(products);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.addToWishlist = async (req, res) => {
  try {
    const userId = req.user.id;
    const productId = Number(req.params.productId);
    const existing = await Wishlist.findOne({ userId, productId });
    if (!existing) await Wishlist.create({ userId, productId });
    res.json({ message: 'Đã thêm vào danh sách ước' });
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};

exports.removeFromWishlist = async (req, res) => {
  try {
    await Wishlist.findOneAndDelete({ userId: req.user.id, productId: Number(req.params.productId) });
    res.json({ message: 'Đã xoá khỏi danh sách ước' });
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};

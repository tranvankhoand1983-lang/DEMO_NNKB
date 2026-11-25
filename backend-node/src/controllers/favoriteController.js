const Favorite = require('../models/Favorite');
const Product = require('../models/Product');

exports.getFavorites = async (req, res) => {
  try {
    const userId = req.user.id;
    const favorites = await Favorite.find({ userId });
    const productIds = favorites.map(f => f.productId);
    const products = await Product.find({ id: { $in: productIds } });
    res.json(products);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.addFavorite = async (req, res) => {
  try {
    const userId = req.user.id;
    const productId = Number(req.params.productId);
    
    const existing = await Favorite.findOne({ userId, productId });
    if (!existing) {
      await Favorite.create({ userId, productId });
    }
    res.json({ message: 'Đã thêm vào yêu thích' });
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};

exports.removeFavorite = async (req, res) => {
  try {
    const userId = req.user.id;
    const productId = Number(req.params.productId);
    await Favorite.findOneAndDelete({ userId, productId });
    res.json({ message: 'Đã xoá khỏi yêu thích' });
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};

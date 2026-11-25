const Banner = require('../models/Banner');

exports.getBanners = async (req, res) => {
  try {
    const banners = await Banner.find();
    res.json(banners);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.getActiveBanner = async (req, res) => {
  try {
    const banner = await Banner.findOne({ isActive: true });
    res.json(banner || null);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.createBanner = async (req, res) => {
  try {
    const maxB = await Banner.findOne().sort({ id: -1 });
    const newId = maxB ? maxB.id + 1 : 1;
    const banner = await Banner.create({ ...req.body, id: newId });
    res.status(201).json(banner);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};

exports.updateBanner = async (req, res) => {
  try {
    const banner = await Banner.findOneAndUpdate({ id: Number(req.params.id) }, req.body, { new: true });
    if (!banner) return res.status(404).json({ message: 'Không tìm thấy banner' });
    res.json(banner);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};

exports.deleteBanner = async (req, res) => {
  try {
    const banner = await Banner.findOneAndDelete({ id: Number(req.params.id) });
    if (!banner) return res.status(404).json({ message: 'Không tìm thấy banner' });
    res.json({ message: 'Xoá banner thành công' });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

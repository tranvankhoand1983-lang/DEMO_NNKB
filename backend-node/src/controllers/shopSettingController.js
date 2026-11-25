const ShopSetting = require('../models/ShopSetting');

exports.getShopSettings = async (req, res) => {
  try {
    const settings = await ShopSetting.findOne();
    res.json(settings || {});
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.updateShopSettings = async (req, res) => {
  try {
    let settings = await ShopSetting.findOne();
    if (settings) {
      settings = await ShopSetting.findOneAndUpdate({}, req.body, { new: true });
    } else {
      settings = await ShopSetting.create({ ...req.body, id: 1 });
    }
    res.json(settings);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};

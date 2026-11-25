const Promotion = require('../models/Promotion');
const UserVoucher = require('../models/UserVoucher');

exports.getPromotions = async (req, res) => {
  try {
    const promos = await Promotion.find().sort({ createdAt: -1 });
    res.json(promos);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.getAvailablePromotions = async (req, res) => {
  try {
    const now = new Date();
    const promos = await Promotion.find({
      isActive: true,
      isVisible: true
    });
    res.json(promos);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.getMyVouchers = async (req, res) => {
  try {
    const userId = req.user.id;
    const userVouchers = await UserVoucher.find({ userId, isUsed: false });
    const promoIds = userVouchers.map(uv => uv.promotionId);
    const promos = await Promotion.find({ id: { $in: promoIds }, isActive: true });
    res.json(promos);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.saveVoucher = async (req, res) => {
  try {
    const userId = req.user.id;
    const promotionId = Number(req.params.id);

    const existing = await UserVoucher.findOne({ userId, promotionId });
    if (existing) {
      return res.status(400).json({ message: 'Bạn đã lưu voucher này rồi' });
    }

    const maxUv = await UserVoucher.findOne().sort({ id: -1 });
    const newId = maxUv ? maxUv.id + 1 : 1;

    await UserVoucher.create({
      id: newId,
      userId,
      promotionId,
      savedAt: new Date(),
      isUsed: false
    });

    res.json({ message: 'Lưu voucher thành công' });
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};

exports.validatePromotion = async (req, res) => {
  try {
    const { code } = req.params;
    const orderAmount = Number(req.query.orderAmount || 0);

    const promo = await Promotion.findOne({ code: code.toUpperCase(), isActive: true });
    if (!promo) {
      return res.status(404).json({ message: 'Mã giảm giá không tồn tại hoặc đã hết hạn' });
    }

    if (promo.minOrderAmount && orderAmount < promo.minOrderAmount) {
      return res.status(400).json({ 
        message: `Đơn hàng tối thiểu phải từ ${promo.minOrderAmount.toLocaleString('vi-VN')}đ để dùng mã này` 
      });
    }

    let discountAmount = 0;
    if (promo.discount <= 100) {
      discountAmount = (orderAmount * promo.discount) / 100;
      if (promo.maxDiscountAmount && discountAmount > promo.maxDiscountAmount) {
        discountAmount = promo.maxDiscountAmount;
      }
    } else {
      discountAmount = promo.discount;
    }

    res.json({
      valid: true,
      promotion: promo,
      discountAmount: discountAmount
    });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.createPromotion = async (req, res) => {
  try {
    const maxP = await Promotion.findOne().sort({ id: -1 });
    const newId = maxP ? maxP.id + 1 : 1;
    const promo = await Promotion.create({ ...req.body, id: newId, code: req.body.code.toUpperCase() });
    res.status(201).json(promo);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};

exports.deletePromotion = async (req, res) => {
  try {
    await Promotion.findOneAndDelete({ id: Number(req.params.id) });
    res.json({ message: 'Xoá mã giảm giá thành công' });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

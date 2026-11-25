import os

base_dir = r'C:\Web_NangCao_locallhost\web-trang-suc-nnkb\backend-node\src'
controllers_dir = os.path.join(base_dir, 'controllers')
routes_dir = os.path.join(base_dir, 'routes')

# ==========================================
# GROUP 2: Account & Customer
# ==========================================
account_ctrl = '''const User = require('../models/User');
const bcrypt = require('bcryptjs');
const jwt = require('jsonwebtoken');
const { v4: uuidv4 } = require('uuid');

const generateToken = (user) => {
  return jwt.sign(
    { id: user.id, email: user.email, role: user.role },
    process.env.JWT_SECRET || 'velmora_super_secure_jwt_secret_key_2026_epu',
    { expiresIn: process.env.JWT_EXPIRES_IN || '7d' }
  );
};

exports.register = async (req, res) => {
  try {
    const { fullName, email, password } = req.body;
    if (!email || !password || !fullName) {
      return res.status(400).json({ message: 'Vui lòng điền đầy đủ họ tên, email và mật khẩu' });
    }

    const existing = await User.findOne({ email });
    if (existing) {
      return res.status(400).json({ message: 'Email này đã được sử dụng' });
    }

    const salt = await bcrypt.genSalt(10);
    const hashedPassword = await bcrypt.hash(password, salt);

    const user = await User.create({
      id: uuidv4(),
      fullName,
      name: fullName,
      email,
      password: hashedPassword,
      role: 'customer',
      provider: 'email',
      isActive: true
    });

    const token = generateToken(user);
    res.cookie('token', token, { httpOnly: true, secure: process.env.NODE_ENV === 'production', maxAge: 7 * 24 * 3600 * 1000 });
    res.status(201).json({
      token,
      user: {
        id: user.id,
        name: user.fullName,
        fullName: user.fullName,
        email: user.email,
        role: user.role,
        provider: user.provider,
        avatar: user.avatar
      }
    });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.login = async (req, res) => {
  try {
    const { email, password } = req.body;
    if (!email || !password) {
      return res.status(400).json({ message: 'Vui lòng nhập email và mật khẩu' });
    }

    const user = await User.findOne({ email });
    if (!user) {
      return res.status(400).json({ message: 'Email hoặc mật khẩu không chính xác' });
    }

    if (!user.isActive) {
      return res.status(403).json({ message: 'Tài khoản của bạn đã bị khoá' });
    }

    // Check plain admin pass or bcrypt
    let isMatch = false;
    if (user.password && user.password.startsWith('$2')) {
      isMatch = await bcrypt.compare(password, user.password);
    } else {
      isMatch = user.password === password;
    }

    if (!isMatch) {
      return res.status(400).json({ message: 'Email hoặc mật khẩu không chính xác' });
    }

    const token = generateToken(user);
    res.cookie('token', token, { httpOnly: true, secure: process.env.NODE_ENV === 'production', maxAge: 7 * 24 * 3600 * 1000 });
    res.json({
      token,
      user: {
        id: user.id,
        name: user.fullName,
        fullName: user.fullName,
        email: user.email,
        role: user.role,
        provider: user.provider,
        avatar: user.avatar
      }
    });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.googleLogin = async (req, res) => {
  try {
    const { email, name, avatar, googleId } = req.body;
    if (!email) return res.status(400).json({ message: 'Thiếu thông tin email Google' });

    let user = await User.findOne({ email });
    if (!user) {
      user = await User.create({
        id: uuidv4(),
        fullName: name || email.split('@')[0],
        name: name || email.split('@')[0],
        email,
        avatar: avatar || null,
        provider: 'google',
        role: 'customer',
        isActive: true
      });
    }

    const token = generateToken(user);
    res.cookie('token', token, { httpOnly: true, secure: process.env.NODE_ENV === 'production', maxAge: 7 * 24 * 3600 * 1000 });
    res.json({
      token,
      user: {
        id: user.id,
        name: user.fullName,
        fullName: user.fullName,
        email: user.email,
        role: user.role,
        provider: user.provider,
        avatar: user.avatar
      }
    });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.changePassword = async (req, res) => {
  try {
    const { currentPassword, newPassword } = req.body;
    const user = await User.findOne({ id: req.user.id });
    if (!user) return res.status(404).json({ message: 'Người dùng không tồn tại' });

    let isMatch = false;
    if (user.password && user.password.startsWith('$2')) {
      isMatch = await bcrypt.compare(currentPassword, user.password);
    } else {
      isMatch = user.password === currentPassword;
    }

    if (!isMatch) return res.status(400).json({ message: 'Mật khẩu hiện tại không chính xác' });

    const salt = await bcrypt.genSalt(10);
    user.password = await bcrypt.hash(newPassword, salt);
    await user.save();

    res.json({ message: 'Đổi mật khẩu thành công' });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.forgotPassword = async (req, res) => {
  try {
    const { email } = req.body;
    const user = await User.findOne({ email });
    if (!user) return res.status(404).json({ message: 'Email không tồn tại trong hệ thống' });
    res.json({ message: 'Đã gửi hướng dẫn đặt lại mật khẩu về email của bạn' });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};
'''
with open(os.path.join(controllers_dir, 'accountController.js'), 'w', encoding='utf-8') as f:
    f.write(account_ctrl)

account_routes = '''const express = require('express');
const router = express.Router();
const accountController = require('../controllers/accountController');
const { protect } = require('../middlewares/authMiddleware');

router.post('/register', accountController.register);
router.post('/login', accountController.login);
router.post('/google-login', accountController.googleLogin);
router.put('/change-password', protect, accountController.changePassword);
router.post('/change-password', protect, accountController.changePassword);
router.post('/forgot-password', accountController.forgotPassword);

module.exports = router;
'''
with open(os.path.join(routes_dir, 'accountRoutes.js'), 'w', encoding='utf-8') as f:
    f.write(account_routes)

# Customer Management for Admin
customer_ctrl = '''const User = require('../models/User');

exports.getCustomers = async (req, res) => {
  try {
    const customers = await User.find().select('-password').sort({ createdAt: -1 });
    res.json(customers);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.getCustomerById = async (req, res) => {
  try {
    const customer = await User.findOne({ id: req.params.id }).select('-password');
    if (!customer) return res.status(404).json({ message: 'Không tìm thấy khách hàng' });
    res.json(customer);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.updateCustomer = async (req, res) => {
  try {
    const customer = await User.findOneAndUpdate({ id: req.params.id }, req.body, { new: true }).select('-password');
    if (!customer) return res.status(404).json({ message: 'Không tìm thấy khách hàng' });
    res.json(customer);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};

exports.deleteCustomer = async (req, res) => {
  try {
    const customer = await User.findOneAndDelete({ id: req.params.id });
    if (!customer) return res.status(404).json({ message: 'Không tìm thấy khách hàng' });
    res.json({ message: 'Xoá khách hàng thành công' });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};
'''
with open(os.path.join(controllers_dir, 'customerController.js'), 'w', encoding='utf-8') as f:
    f.write(customer_ctrl)

customer_routes = '''const express = require('express');
const router = express.Router();
const customerController = require('../controllers/customerController');
const { protect, authorize } = require('../middlewares/authMiddleware');

router.get('/', protect, authorize('admin', 'staff'), customerController.getCustomers);
router.get('/:id', protect, authorize('admin', 'staff'), customerController.getCustomerById);
router.put('/:id', protect, authorize('admin'), customerController.updateCustomer);
router.delete('/:id', protect, authorize('admin'), customerController.deleteCustomer);

module.exports = router;
'''
with open(os.path.join(routes_dir, 'customerRoutes.js'), 'w', encoding='utf-8') as f:
    f.write(customer_routes)

# ==========================================
# GROUP 3: Carts, Orders, Payment / PayOS
# ==========================================
cart_ctrl = '''const Cart = require('../models/Cart');
const Product = require('../models/Product');

exports.getCart = async (req, res) => {
  try {
    const userId = req.user.id;
    let cart = await Cart.findOne({ userId });
    if (!cart) {
      const maxC = await Cart.findOne().sort({ id: -1 });
      const newId = maxC ? maxC.id + 1 : 1;
      cart = await Cart.create({ id: newId, userId, items: [] });
    }
    res.json(cart.items || []);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.addToCart = async (req, res) => {
  try {
    const userId = req.user.id;
    const { productId, variantId, quantity, size } = req.body;

    const product = await Product.findOne({ id: Number(productId) });
    if (!product) return res.status(404).json({ message: 'Sản phẩm không tồn tại' });

    let cart = await Cart.findOne({ userId });
    if (!cart) {
      const maxC = await Cart.findOne().sort({ id: -1 });
      const newId = maxC ? maxC.id + 1 : 1;
      cart = await Cart.create({ id: newId, userId, items: [] });
    }

    const existingItem = cart.items.find(i => 
      i.productId === Number(productId) && 
      (!variantId || i.variantId === Number(variantId)) &&
      (!size || i.size === size)
    );

    if (existingItem) {
      existingItem.quantity += (Number(quantity) || 1);
    } else {
      const maxItemId = cart.items.reduce((max, i) => Math.max(max, i.id || 0), 0);
      cart.items.push({
        id: maxItemId + 1,
        cartId: cart.id,
        productId: Number(productId),
        variantId: variantId ? Number(variantId) : null,
        quantity: Number(quantity) || 1,
        size: size || null,
        product: {
          id: product.id,
          name: product.name,
          price: product.price,
          images: product.images
        }
      });
    }

    await cart.save();
    res.status(200).json(cart.items);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};

exports.updateQuantity = async (req, res) => {
  try {
    const userId = req.user.id;
    const { cartItemId, id, quantity } = req.body;
    const targetId = Number(cartItemId || id);

    const cart = await Cart.findOne({ userId });
    if (!cart) return res.status(404).json({ message: 'Giỏ hàng không tồn tại' });

    const item = cart.items.find(i => i.id === targetId);
    if (!item) return res.status(404).json({ message: 'Món hàng không tồn tại trong giỏ' });

    if (Number(quantity) <= 0) {
      cart.items = cart.items.filter(i => i.id !== targetId);
    } else {
      item.quantity = Number(quantity);
    }

    await cart.save();
    res.json(cart.items);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};

exports.removeFromCart = async (req, res) => {
  try {
    const userId = req.user.id;
    const { cartItemId, id } = req.body;
    const targetId = Number(cartItemId || id);

    const cart = await Cart.findOne({ userId });
    if (!cart) return res.status(404).json({ message: 'Giỏ hàng không tồn tại' });

    cart.items = cart.items.filter(i => i.id !== targetId);
    await cart.save();
    res.json(cart.items);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};

exports.clearCart = async (req, res) => {
  try {
    const userId = req.user.id;
    await Cart.findOneAndUpdate({ userId }, { items: [] });
    res.json({ message: 'Đã làm trống giỏ hàng' });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};
'''
with open(os.path.join(controllers_dir, 'cartController.js'), 'w', encoding='utf-8') as f:
    f.write(cart_ctrl)

cart_routes = '''const express = require('express');
const router = express.Router();
const cartController = require('../controllers/cartController');
const { protect } = require('../middlewares/authMiddleware');

router.get('/', protect, cartController.getCart);
router.post('/items', protect, cartController.addToCart);
router.put('/items', protect, cartController.updateQuantity);
router.delete('/items', protect, cartController.removeFromCart);
router.delete('/', protect, cartController.clearCart);

module.exports = router;
'''
with open(os.path.join(routes_dir, 'cartRoutes.js'), 'w', encoding='utf-8') as f:
    f.write(cart_routes)

# Orders
order_ctrl = '''const Order = require('../models/Order');
const Cart = require('../models/Cart');

exports.getAllOrders = async (req, res) => {
  try {
    const orders = await Order.find().sort({ createdAt: -1 });
    res.json(orders);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.getMyOrders = async (req, res) => {
  try {
    const orders = await Order.find({ userId: req.user.id }).sort({ createdAt: -1 });
    res.json(orders);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.getOrderDetails = async (req, res) => {
  try {
    const order = await Order.findOne({ id: req.params.id });
    if (!order) return res.status(404).json({ message: 'Không tìm thấy đơn hàng' });
    res.json(order);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.placeOrder = async (req, res) => {
  try {
    const userId = req.user.id;
    const { 
      shipping, items, total, totalAmount, paymentMethod, shippingMethod, 
      discountCode, discountAmount, recipientName, phone, email, address, city 
    } = req.body;

    const orderId = 'ORD-' + Date.now().toString().slice(-8);

    const shipInfo = shipping || {};
    const orderDoc = {
      id: orderId,
      userId: userId,
      recipientName: recipientName || `${shipInfo.firstName || ''} ${shipInfo.lastName || ''}`.trim() || req.user.fullName,
      firstName: shipInfo.firstName || '',
      lastName: shipInfo.lastName || '',
      email: email || shipInfo.email || req.user.email,
      phone: phone || shipInfo.phone || req.user.phone || '0900000000',
      company: shipInfo.company || '',
      address: address || shipInfo.address || 'N/A',
      apartment: shipInfo.apartment || '',
      city: city || shipInfo.city || 'Hà Nội',
      country: shipInfo.country || 'Vietnam',
      postalCode: shipInfo.postalCode || '',
      shippingMethod: shippingMethod || 'free',
      shippingFee: 0,
      paymentMethod: paymentMethod || 'vietqr',
      paymentStatus: paymentMethod === 'cod' ? 'unpaid' : 'pending',
      orderStatus: 'pending',
      status: 'pending',
      discountCode: discountCode || null,
      discountAmount: Number(discountAmount) || 0,
      total: Number(total || totalAmount) || 0,
      totalAmount: Number(total || totalAmount) || 0,
      items: (items || []).map((it, idx) => ({
        id: idx + 1,
        orderId: orderId,
        productId: it.productId || it.product?.id,
        variantId: it.variantId || null,
        quantity: it.quantity || 1,
        size: it.size || null,
        priceAtPurchase: it.priceAtPurchase || it.product?.price || 0,
        product: it.product || null
      }))
    };

    const newOrder = await Order.create(orderDoc);

    // Clear user cart after placing order
    await Cart.findOneAndUpdate({ userId }, { items: [] });

    res.status(201).json({
      success: true,
      message: 'Đặt hàng thành công',
      orderId: newOrder.id,
      order: newOrder
    });
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};

exports.updateOrderStatus = async (req, res) => {
  try {
    const { status, orderStatus } = req.body;
    const newStatus = status || orderStatus;
    const order = await Order.findOneAndUpdate(
      { id: req.params.id }, 
      { status: newStatus, orderStatus: newStatus },
      { new: true }
    );
    if (!order) return res.status(404).json({ message: 'Không tìm thấy đơn hàng' });
    res.json(order);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};
'''
with open(os.path.join(controllers_dir, 'orderController.js'), 'w', encoding='utf-8') as f:
    f.write(order_ctrl)

order_routes = '''const express = require('express');
const router = express.Router();
const orderController = require('../controllers/orderController');
const { protect, authorize } = require('../middlewares/authMiddleware');

router.get('/', protect, authorize('admin', 'staff'), orderController.getAllOrders);
router.get('/my-orders', protect, orderController.getMyOrders);
router.get('/:id', protect, orderController.getOrderDetails);
router.post('/place-order', protect, orderController.placeOrder);
router.post('/', protect, orderController.placeOrder);
router.put('/:id', protect, authorize('admin', 'staff'), orderController.updateOrderStatus);

module.exports = router;
'''
with open(os.path.join(routes_dir, 'orderRoutes.js'), 'w', encoding='utf-8') as f:
    f.write(order_routes)

# PayOS / Payment
payment_ctrl = '''const Order = require('../models/Order');

exports.createPaymentLink = async (req, res) => {
  try {
    const { orderId, amount } = req.body;
    const targetOrderId = orderId || req.params.orderId;
    
    const order = await Order.findOne({ id: targetOrderId });
    if (!order) return res.status(404).json({ message: 'Không tìm thấy đơn hàng' });

    const orderAmount = Number(amount || order.totalAmount);
    const orderCode = Number(Date.now().toString().slice(-6));

    // Simulated VietQR / PayOS Payment URL
    const frontendUrl = process.env.CLIENT_URL || 'http://localhost:5173';
    const checkoutUrl = `${frontendUrl}/checkout/success?orderId=${targetOrderId}&orderCode=${orderCode}&status=PAID`;

    res.json({
      url: checkoutUrl,
      checkoutUrl: checkoutUrl,
      orderCode: orderCode,
      orderId: targetOrderId
    });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.checkStatus = async (req, res) => {
  try {
    const { orderId } = req.params;
    const order = await Order.findOne({ id: orderId });
    if (!order) return res.status(404).json({ message: 'Không tìm thấy đơn hàng' });
    res.json({
      id: order.id,
      orderStatus: order.orderStatus,
      paymentStatus: order.paymentStatus
    });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.syncStatus = async (req, res) => {
  try {
    const { orderId, status } = req.query;
    const order = await Order.findOne({ id: orderId });
    if (!order) return res.status(404).json({ success: false, message: 'Không tìm thấy đơn hàng' });

    if (status === 'PAID') {
      order.paymentStatus = 'Paid';
      order.orderStatus = 'Chờ lấy hàng';
      order.status = 'processing';
      order.paidAt = new Date();
      await order.save();
    } else if (status === 'CANCELLED') {
      order.paymentStatus = 'Failed';
      order.orderStatus = 'Hủy';
      order.status = 'cancelled';
      await order.save();
    }

    res.json({
      success: true,
      paymentStatus: order.paymentStatus,
      orderStatus: order.orderStatus
    });
  } catch (err) {
    res.status(500).json({ success: false, message: err.message });
  }
};
'''
with open(os.path.join(controllers_dir, 'paymentController.js'), 'w', encoding='utf-8') as f:
    f.write(payment_ctrl)

payment_routes = '''const express = require('express');
const router = express.Router();
const paymentController = require('../controllers/paymentController');

router.post('/create-payment-link', paymentController.createPaymentLink);
router.post('/create-payment-link/:orderId', paymentController.createPaymentLink);
router.get('/check-status/:orderId', paymentController.checkStatus);
router.get('/sync-status', paymentController.syncStatus);

module.exports = router;
'''
with open(os.path.join(routes_dir, 'paymentRoutes.js'), 'w', encoding='utf-8') as f:
    f.write(payment_routes)

# ==========================================
# GROUP 4: Favorites, Promotions, Reviews, Wishlist
# ==========================================
favorite_ctrl = '''const Favorite = require('../models/Favorite');
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
'''
with open(os.path.join(controllers_dir, 'favoriteController.js'), 'w', encoding='utf-8') as f:
    f.write(favorite_ctrl)

favorite_routes = '''const express = require('express');
const router = express.Router();
const favoriteController = require('../controllers/favoriteController');
const { protect } = require('../middlewares/authMiddleware');

router.get('/', protect, favoriteController.getFavorites);
router.post('/:productId', protect, favoriteController.addFavorite);
router.delete('/:productId', protect, favoriteController.removeFavorite);

module.exports = router;
'''
with open(os.path.join(routes_dir, 'favoriteRoutes.js'), 'w', encoding='utf-8') as f:
    f.write(favorite_routes)

# Promotions
promotion_ctrl = '''const Promotion = require('../models/Promotion');
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
'''
with open(os.path.join(controllers_dir, 'promotionController.js'), 'w', encoding='utf-8') as f:
    f.write(promotion_ctrl)

promotion_routes = '''const express = require('express');
const router = express.Router();
const promotionController = require('../controllers/promotionController');
const { protect, authorize } = require('../middlewares/authMiddleware');

router.get('/', promotionController.getPromotions);
router.get('/available', promotionController.getAvailablePromotions);
router.get('/my-vouchers', protect, promotionController.getMyVouchers);
router.get('/validate/:code', promotionController.validatePromotion);
router.post('/save/:id', protect, promotionController.saveVoucher);
router.post('/', protect, authorize('admin'), promotionController.createPromotion);
router.delete('/:id', protect, authorize('admin'), promotionController.deletePromotion);

module.exports = router;
'''
with open(os.path.join(routes_dir, 'promotionRoutes.js'), 'w', encoding='utf-8') as f:
    f.write(promotion_routes)

# Reviews
review_ctrl = '''const Review = require('../models/Review');

exports.getReviewsByProduct = async (req, res) => {
  try {
    const reviews = await Review.find({ product_id: Number(req.params.id) }).sort({ created_at: -1 });
    res.json(reviews);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.createReview = async (req, res) => {
  try {
    const maxR = await Review.findOne().sort({ id: -1 });
    const newId = maxR ? maxR.id + 1 : 1;
    const review = await Review.create({
      id: newId,
      user_id: req.user.id,
      product_id: Number(req.body.productId || req.body.product_id),
      rating: Number(req.body.rating),
      comment: req.body.comment,
      created_at: new Date()
    });
    res.status(201).json(review);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};
'''
with open(os.path.join(controllers_dir, 'reviewController.js'), 'w', encoding='utf-8') as f:
    f.write(review_ctrl)

review_routes = '''const express = require('express');
const router = express.Router();
const reviewController = require('../controllers/reviewController');
const { protect } = require('../middlewares/authMiddleware');

router.get('/product/:id', reviewController.getReviewsByProduct);
router.post('/', protect, reviewController.createReview);

module.exports = router;
'''
with open(os.path.join(routes_dir, 'reviewRoutes.js'), 'w', encoding='utf-8') as f:
    f.write(review_routes)

# Wishlist
wishlist_ctrl = '''const Wishlist = require('../models/Wishlist');
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
'''
with open(os.path.join(controllers_dir, 'wishlistController.js'), 'w', encoding='utf-8') as f:
    f.write(wishlist_ctrl)

wishlist_routes = '''const express = require('express');
const router = express.Router();
const wishlistController = require('../controllers/wishlistController');
const { protect } = require('../middlewares/authMiddleware');

router.get('/', protect, wishlistController.getWishlist);
router.post('/:productId', protect, wishlistController.addToWishlist);
router.delete('/:productId', protect, wishlistController.removeFromWishlist);

module.exports = router;
'''
with open(os.path.join(routes_dir, 'wishlistRoutes.js'), 'w', encoding='utf-8') as f:
    f.write(wishlist_routes)

# ==========================================
# GROUP 5: Statistics, Services, Suppliers, Chat
# ==========================================
stats_ctrl = '''const Order = require('../models/Order');
const Product = require('../models/Product');
const User = require('../models/User');

exports.getDashboardStats = async (req, res) => {
  try {
    const totalOrders = await Order.countDocuments();
    const totalProducts = await Product.countDocuments();
    const totalUsers = await User.countDocuments();

    const orders = await Order.find();
    const totalRevenue = orders.reduce((sum, o) => sum + (Number(o.totalAmount) || 0), 0);

    const recentOrders = await Order.find().sort({ createdAt: -1 }).limit(5);

    res.json({
      totalRevenue,
      totalOrders,
      totalProducts,
      totalCustomers: totalUsers,
      recentOrders
    });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};
'''
with open(os.path.join(controllers_dir, 'statisticsController.js'), 'w', encoding='utf-8') as f:
    f.write(stats_ctrl)

stats_routes = '''const express = require('express');
const router = express.Router();
const statisticsController = require('../controllers/statisticsController');
const { protect, authorize } = require('../middlewares/authMiddleware');

router.get('/dashboard', protect, authorize('admin', 'staff'), statisticsController.getDashboardStats);

module.exports = router;
'''
with open(os.path.join(routes_dir, 'statisticsRoutes.js'), 'w', encoding='utf-8') as f:
    f.write(stats_routes)

# Services
service_ctrl = '''const Service = require('../models/Service');

exports.getServices = async (req, res) => {
  try {
    const services = await Service.find();
    res.json(services);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.getServiceById = async (req, res) => {
  try {
    const service = await Service.findOne({ id: Number(req.params.id) });
    if (!service) return res.status(404).json({ message: 'Không tìm thấy dịch vụ' });
    res.json(service);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.createService = async (req, res) => {
  try {
    const maxS = await Service.findOne().sort({ id: -1 });
    const newId = maxS ? maxS.id + 1 : 1;
    const s = await Service.create({ ...req.body, id: newId });
    res.status(201).json(s);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};

exports.deleteService = async (req, res) => {
  try {
    await Service.findOneAndDelete({ id: Number(req.params.id) });
    res.json({ message: 'Xoá dịch vụ thành công' });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};
'''
with open(os.path.join(controllers_dir, 'serviceController.js'), 'w', encoding='utf-8') as f:
    f.write(service_ctrl)

service_routes = '''const express = require('express');
const router = express.Router();
const serviceController = require('../controllers/serviceController');
const { protect, authorize } = require('../middlewares/authMiddleware');

router.get('/', serviceController.getServices);
router.get('/:id', serviceController.getServiceById);
router.post('/', protect, authorize('admin'), serviceController.createService);
router.delete('/:id', protect, authorize('admin'), serviceController.deleteService);

module.exports = router;
'''
with open(os.path.join(routes_dir, 'serviceRoutes.js'), 'w', encoding='utf-8') as f:
    f.write(service_routes)

# Suppliers
supplier_ctrl = '''const Supplier = require('../models/Supplier');

exports.getSuppliers = async (req, res) => {
  try {
    const suppliers = await Supplier.find();
    res.json(suppliers);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.getSupplierById = async (req, res) => {
  try {
    const supplier = await Supplier.findOne({ id: Number(req.params.id) });
    if (!supplier) return res.status(404).json({ message: 'Không tìm thấy nhà cung cấp' });
    res.json(supplier);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.createSupplier = async (req, res) => {
  try {
    const maxS = await Supplier.findOne().sort({ id: -1 });
    const newId = maxS ? maxS.id + 1 : 1;
    const s = await Supplier.create({ ...req.body, id: newId });
    res.status(201).json(s);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};

exports.deleteSupplier = async (req, res) => {
  try {
    await Supplier.findOneAndDelete({ id: Number(req.params.id) });
    res.json({ message: 'Xoá nhà cung cấp thành công' });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};
'''
with open(os.path.join(controllers_dir, 'supplierController.js'), 'w', encoding='utf-8') as f:
    f.write(supplier_ctrl)

supplier_routes = '''const express = require('express');
const router = express.Router();
const supplierController = require('../controllers/supplierController');
const { protect, authorize } = require('../middlewares/authMiddleware');

router.get('/', supplierController.getSuppliers);
router.get('/:id', supplierController.getSupplierById);
router.post('/', protect, authorize('admin'), supplierController.createSupplier);
router.delete('/:id', protect, authorize('admin'), supplierController.deleteSupplier);

module.exports = router;
'''
with open(os.path.join(routes_dir, 'supplierRoutes.js'), 'w', encoding='utf-8') as f:
    f.write(supplier_routes)

# Chat (AI Chatbot assistant)
chat_ctrl = '''exports.handleChat = async (req, res) => {
  try {
    const { message } = req.body;
    if (!message) return res.status(400).json({ reply: 'Vui lòng nhập tin nhắn' });

    const lower = message.toLowerCase();
    let reply = 'Chào bạn! Tôi là trợ lý ảo Velmora Jewelry. Tôi có thể hỗ trợ tư vấn chọn size nhẫn, gợi ý trang sức phong thuỷ và kiểm tra chính sách bảo hành.';

    if (lower.includes('nhẫn') || lower.includes('size')) {
      reply = 'Để đo size nhẫn chuẩn xác: Bạn dùng một sợi chỉ quấn quanh ngón tay, đo chiều dài mm rồi chia cho 3.14 là ra đường kính lòng nhẫn (Size 5 tương ứng 49mm, Size 6 tương ứng 51mm, Size 7 tương ứng 53mm).';
    } else if (lower.includes('vàng') || lower.includes('chất liệu')) {
      reply = 'Velmora cung cấp các dòng trang sức Bạc S925 mạ Rhodium cao cấp, Vàng 18K và Kim Cương nhân tạo đạt chuẩn quốc tế.';
    } else if (lower.includes('giao hàng') || lower.includes('ship')) {
      reply = 'Velmora miễn phí giao hàng toàn quốc cho tất cả đơn hàng từ 500.000đ. Thời gian giao hàng tiêu chuẩn từ 2 - 4 ngày làm việc.';
    } else if (lower.includes('đổi trả') || lower.includes('bảo hành')) {
      reply = 'Chính sách bảo hành: Bảo hành làm sạch, đánh bóng miễn phí trọn đời và hỗ trợ đổi size trong vòng 7 ngày kể từ khi nhận hàng.';
    }

    res.json({ reply });
  } catch (err) {
    res.status(500).json({ reply: 'Có lỗi xảy ra, vui lòng thử lại sau.' });
  }
};
'''
with open(os.path.join(controllers_dir, 'chatController.js'), 'w', encoding='utf-8') as f:
    f.write(chat_ctrl)

chat_routes = '''const express = require('express');
const router = express.Router();
const chatController = require('../controllers/chatController');

router.post('/', chatController.handleChat);

module.exports = router;
'''
with open(os.path.join(routes_dir, 'chatRoutes.js'), 'w', encoding='utf-8') as f:
    f.write(chat_routes)

print("Generated ALL remaining groups successfully!")

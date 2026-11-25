const Order = require('../models/Order');
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

const Order = require('../models/Order');

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

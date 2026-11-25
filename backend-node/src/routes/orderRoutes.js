const express = require('express');
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

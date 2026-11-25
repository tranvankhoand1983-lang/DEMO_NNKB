const express = require('express');
const router = express.Router();
const cartController = require('../controllers/cartController');
const { protect } = require('../middlewares/authMiddleware');

router.get('/', protect, cartController.getCart);
router.post('/items', protect, cartController.addToCart);
router.put('/items', protect, cartController.updateQuantity);
router.delete('/items', protect, cartController.removeFromCart);
router.delete('/', protect, cartController.clearCart);

module.exports = router;

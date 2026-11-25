const express = require('express');
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

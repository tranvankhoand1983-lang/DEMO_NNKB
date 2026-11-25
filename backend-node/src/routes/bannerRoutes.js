const express = require('express');
const router = express.Router();
const bannerController = require('../controllers/bannerController');
const { protect, authorize } = require('../middlewares/authMiddleware');

router.get('/', bannerController.getBanners);
router.get('/active', bannerController.getActiveBanner);
router.post('/', protect, authorize('admin'), bannerController.createBanner);
router.put('/:id', protect, authorize('admin'), bannerController.updateBanner);
router.delete('/:id', protect, authorize('admin'), bannerController.deleteBanner);

module.exports = router;

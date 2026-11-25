const express = require('express');
const router = express.Router();
const shopSettingController = require('../controllers/shopSettingController');
const { protect, authorize } = require('../middlewares/authMiddleware');

router.get('/', shopSettingController.getShopSettings);
router.put('/', protect, authorize('admin'), shopSettingController.updateShopSettings);

module.exports = router;

const express = require('express');
const router = express.Router();
const serviceController = require('../controllers/serviceController');
const { protect, authorize } = require('../middlewares/authMiddleware');

router.get('/', serviceController.getServices);
router.get('/:id', serviceController.getServiceById);
router.post('/', protect, authorize('admin'), serviceController.createService);
router.delete('/:id', protect, authorize('admin'), serviceController.deleteService);

module.exports = router;

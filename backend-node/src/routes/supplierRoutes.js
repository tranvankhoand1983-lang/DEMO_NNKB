const express = require('express');
const router = express.Router();
const supplierController = require('../controllers/supplierController');
const { protect, authorize } = require('../middlewares/authMiddleware');

router.get('/', supplierController.getSuppliers);
router.get('/:id', supplierController.getSupplierById);
router.post('/', protect, authorize('admin'), supplierController.createSupplier);
router.delete('/:id', protect, authorize('admin'), supplierController.deleteSupplier);

module.exports = router;

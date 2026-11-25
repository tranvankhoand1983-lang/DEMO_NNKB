const express = require('express');
const router = express.Router();
const paymentController = require('../controllers/paymentController');

router.post('/create-payment-link', paymentController.createPaymentLink);
router.post('/create-payment-link/:orderId', paymentController.createPaymentLink);
router.get('/check-status/:orderId', paymentController.checkStatus);
router.get('/sync-status', paymentController.syncStatus);

module.exports = router;

const express = require('express');
const router = express.Router();
const accountController = require('../controllers/accountController');
const { protect } = require('../middlewares/authMiddleware');

router.post('/register', accountController.register);
router.post('/login', accountController.login);
router.post('/google-login', accountController.googleLogin);
router.put('/change-password', protect, accountController.changePassword);
router.post('/change-password', protect, accountController.changePassword);
router.post('/forgot-password', accountController.forgotPassword);

module.exports = router;

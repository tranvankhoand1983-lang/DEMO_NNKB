const express = require('express');
const router = express.Router();
const favoriteController = require('../controllers/favoriteController');
const { protect } = require('../middlewares/authMiddleware');

router.get('/', protect, favoriteController.getFavorites);
router.post('/:productId', protect, favoriteController.addFavorite);
router.delete('/:productId', protect, favoriteController.removeFavorite);

module.exports = router;

const Review = require('../models/Review');

exports.getReviewsByProduct = async (req, res) => {
  try {
    const reviews = await Review.find({ product_id: Number(req.params.id) }).sort({ created_at: -1 });
    res.json(reviews);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.createReview = async (req, res) => {
  try {
    const maxR = await Review.findOne().sort({ id: -1 });
    const newId = maxR ? maxR.id + 1 : 1;
    const review = await Review.create({
      id: newId,
      user_id: req.user.id,
      product_id: Number(req.body.productId || req.body.product_id),
      rating: Number(req.body.rating),
      comment: req.body.comment,
      created_at: new Date()
    });
    res.status(201).json(review);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};

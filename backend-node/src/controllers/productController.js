const Product = require('../models/Product');

// GET /api/products
exports.getProducts = async (req, res) => {
  try {
    const { search, category, material, minPrice, maxPrice, sort } = req.query;
    let query = {};

    if (search) {
      query.$or = [
        { name: { $regex: search, $options: 'i' } },
        { sku: { $regex: search, $options: 'i' } },
        { description: { $regex: search, $options: 'i' } }
      ];
    }
    if (category) {
      query.$or = [{ category: category }, { categoryName: category }];
    }
    if (material) {
      query.$or = [{ material: material }, { materialName: material }];
    }
    if (minPrice || maxPrice) {
      query.price = {};
      if (minPrice) query.price.$gte = Number(minPrice);
      if (maxPrice) query.price.$lte = Number(maxPrice);
    }

    let sortOption = { id: 1 };
    if (sort === 'price-asc') sortOption = { price: 1 };
    else if (sort === 'price-desc') sortOption = { price: -1 };
    else if (sort === 'newest') sortOption = { createdAt: -1 };
    else if (sort === 'popular') sortOption = { rating: -1, reviews: -1 };

    const products = await Product.find(query).sort(sortOption);
    res.json(products);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

// GET /api/products/:id
exports.getProductById = async (req, res) => {
  try {
    const id = Number(req.params.id);
    const product = await Product.findOne({ id });
    if (!product) {
      return res.status(404).json({ message: 'Không tìm thấy sản phẩm' });
    }
    res.json(product);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

// POST /api/products
exports.createProduct = async (req, res) => {
  try {
    const maxProd = await Product.findOne().sort({ id: -1 });
    const newId = maxProd ? maxProd.id + 1 : 1;
    
    const prodData = { ...req.body, id: newId };
    if (!prodData.images && prodData.detailedImages) {
      prodData.images = prodData.detailedImages.map(img => img.url);
    }
    const product = await Product.create(prodData);
    res.status(201).json(product);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};

// PUT /api/products/:id
exports.updateProduct = async (req, res) => {
  try {
    const id = Number(req.params.id);
    const product = await Product.findOneAndUpdate({ id }, req.body, { new: true });
    if (!product) return res.status(404).json({ message: 'Không tìm thấy sản phẩm' });
    res.json(product);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};

// DELETE /api/products/:id
exports.deleteProduct = async (req, res) => {
  try {
    const id = Number(req.params.id);
    const product = await Product.findOneAndDelete({ id });
    if (!product) return res.status(404).json({ message: 'Không tìm thấy sản phẩm' });
    res.json({ message: 'Xoá sản phẩm thành công' });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

import os

base_dir = r'C:\Web_NangCao_locallhost\web-trang-suc-nnkb\backend-node\src'
controllers_dir = os.path.join(base_dir, 'controllers')
routes_dir = os.path.join(base_dir, 'routes')
middlewares_dir = os.path.join(base_dir, 'middlewares')

os.makedirs(controllers_dir, exist_ok=True)
os.makedirs(routes_dir, exist_ok=True)
os.makedirs(middlewares_dir, exist_ok=True)

# 1. authMiddleware.js
auth_middleware_code = '''const jwt = require('jsonwebtoken');
const User = require('../models/User');

const protect = async (req, res, next) => {
  let token;
  if (req.headers.authorization && req.headers.authorization.startsWith('Bearer')) {
    token = req.headers.authorization.split(' ')[1];
  } else if (req.cookies && req.cookies.token) {
    token = req.cookies.token;
  }

  if (!token) {
    return res.status(401).json({ message: 'Chưa đăng nhập, vui lòng đăng nhập để tiếp tục' });
  }

  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET || 'velmora_super_secure_jwt_secret_key_2026_epu');
    const user = await User.findOne({ id: decoded.id }).select('-password');
    if (!user) {
      return res.status(401).json({ message: 'Tài khoản không tồn tại trên hệ thống' });
    }
    req.user = user;
    next();
  } catch (err) {
    return res.status(401).json({ message: 'Token không hợp lệ hoặc đã hết hạn' });
  }
};

const authorize = (...roles) => {
  return (req, res, next) => {
    if (!req.user || !roles.includes(req.user.role)) {
      return res.status(403).json({ message: 'Bạn không có quyền truy cập chức năng này' });
    }
    next();
  };
};

module.exports = { protect, authorize };
'''
with open(os.path.join(middlewares_dir, 'authMiddleware.js'), 'w', encoding='utf-8') as f:
    f.write(auth_middleware_code)

# 2. Group 1: Products, Categories, Materials, Banners, ShopSettings
product_ctrl = '''const Product = require('../models/Product');

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
'''
with open(os.path.join(controllers_dir, 'productController.js'), 'w', encoding='utf-8') as f:
    f.write(product_ctrl)

product_routes = '''const express = require('express');
const router = express.Router();
const productController = require('../controllers/productController');
const { protect, authorize } = require('../middlewares/authMiddleware');

router.get('/', productController.getProducts);
router.get('/:id', productController.getProductById);
router.post('/', protect, authorize('admin', 'staff'), productController.createProduct);
router.put('/:id', protect, authorize('admin', 'staff'), productController.updateProduct);
router.delete('/:id', protect, authorize('admin'), productController.deleteProduct);

module.exports = router;
'''
with open(os.path.join(routes_dir, 'productRoutes.js'), 'w', encoding='utf-8') as f:
    f.write(product_routes)

# Categories
category_ctrl = '''const Category = require('../models/Category');

exports.getCategories = async (req, res) => {
  try {
    const categories = await Category.find().sort({ id: 1 });
    res.json(categories);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.getCategoryById = async (req, res) => {
  try {
    const category = await Category.findOne({ id: Number(req.params.id) });
    if (!category) return res.status(404).json({ message: 'Không tìm thấy danh mục' });
    res.json(category);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.createCategory = async (req, res) => {
  try {
    const maxCat = await Category.findOne().sort({ id: -1 });
    const newId = maxCat ? maxCat.id + 1 : 1;
    const cat = await Category.create({ ...req.body, id: newId });
    res.status(201).json(cat);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};

exports.updateCategory = async (req, res) => {
  try {
    const cat = await Category.findOneAndUpdate({ id: Number(req.params.id) }, req.body, { new: true });
    if (!cat) return res.status(404).json({ message: 'Không tìm thấy danh mục' });
    res.json(cat);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};

exports.deleteCategory = async (req, res) => {
  try {
    const cat = await Category.findOneAndDelete({ id: Number(req.params.id) });
    if (!cat) return res.status(404).json({ message: 'Không tìm thấy danh mục' });
    res.json({ message: 'Xoá danh mục thành công' });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};
'''
with open(os.path.join(controllers_dir, 'categoryController.js'), 'w', encoding='utf-8') as f:
    f.write(category_ctrl)

category_routes = '''const express = require('express');
const router = express.Router();
const categoryController = require('../controllers/categoryController');
const { protect, authorize } = require('../middlewares/authMiddleware');

router.get('/', categoryController.getCategories);
router.get('/:id', categoryController.getCategoryById);
router.post('/', protect, authorize('admin'), categoryController.createCategory);
router.put('/:id', protect, authorize('admin'), categoryController.updateCategory);
router.delete('/:id', protect, authorize('admin'), categoryController.deleteCategory);

module.exports = router;
'''
with open(os.path.join(routes_dir, 'categoryRoutes.js'), 'w', encoding='utf-8') as f:
    f.write(category_routes)

# Materials
material_ctrl = '''const Material = require('../models/Material');

exports.getMaterials = async (req, res) => {
  try {
    const materials = await Material.find().sort({ id: 1 });
    res.json(materials);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.getMaterialById = async (req, res) => {
  try {
    const material = await Material.findOne({ id: Number(req.params.id) });
    if (!material) return res.status(404).json({ message: 'Không tìm thấy chất liệu' });
    res.json(material);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};
'''
with open(os.path.join(controllers_dir, 'materialController.js'), 'w', encoding='utf-8') as f:
    f.write(material_ctrl)

material_routes = '''const express = require('express');
const router = express.Router();
const materialController = require('../controllers/materialController');

router.get('/', materialController.getMaterials);
router.get('/:id', materialController.getMaterialById);

module.exports = router;
'''
with open(os.path.join(routes_dir, 'materialRoutes.js'), 'w', encoding='utf-8') as f:
    f.write(material_routes)

# Banners
banner_ctrl = '''const Banner = require('../models/Banner');

exports.getBanners = async (req, res) => {
  try {
    const banners = await Banner.find();
    res.json(banners);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.getActiveBanner = async (req, res) => {
  try {
    const banner = await Banner.findOne({ isActive: true });
    res.json(banner || null);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.createBanner = async (req, res) => {
  try {
    const maxB = await Banner.findOne().sort({ id: -1 });
    const newId = maxB ? maxB.id + 1 : 1;
    const banner = await Banner.create({ ...req.body, id: newId });
    res.status(201).json(banner);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};

exports.updateBanner = async (req, res) => {
  try {
    const banner = await Banner.findOneAndUpdate({ id: Number(req.params.id) }, req.body, { new: true });
    if (!banner) return res.status(404).json({ message: 'Không tìm thấy banner' });
    res.json(banner);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};

exports.deleteBanner = async (req, res) => {
  try {
    const banner = await Banner.findOneAndDelete({ id: Number(req.params.id) });
    if (!banner) return res.status(404).json({ message: 'Không tìm thấy banner' });
    res.json({ message: 'Xoá banner thành công' });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};
'''
with open(os.path.join(controllers_dir, 'bannerController.js'), 'w', encoding='utf-8') as f:
    f.write(banner_ctrl)

banner_routes = '''const express = require('express');
const router = express.Router();
const bannerController = require('../controllers/bannerController');
const { protect, authorize } = require('../middlewares/authMiddleware');

router.get('/', bannerController.getBanners);
router.get('/active', bannerController.getActiveBanner);
router.post('/', protect, authorize('admin'), bannerController.createBanner);
router.put('/:id', protect, authorize('admin'), bannerController.updateBanner);
router.delete('/:id', protect, authorize('admin'), bannerController.deleteBanner);

module.exports = router;
'''
with open(os.path.join(routes_dir, 'bannerRoutes.js'), 'w', encoding='utf-8') as f:
    f.write(banner_routes)

# ShopSettings
shop_setting_ctrl = '''const ShopSetting = require('../models/ShopSetting');

exports.getShopSettings = async (req, res) => {
  try {
    const settings = await ShopSetting.findOne();
    res.json(settings || {});
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.updateShopSettings = async (req, res) => {
  try {
    let settings = await ShopSetting.findOne();
    if (settings) {
      settings = await ShopSetting.findOneAndUpdate({}, req.body, { new: true });
    } else {
      settings = await ShopSetting.create({ ...req.body, id: 1 });
    }
    res.json(settings);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};
'''
with open(os.path.join(controllers_dir, 'shopSettingController.js'), 'w', encoding='utf-8') as f:
    f.write(shop_setting_ctrl)

shop_setting_routes = '''const express = require('express');
const router = express.Router();
const shopSettingController = require('../controllers/shopSettingController');
const { protect, authorize } = require('../middlewares/authMiddleware');

router.get('/', shopSettingController.getShopSettings);
router.put('/', protect, authorize('admin'), shopSettingController.updateShopSettings);

module.exports = router;
'''
with open(os.path.join(routes_dir, 'shopSettingRoutes.js'), 'w', encoding='utf-8') as f:
    f.write(shop_setting_routes)

print("Generated Group 1 (Storefront) successfully!")

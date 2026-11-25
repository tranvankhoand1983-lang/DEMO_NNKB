require('dotenv').config();
const path = require('path');
const fs = require('fs');
const mongoose = require('mongoose');

// Import Models
const User = require('./models/User');
const Category = require('./models/Category');
const Material = require('./models/Material');
const Product = require('./models/Product');
const Order = require('./models/Order');
const Cart = require('./models/Cart');
const Promotion = require('./models/Promotion');
const UserVoucher = require('./models/UserVoucher');
const Banner = require('./models/Banner');
const Review = require('./models/Review');
const ShopSetting = require('./models/ShopSetting');
const Favorite = require('./models/Favorite');
const Wishlist = require('./models/Wishlist');
const Service = require('./models/Service');
const Supplier = require('./models/Supplier');

const seedsDir = path.resolve(__dirname, '../../database/seeds');

const loadJson = (fileName) => {
  const filePath = path.join(seedsDir, fileName);
  if (!fs.existsSync(filePath)) return [];
  const raw = fs.readFileSync(filePath, 'utf-8');
  return JSON.parse(raw);
};

const runSeed = async () => {
  try {
    const mongoUri = process.env.MONGO_URI || 'mongodb://127.0.0.1:27017/web_trang_suc';
    console.log(`Connecting to MongoDB: ${mongoUri}...`);
    await mongoose.connect(mongoUri);
    console.log('MongoDB connected successfully!');

    // 1. Categories
    const categories = loadJson('categories.json');
    await Category.deleteMany({});
    if (categories.length) await Category.insertMany(categories);
    console.log(`✔ Categories seeded: ${categories.length}`);

    // 2. Materials
    const materials = loadJson('materials.json');
    await Material.deleteMany({});
    if (materials.length) await Material.insertMany(materials);
    console.log(`✔ Materials seeded: ${materials.length}`);

    // 3. Products
    const products = loadJson('products.json');
    await Product.deleteMany({});
    if (products.length) await Product.insertMany(products);
    console.log(`✔ Products seeded: ${products.length}`);

    // 4. Users
    const users = loadJson('users.json');
    await User.deleteMany({});
    if (users.length) await User.insertMany(users);
    console.log(`✔ Users seeded: ${users.length}`);

    // 5. Orders
    const orders = loadJson('orders.json');
    await Order.deleteMany({});
    if (orders.length) await Order.insertMany(orders);
    console.log(`✔ Orders seeded: ${orders.length}`);

    // 6. Carts
    const carts = loadJson('carts.json');
    await Cart.deleteMany({});
    if (carts.length) await Cart.insertMany(carts);
    console.log(`✔ Carts seeded: ${carts.length}`);

    // 7. Promotions
    const promotions = loadJson('promotions.json');
    await Promotion.deleteMany({});
    if (promotions.length) await Promotion.insertMany(promotions);
    console.log(`✔ Promotions seeded: ${promotions.length}`);

    // 8. User Vouchers
    const userVouchers = loadJson('user_vouchers.json');
    await UserVoucher.deleteMany({});
    if (userVouchers.length) await UserVoucher.insertMany(userVouchers);
    console.log(`✔ User Vouchers seeded: ${userVouchers.length}`);

    // 9. Banners
    const banners = loadJson('banners.json');
    await Banner.deleteMany({});
    if (banners.length) await Banner.insertMany(banners);
    console.log(`✔ Banners seeded: ${banners.length}`);

    // 10. Reviews
    const reviews = loadJson('reviews.json');
    await Review.deleteMany({});
    if (reviews.length) await Review.insertMany(reviews);
    console.log(`✔ Reviews seeded: ${reviews.length}`);

    // 11. Shop Settings
    const shopSettings = loadJson('shop_settings.json');
    await ShopSetting.deleteMany({});
    if (shopSettings.length) await ShopSetting.insertMany(shopSettings);
    console.log(`✔ Shop Settings seeded: ${shopSettings.length}`);

    // 12. Clear empty tables if any
    await Favorite.deleteMany({});
    await Wishlist.deleteMany({});
    await Service.deleteMany({});
    await Supplier.deleteMany({});
    console.log('✔ Cleared/Ready: Favorites, Wishlist, Services, Suppliers');

    console.log('\n=== ALL SEEDS IMPORTED SUCCESSFULLY TO MONGODB ===');
    process.exit(0);
  } catch (err) {
    console.error('Seed error:', err);
    process.exit(1);
  }
};

runSeed();

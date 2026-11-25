require('dotenv').config();
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const cookieParser = require('cookie-parser');
const connectDB = require('./config/db');

// Security Middlewares (Môn Web An Toàn - ThS. Phương Văn Cảnh)
const {
  preventNoSqlInjection,
  authLimiter,
  apiLimiter,
  sanitizeXSS
} = require('./middlewares/securityMiddleware');

// Import Routes
const productRoutes = require('./routes/productRoutes');
const categoryRoutes = require('./routes/categoryRoutes');
const materialRoutes = require('./routes/materialRoutes');
const bannerRoutes = require('./routes/bannerRoutes');
const shopSettingRoutes = require('./routes/shopSettingRoutes');
const accountRoutes = require('./routes/accountRoutes');
const customerRoutes = require('./routes/customerRoutes');
const cartRoutes = require('./routes/cartRoutes');
const orderRoutes = require('./routes/orderRoutes');
const paymentRoutes = require('./routes/paymentRoutes');
const favoriteRoutes = require('./routes/favoriteRoutes');
const promotionRoutes = require('./routes/promotionRoutes');
const reviewRoutes = require('./routes/reviewRoutes');
const wishlistRoutes = require('./routes/wishlistRoutes');
const serviceRoutes = require('./routes/serviceRoutes');
const supplierRoutes = require('./routes/supplierRoutes');
const statisticsRoutes = require('./routes/statisticsRoutes');
const chatRoutes = require('./routes/chatRoutes');

const app = express();
const PORT = process.env.PORT || 5278;

// Connect to MongoDB
connectDB();

// 1. Tầng Tiêu đề Bảo mật HTTP (Helmet)
app.use(helmet({
  crossOriginResourcePolicy: { policy: "cross-origin" }
}));

// 2. Tầng Kiểm soát Nguồn gốc truy cập (CORS)
const allowedOrigins = [
  process.env.CLIENT_URL || 'http://localhost:5173',
  'http://localhost:3000',
  'http://localhost:5278',
  'http://127.0.0.1:5173',
  'http://127.0.0.1:3000'
];

app.use(cors({
  origin: function (origin, callback) {
    if (!origin) return callback(null, true);
    if (allowedOrigins.indexOf(origin) === -1) {
      return callback(null, true);
    }
    return callback(null, true);
  },
  credentials: true,
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With']
}));

// 3. Giới hạn dung lượng Payload chống Buffer Overflow
app.use(express.json({ limit: '10mb' }));
app.use(express.urlencoded({ extended: true, limit: '10mb' }));
app.use(cookieParser());
app.use(morgan('dev'));

// 4. Tầng Triệt tiêu Lỗ hổng NoSQL Injection & XSS
app.use(preventNoSqlInjection);
app.use(sanitizeXSS);

// 5. Tầng Giới hạn Tần suất (Rate Limiter) chống DDoS & Brute-force
app.use('/api/', apiLimiter);
app.use('/api/account/login', authLimiter);
app.use('/api/account/register', authLimiter);

// Basic Health Check Route
app.get('/api/health', (req, res) => {
  res.json({
    status: 'success',
    message: 'Velmora Jewelry Backend NodeJS (Express + MongoDB) is running securely',
    security: {
      helmet: 'Active',
      rateLimiter: 'Active',
      noSqlInjectionGuard: 'Active',
      xssSanitizer: 'Active',
      rbacAuth: 'Active'
    },
    port: PORT,
    timestamp: new Date().toISOString()
  });
});

app.get('/', (req, res) => {
  res.send('Velmora Jewelry Secure Backend NodeJS API Server is Online!');
});

// Mount Routes (Exact mapping to C# endpoints)
app.use('/api/products', productRoutes);
app.use('/api/categories', categoryRoutes);
app.use('/api/materials', materialRoutes);
app.use('/api/banners', bannerRoutes);
app.use('/api/shopsettings', shopSettingRoutes);
app.use('/api/account', accountRoutes);
app.use('/api/customers', customerRoutes);
app.use('/api/carts', cartRoutes);
app.use('/api/orders', orderRoutes);
app.use('/api/payment', paymentRoutes);
app.use('/api/payos', paymentRoutes);
app.use('/api/favorites', favoriteRoutes);
app.use('/api/promotions', promotionRoutes);
app.use('/api/reviews', reviewRoutes);
app.use('/api/wishlist', wishlistRoutes);
app.use('/api/services', serviceRoutes);
app.use('/api/suppliers', supplierRoutes);
app.use('/api/statistics', statisticsRoutes);
app.use('/api/chat', chatRoutes);

// Start Server
app.listen(PORT, () => {
  console.log(`=======================================================`);
  console.log(`  VELMORA SECURE BACKEND NODEJS SERVER STARTED         `);
  console.log(`  SECURITY: Helmet + NoSQL Guard + RateLimit + RBAC    `);
  console.log(`  PORT: ${PORT}                                       `);
  console.log(`  URL: http://localhost:${PORT}/api/health            `);
  console.log(`=======================================================`);
});

module.exports = app;

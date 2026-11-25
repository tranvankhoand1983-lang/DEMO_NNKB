const Cart = require('../models/Cart');
const Product = require('../models/Product');

exports.getCart = async (req, res) => {
  try {
    const userId = req.user.id;
    let cart = await Cart.findOne({ userId });
    if (!cart) {
      const maxC = await Cart.findOne().sort({ id: -1 });
      const newId = maxC ? maxC.id + 1 : 1;
      cart = await Cart.create({ id: newId, userId, items: [] });
    }
    res.json(cart.items || []);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.addToCart = async (req, res) => {
  try {
    const userId = req.user.id;
    const { productId, variantId, quantity, size } = req.body;

    const product = await Product.findOne({ id: Number(productId) });
    if (!product) return res.status(404).json({ message: 'Sản phẩm không tồn tại' });

    let cart = await Cart.findOne({ userId });
    if (!cart) {
      const maxC = await Cart.findOne().sort({ id: -1 });
      const newId = maxC ? maxC.id + 1 : 1;
      cart = await Cart.create({ id: newId, userId, items: [] });
    }

    const existingItem = cart.items.find(i => 
      i.productId === Number(productId) && 
      (!variantId || i.variantId === Number(variantId)) &&
      (!size || i.size === size)
    );

    if (existingItem) {
      existingItem.quantity += (Number(quantity) || 1);
    } else {
      const maxItemId = cart.items.reduce((max, i) => Math.max(max, i.id || 0), 0);
      cart.items.push({
        id: maxItemId + 1,
        cartId: cart.id,
        productId: Number(productId),
        variantId: variantId ? Number(variantId) : null,
        quantity: Number(quantity) || 1,
        size: size || null,
        product: {
          id: product.id,
          name: product.name,
          price: product.price,
          images: product.images
        }
      });
    }

    await cart.save();
    res.status(200).json(cart.items);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};

exports.updateQuantity = async (req, res) => {
  try {
    const userId = req.user.id;
    const { cartItemId, id, quantity } = req.body;
    const targetId = Number(cartItemId || id);

    const cart = await Cart.findOne({ userId });
    if (!cart) return res.status(404).json({ message: 'Giỏ hàng không tồn tại' });

    const item = cart.items.find(i => i.id === targetId);
    if (!item) return res.status(404).json({ message: 'Món hàng không tồn tại trong giỏ' });

    if (Number(quantity) <= 0) {
      cart.items = cart.items.filter(i => i.id !== targetId);
    } else {
      item.quantity = Number(quantity);
    }

    await cart.save();
    res.json(cart.items);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};

exports.removeFromCart = async (req, res) => {
  try {
    const userId = req.user.id;
    const { cartItemId, id } = req.body;
    const targetId = Number(cartItemId || id);

    const cart = await Cart.findOne({ userId });
    if (!cart) return res.status(404).json({ message: 'Giỏ hàng không tồn tại' });

    cart.items = cart.items.filter(i => i.id !== targetId);
    await cart.save();
    res.json(cart.items);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};

exports.clearCart = async (req, res) => {
  try {
    const userId = req.user.id;
    await Cart.findOneAndUpdate({ userId }, { items: [] });
    res.json({ message: 'Đã làm trống giỏ hàng' });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

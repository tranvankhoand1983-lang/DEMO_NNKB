const Category = require('../models/Category');

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

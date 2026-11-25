const Supplier = require('../models/Supplier');

exports.getSuppliers = async (req, res) => {
  try {
    const suppliers = await Supplier.find();
    res.json(suppliers);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.getSupplierById = async (req, res) => {
  try {
    const supplier = await Supplier.findOne({ id: Number(req.params.id) });
    if (!supplier) return res.status(404).json({ message: 'Không tìm thấy nhà cung cấp' });
    res.json(supplier);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.createSupplier = async (req, res) => {
  try {
    const maxS = await Supplier.findOne().sort({ id: -1 });
    const newId = maxS ? maxS.id + 1 : 1;
    const s = await Supplier.create({ ...req.body, id: newId });
    res.status(201).json(s);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};

exports.deleteSupplier = async (req, res) => {
  try {
    await Supplier.findOneAndDelete({ id: Number(req.params.id) });
    res.json({ message: 'Xoá nhà cung cấp thành công' });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

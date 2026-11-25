const User = require('../models/User');

exports.getCustomers = async (req, res) => {
  try {
    const customers = await User.find().select('-password').sort({ createdAt: -1 });
    res.json(customers);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.getCustomerById = async (req, res) => {
  try {
    const customer = await User.findOne({ id: req.params.id }).select('-password');
    if (!customer) return res.status(404).json({ message: 'Không tìm thấy khách hàng' });
    res.json(customer);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.updateCustomer = async (req, res) => {
  try {
    const customer = await User.findOneAndUpdate({ id: req.params.id }, req.body, { new: true }).select('-password');
    if (!customer) return res.status(404).json({ message: 'Không tìm thấy khách hàng' });
    res.json(customer);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};

exports.deleteCustomer = async (req, res) => {
  try {
    const customer = await User.findOneAndDelete({ id: req.params.id });
    if (!customer) return res.status(404).json({ message: 'Không tìm thấy khách hàng' });
    res.json({ message: 'Xoá khách hàng thành công' });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

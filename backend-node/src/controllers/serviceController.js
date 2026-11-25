const Service = require('../models/Service');

exports.getServices = async (req, res) => {
  try {
    const services = await Service.find();
    res.json(services);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.getServiceById = async (req, res) => {
  try {
    const service = await Service.findOne({ id: Number(req.params.id) });
    if (!service) return res.status(404).json({ message: 'Không tìm thấy dịch vụ' });
    res.json(service);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

exports.createService = async (req, res) => {
  try {
    const maxS = await Service.findOne().sort({ id: -1 });
    const newId = maxS ? maxS.id + 1 : 1;
    const s = await Service.create({ ...req.body, id: newId });
    res.status(201).json(s);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
};

exports.deleteService = async (req, res) => {
  try {
    await Service.findOneAndDelete({ id: Number(req.params.id) });
    res.json({ message: 'Xoá dịch vụ thành công' });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
};

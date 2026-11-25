const Material = require('../models/Material');

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
